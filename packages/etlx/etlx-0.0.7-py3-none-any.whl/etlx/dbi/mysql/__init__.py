from etlx.dbi.mysql.dbi_mysqldb import DBI_MySQL_MySQLdb
from etlx.dbi.mysql.metadata import MySQL_MetadataMixIn

class DBI_MySQL(MySQL_MetadataMixIn, DBI_MySQL_MySQLdb):
    pass

DBI = DBI_MySQL
