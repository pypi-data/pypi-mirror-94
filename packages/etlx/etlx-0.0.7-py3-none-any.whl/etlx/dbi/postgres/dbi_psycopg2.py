import psycopg2
from etlx.dbi.abc import DBI
from etlx.sql import SQL

class SQL_Postgres(SQL):
    pass
   

class DBI_Postgres_psycopg2(DBI):

    SQL = SQL_Postgres

    def connect_factory(self, **kwargs):
        return psycopg2.connect(**kwargs)
