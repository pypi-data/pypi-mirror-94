import os
from automapdb.utils import format_return, set_logger
from automapdb.table import TableManager
from automapdb.mappings import TableMappings
from automapdb.db import AutoMapDB
import fire


class FireCLI:
    def __init__(self, connection_string=None, log_level="INFO"):
        set_logger(log_level)
        connection_string = connection_string or os.getenv("PG_CONNECTION")
        db = AutoMapDB(connection_string)
        db.connect()
        self.table = TableManager(db)
        self.mapping = TableMappings(db)


@format_return
def main(fmt="str"):
    fire.Fire(FireCLI)


if __name__ == "__main__":
    main()
