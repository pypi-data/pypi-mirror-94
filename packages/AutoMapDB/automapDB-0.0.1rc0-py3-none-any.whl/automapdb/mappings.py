import json
from automapdb.utils import log
from automapdb.utils import format_return
from automapdb.utils import filter_dict


class TableMappings:
    def __init__(self, db, tables_file="tables.json"):
        self.db = db
        self.mappings_file = tables_file
        self.mappings = {}
        try:
            read_file = open(self.mappings_file)
            try:
                self.mappings = json.load(read_file)
            except Exception as err:
                log.error(repr(err))
                self.mappings = {}
        except FileNotFoundError:
            log.warning(f"File {tables_file} not found. Creating one!")
            self._dump()

    def add(self, path, name=None, get_args=None, set_args=None):
        """Add / Update a table mapping for the ORM mapping

        Updates the json source file.
        If path already exists, it is updated.
        It will then be available for the CLI CRUD operations of this tool

        Args:
            name (str): Name which is referenced from CLI
            path (str): Exact short_name of the table in database
            get_args (list): Fields required to retrieve a db entry
            set_args (list): Fields required to add an entry
        """
        table = self.db.get_table(path)
        name = name or table.path
        data = {
            name: {
                "path": table.path,
                # Args needed to add an objects are not nullable
                "get_args": get_args or table.primary_keys(),
                # Args needed to query an object are the primary keys
                "set_args": set_args or table.not_nullable(),
            }
        }
        for map_name, mapping in self.mappings.copy().items():
            if mapping["path"] == path:
                del self.mappings[map_name]
        self.mappings.update(data)
        self._dump()

    def list_all(self, schema="public"):
        """Shows tables on server in given schema
        Args:
            schema (str): Name of schema containing desired tables
        """
        self.db.set_schema(schema)
        data = {}
        for cls in self.db.classes:
            table = self.db.get_table(str(cls.__table__))
            data[table.name] = {
                    "path": table.path,
                    "get_args": table.primary_keys(),
                    "set_args": table.not_nullable(),
                }
        return data

    def add_all(self, schema="public"):
        """Shows/Creates a map entry for every table in given schema
        Args:
            schema (str): Name of schema containing desired tables
        """
        self.db.set_schema(schema)
        for cls in self.db.classes:
            table = self.db.get_table(str(cls.__table__))
            data = {
                table.name: {
                    "path": table.path,
                    "get_args": table.primary_keys(),
                    "set_args": table.not_nullable(),
                }
            }
            self.add(**data[table.name])
        self._dump()

    def update(self, path, name=None, get_args=None, set_args=None, new_path=None):
        """Add / Update a table mapping for the ORM mapping

        Updates the json source file. If path already exists, it is updated.
        It will then be available for CRUD operations of this tool.

        Args:
            name (str): Name which is referenced from CLI
            path (str): Exact short_name of the table in database
            get_args (list): Fields required to retrieve a db entry
            set_args (list): Fields required to add an entry
            new_path (str): New datbase path for given table (schema.table)
        """
        map_name, mapping = self._get_mapping_by_path(path)
        name = name or map_name
        if new_path and len(new_path.split(".")) < 2:
            msg = f"Invalid new_path: '{path}'! Does it contain schema.table? "
            raise Exception(msg)
        data = {
            name: {
                "path": new_path or mapping["path"],
                "get_args": get_args or mapping["get_args"],
                "set_args": set_args or mapping["set_args"],
            }
        }
        del self.mappings[map_name]
        self.mappings.update(data)
        self._dump()

    @format_return
    def show(self, path, from_server=False, fmt=None) -> dict:
        """Find mapping in tables.json or search online in database

        Args:
            path (str): Dotted path to desired table
            from_server (bool): Get def from Database instead from local file
        """
        data = {}
        if from_server:
            table = self.db.get_table(path)
            name = table.path
            data = {
                name: {
                    "path": table.path,
                    "get_args": table.primary_keys(),
                    "set_args": table.not_nullable(),
                }
            }
        else:
            map_name, mapping = self._get_mapping_by_path(path)
            data = {map_name: mapping}
        return data

    @format_return
    def show_fields(self, path, fmt=None) -> list:
        """
        Shows the name, datatype, primary_key and nullable flags
        for the columns of given Table if database
        """
        table = self.db.get_table(path)
        filter = ["type", "nullable", "primary_key", "name"]
        return [filter_dict(c, incl=filter) for c in table.columns]

    @format_return
    def list(self, fmt=None):
        """ List mapped table from the tables.json file """
        return self.mappings

    def delete(self, name):
        """Deletes the TableManager Definition from the definitions file"""
        del self.mappings[name]  # Find definition in list and delete
        self._dump()

    def _dump(self):
        """ Dumps table dictionary to tables.json """
        with open(self.mappings_file, "w") as write_file:
            json.dump(self.mappings, write_file, indent=4)
            log.debug(str(write_file))

    def _get_mapping_by_path(self, path):
        """Search in tables.json for Mapping with given path"""
        for map_name, mapping in self.mappings.items():
            if mapping["path"] == path:
                return map_name, mapping
        else:
            raise Exception(f"Mapping for path not found: {path}", exit=1)

    def _get_mapping_by_name(self, name):
        """Search in tables.json for Mapping with given name"""
        try:
            mapping = self.mappings[name]
            return name, mapping
        except KeyError as err:
            raise Exception(f"Mapping for path not found: {name}", exit=1)

    def __getitem__(self, item):
        return self.mappings[item]
