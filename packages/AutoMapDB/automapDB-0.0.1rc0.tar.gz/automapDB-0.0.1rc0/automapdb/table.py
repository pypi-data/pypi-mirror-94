#!/usr/bin/python3
# -*- coding: utf-8 -*-

import inspect
from automapdb.mappings import TableMappings
from automapdb.utils import log, format_return, joinsep, filter_dict

import fire
import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound

USAGE_TEMPLATE = """\
ERROR: Missing fields: {}
Usage: i2b2fire {action} {} {} [{}]



For detailed information on this command, run:
    i2b2fire.py {action} --help"""


class TableManager:
    """CRUD interface to Database objects"""
    def __init__(self, db, tables_file="tables.json"):
        """Create basic tables_file and data structure

        * Create Conf from tables_file folder (arg)
        * Create AutoMapDB from Conf data
        * Set default columns for add() method

        The main constructor is used to glue the database
        and tables_file data to this central object.
        Further initiation happens in init_table when a method is called
        with the table to modify.
        """
        # Set in init_table when the the table is known
        self.db = db  # AutoMapDB object for SQLAlchemy connection
        self.tables_file = tables_file  # tables_file path
        self.path = None  # Dotted path to table, eg. i2b2pm.pm_project_data
        self.schema = None  # Schema short_name, i2b2pm/i2b2hive
        self.columns = None  # List of columns in table
        self.tab_name = None  # short_name as in Database, eg. pm_project_data
        self.set_args = None  # Args needed to add row. Read from definitions
        self.get_args = None  # Args needed to query data.
        self.opt_args = None  # Optional args
        self.short_name = None  # User given short_name as in definitions
        self.alchemy_table = None  # SQLAlchemy alchemy_table class
        self.definitions = TableMappings(self.db, self.tables_file)

        self.default_columns = {
            "change_date": "NOW()",
            "entry_date": "NOW()",
            "c_change_date": "NOW()",
            "c_entry_date": "NOW()",
            "status_cd": "A",
            "c_status_cd": "A",
            "changeby_char": "i2b2fire",
        }

    def _init_table(self, table: str) -> None:
        """Map ORM table attributes to this instance
        Args:
            table (str): Name of table to be searched in tables
        """
        self.short_name = table
        # Map DB_TABLES attributes to self (set_args, get_args, path)
        self.__dict__.update(self.definitions[table])
        self.set_args = self.definitions[table]["set_args"]
        self._set_table(self.path)

    def _set_table(self, path) -> None:
        table = self.db.get_table(path)
        self.__dict__.update(table.__dict__)
        log.debug(f"{table.path}")

    def query(self, table: str, *args) -> dict:
        """Construct raw SQL query for a table.

        Called by add, update, delete, list.
        Args are mapped to not nullable fields on postgres table
        Args:
            table (str): alchemy_table short_name from definitions to query
            args (str): Values for get_args required to find row
        """
        self._init_table(table)
        # Validate args against table fields from table def
        self._check_args(args, self.get_args)
        query = self.db.session.query(self.alchemy_table)
        # Concatenate required and optional args
        for index, arg in enumerate(self.get_args):
            # If local arg is a valid column in the table:
            if arg in self.columns:
                # Get local column attribute from ORM class
                table_column = getattr(self.alchemy_table, arg)
                # Concatenate excl statement
                # (alchemy_table.column == arg) to query
                query = query.filter(table_column == args[index])
        log.debug(str(query)[:40] + str(query)[-40:-1])
        return query

    def query_dict(self, table, data):
        self._init_table(table)
        query = self.db.session.query(self.alchemy_table)
        query = query.filter_by(**data)
        log.debug(str(query)[:40] + str(query)[-40:-1])
        return query

    @format_return
    def list_fields(self, table, fmt=None) -> list:
        """
        Shows the name, datatype, primary_key and nullable flags
        for the columns of given Table
        """
        self._init_table(table)
        filter = ["type", "nullable", "primary_key", "name"]
        return [filter_dict(c, incl=filter) for c in self.columns]

    @format_return
    def list(self, table: str, fields: list = None, **kwargs) -> list:
        """Open query to table with kwargs as WHERE filters"""
        self._init_table(table)
        # Query only table to get all the rows
        query = self.db.session.query(self.alchemy_table)
        # Iterate kwargs to construct filters
        for key, value in kwargs.items():
            # use only kwargs that are valid columns
            if key in self.columns:
                # Get kwarg as Column object
                table_column = getattr(self.alchemy_table, key)
                # Filter where Column == Value
                query = query.filter(table_column == value)
        log.debug(query)
        return [filter_dict(q, incl=fields) for q in query.all()]

    def add(self, table, *args):
        """
        Add row to table, with args mapped to the table's not_nullable fields
        """
        log.debug(f"ADD: {table} {args}")
        self._init_table(table)
        u_args = self.set_args + list(self.default_columns.keys())
        self.opt_args = [c.name for c in self.columns if c.name not in u_args]
        # If number of args doesn't match number of required args
        self._check_args(args, self.set_args, self.opt_args)
        new_row_data = {}
        # Iterate ORM table & write values from default_columns to a new dict
        for col in self.columns:
            new_row_data[col.name] = self.default_columns.get(col.name, None)
        # Iterate over required + optional arg names with an index
        for index, arg in enumerate(self.set_args + self.opt_args):
            # If local arg is a valid column in the table:
            if arg in self.columns:
                try:
                    # Get user arg value by index,
                    # map short_name: value to new dict
                    new_row_data.update({arg: args[index]})
                except IndexError:
                    # If not all optional fields are filled, use None
                    new_row_data.update({arg: None})
        # Create new SQL Table with unpacked data as kwargs
        new_row = self.alchemy_table(**new_row_data)
        # Add
        self.db.add(new_row)

    def update(self, table, *args):
        """Update row with args mapped to the table's not_nullable fields"""
        log.debug(f"UPDATE: {table} {args}")
        # Get raw query
        query = self.query(table, *args)
        # Add column + value to update
        arg_list = self.get_args + ["key", "value"]
        self._check_args(args, arg_list)
        # Dict from last and second to last args {key: value}
        update_data = {args[-2]: args[-1]}
        log.debug(str(update_data))
        if len(query.all()) == 0:
            raise sqlalchemy.orm.exc.NoResultFound("")
        self.db.update(query, update_data)

    @format_return
    def get(self, table, *args, fields=None, n="one", fmt="") -> list or dict:
        """Query database for one/multiple rows.
        Use args to provide the primary keys

        Args:
            table (str): Name of table to query
            n (str): Amount of results as string (all/one)
            *args (list): List of values to excl for
            fields (list): Fields which are shown by the query
        """
        fields = fields or []
        log.debug(f"GET: {table} {args} {fields} {n}")
        if n == "one":
            try:
                query = self.query(table, *args).one()
            except NoResultFound as err:
                raise NoResultFound(f"{err}: {table}: {args}")
            data = filter_dict(query, incl=fields)
        else:
            query = self.query(table, *args).all()
            data = [filter_dict(q, incl=fields) for q in query]
        return data

    def delete(self, table, *args):
        """Delete row from table"""
        log.debug(f"DEL: {table} {args}")
        query = self.query(table, *args).all()
        log.debug(str(query))
        if not query:
            return False
        for q in query:
            self.db.delete(q)
        return True

    def _check_args(self, args: tuple, mandatory_args: list, opt_args=None):
        opt_args = opt_args or []
        action = inspect.stack()[1][3]
        usage = USAGE_TEMPLATE.format(
            joinsep(mandatory_args[len(args) :]),
            self.short_name,
            joinsep(mandatory_args, sep=" "),
            joinsep(opt_args, sep="|"),
            action=action,
        )
        if len(args) < len(mandatory_args):
            raise fire.core.FireError(usage)

    def validate_kwargs(self, **kwargs):
        pass
        # get_args = [c.name for c in self.columns if c.primary_key]
        # Args needed to query an object are the primary keys
        # set_args = [c.name for c in self.columns if not c.nullable]

    def __repr__(self):
        return self.__dict__
