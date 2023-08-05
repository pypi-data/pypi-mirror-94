from etlx.abc.row import RowDict
from etlx.sql import SQL


class DBI:

    SQL = SQL

    def __init__(self, *, connect=None):
        self._dbapi = None
        self._connect_kwargs = dict()
        if isinstance(connect,dict):
            self._connect_kwargs.update(connect)
        self._close_on_exit = False

    @property
    def database(self):
        return self._connect_kwargs.get("database")

    @property
    def sql(self):
        return self.SQL(self)

    @property
    def connected(self):
        return self._dbapi is not None

    def connect_factory(self, **kwargs):
        raise NotImplementedError()

    def connect(self, **kwargs):
        params = dict()
        params.update(self._connect_kwargs)
        params.update(kwargs)
        params = filter(lambda x: (x[1] != None), params.items())
        params = dict(params)
        self._dbapi = self.connect_factory(**params)

    def close(self):
        if self.connected:
            self._dbapi.close()
        self._dbapi = None

    def commit(self):
        self._dbapi.commit()

    def rollback(self):
        if self._dbapi:
            self._dbapi.rollback()

    def cursor(self, serverside=False):
        return self._dbapi.cursor()

    def execute(self, _sql, *args, **kwargs):
        if not isinstance(_sql, str):
            _sql = str(_sql)
        with self.cursor(serverside=False) as cursor:
            cursor.execute(_sql, args or kwargs)
            return cursor

    def query(self, _sql, *args, **kwargs):
        if not isinstance(_sql, str):
            _sql = str(_sql)
        with self.cursor(serverside=True) as cursor:
            cursor.execute(_sql, args or kwargs)
            for row in cursor:
                yield RowDict((d[0], v) for d, v in zip(cursor.description, row))

    def readone(self, _sql, *args, **kwargs):
        if not isinstance(_sql, str):
            _sql = str(_sql)
        with self.cursor(serverside=True) as cursor:
            cursor.execute(_sql, args or kwargs)
            row = cursor.fetchone()
            if row:
                row = RowDict((d[0], v) for d, v in zip(cursor.description, row))
            return row

    def __enter__(self):
        if not self.connected:
            self.connect()
            self._close_on_exit = True
        else:
            self._close_on_exit = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.connected:
            return
        if exc_type:
            self.rollback()
        else:
            self.commit()
        if self._close_on_exit:
            self.close()
