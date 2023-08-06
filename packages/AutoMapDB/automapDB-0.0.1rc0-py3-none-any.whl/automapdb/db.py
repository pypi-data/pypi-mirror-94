#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import atexit
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm.query import Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from automapdb.utils import log, singleton
from automapdb.utils import SQLException


@singleton
class AutoMapDB:
    """Manage Basic Database connection"""
    def __init__(self, connection_string, options=None, autocommit=False):
        """Create basic database session through SQLAlchemy"""
        log.debug(f"{self.__class__.__name__}")
        self.db_string = connection_string
        self.options = options or {"options": ""}
        self.raise_on_rollback = True
        self.autocommit = autocommit
        self.connection = None
        self.metadata = None
        self.session = None
        self.classes = None
        self.commit = False
        self.engine = None
        self.schema = None
        self.base = None
        if not self.db_string.startswith("postgresql://"):
            raise SQLException(f"Invalid connection: '{connection_string}'")

    def connect(self):
        """Create Engine, Connection and Session objects"""
        log.debug(f"Connecting to database: {self.db_string}")
        self.engine = create_engine(self.db_string, connect_args=self.options)
        self.connection = self.engine.connect()
        self.session = Session(self.engine, autoflush=True, expire_on_commit=False)
        log.debug("Connection and Session opened.")

    def connected(self):
        return self.connection and self.connection.closed == 0

    def set_schema(self, schema: str):
        """Create metadata object from schema short_name, map base to schema

        I found it impossible to map a base across all postgres schemas or
        use dotted table paths. Therefor a alchemy_table object needs to set,
        which schema it belongs to.
        """
        if self.schema == schema:
            return
        if self.connected():
            log.debug(f"Connected to schema {self.schema}. Committing queries.")
            self.session.commit()
        else:
            self.connect()
        self.schema = schema
        self.metadata = MetaData(bind=self.connection, schema=self.schema)
        self.base = automap_base(metadata=self.metadata)
        self.base.prepare(self.engine, reflect=True)
        self.classes = self.base.classes
        log.debug(f"Schema {self.schema} mapped")

    def post_statement(self, force_commit: bool = None):
        try:
            self.session.flush()
            self.commit = True
        except SQLAlchemyError as err:
            msg = f"{err.__cause__.__class__.__name__}: {err.__cause__}"
            log.error(msg.replace("\n", " "))
        except Exception as err:
            log.error(repr(err))
            self.session.rollback()
            self.commit = False
            log.warning("Rollback done!")
            if self.raise_on_rollback:
                raise err

        if force_commit or self.autocommit:
            try:
                log.warning("Trying autocommit...")
                self.session.commit()
            except Exception as err:
                msg = f"{err.__cause__.__class__.__name__}: {err.__cause__}"
                log.error(msg.replace("\n", " "))
                self.session.rollback()

    def execute(self, query: Query, *args):
        """Add `CREATE` query to psql session and flushes handler"""
        self.session.execute(query, *args)
        self.post_statement()

    def add(self, query: Query):
        """Add `CREATE` query to psql session and flushes handler"""
        self.session.add(query)
        self.post_statement()

    def update(self, query: Query, data: dict):
        """Add `UPDATE` query to the session and flushes the connection"""
        query.update(data)
        self.post_statement()

    def delete(self, query: Query):
        """Add `DELETE` query to psql session and flushes handler"""
        self.session.delete(query)
        self.post_statement()

    def get_table(self, path):
        try:
            schema, tab_name = path.split(".")
        except ValueError as err:
            msg = f"Invalid path: '{path}'! Does it contain schema.table? "
            raise Exception(msg)

        # Update database search path
        self.set_schema(schema)
        # Get SQLAlchemy alchemy_table object through db object
        alchemy_table = getattr(self.base.classes, tab_name)
        return ProxyTable(schema, tab_name, alchemy_table)


class ProxyTable:
    def __init__(self, schema, name, alchemy_table):
        self.name = name
        self.schema = schema
        self.alchemy_table = alchemy_table
        self.columns = self.alchemy_table.__table__.columns
        self.path = f"{schema}.{name}"

    def primary_keys(self):
        return [c.name for c in self.columns if c.primary_key]

    def not_nullable(self):
        return [c.name for c in self.columns if not c.nullable]


class AutoMapDBContext:
    def __init__(self, *args, **kwargs):
        self.db = AutoMapDB(*args, **kwargs)

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        # if exc_type:
        # raise exc_type, exc_value, traceback
        try:
            self.db.session.commit()
        except Exception as err:
            print(err)
        print("connt + exit")


# Ugly hack to ensure transactions are commited on exit
@atexit.register
def post_db():
    db = AutoMapDB("postgresql://")
    if db.commit:
        try:
            db.session.commit()
        except SQLAlchemyError as err:
            log.error(err)
            print(err)
