import sqlite3
from etlx.dbi.abc import DBI
from etlx.sql import SQL

class SQLite_Cursor(sqlite3.Cursor):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class SQL_SQLite(SQL):
    pass
   

class DBI_SQLite_sqlite3(DBI):

    SQL = SQL_SQLite

    def connect_factory(self, **kwargs):
        return sqlite3.connect(**kwargs)

    def cursor(self, serverside=False):
        return self._dbapi.cursor(factory=SQLite_Cursor)
