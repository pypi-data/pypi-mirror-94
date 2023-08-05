from etlx.dbi.postgres.dbi_psycopg2 import DBI_Postgres_psycopg2

class DBI_Postgres(DBI_Postgres_psycopg2):
    pass

DBI = DBI_Postgres
