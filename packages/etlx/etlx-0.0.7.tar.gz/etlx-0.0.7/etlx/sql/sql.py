from io import StringIO
from decimal import Decimal
from datetime import datetime, date, time


class SQL:
    def __init__(self, dbi=None):
        self.dbi = dbi
        self.buffer = StringIO()

    def __len__(self):
        return self.buffer.tell()

    def __str__(self):
        return self.buffer.getvalue()

    def __bool__(self):
        return len(self) > 0

    def sql(self, *args):
        for sql in args:
            if not isinstance(sql, str):
                sql = str(sql)
            self.buffer.write(sql)
        return self

    def execute(self, *args, **kwargs):
        return self.dbi.execute(self, *args, **kwargs)

    def query(self, *args, **kwargs):
        return self.dbi.query(self, *args, **kwargs)

    def quoted(self, *args):
        for i, name in enumerate(args):
            self.sql("," if i else "")
            self.sql('"' + name.replace('"', '""') + '"')
        return self

    def arg(self):
        return self.sql("%s")

    def kwarg(self, name):
        return self.sql(f"%({name})s")

    def literal(self, *args):
        for i, value in enumerate(args):
            self.sql("," if i else "")
            if value is None:
                self.sql("NULL")
            elif isinstance(value, bool):
                self.sql("1" if value else "0")
            elif isinstance(value, (int, float, Decimal)):
                self.sql(str(value))
            elif isinstance(value, (datetime, date, time)):
                self.sql("'", str(value), "'")
            elif isinstance(value, str):
                value = value.replace("'", "''")
                value = value.replace("%", "%%")
                self.sql("'", value, "'")
            elif isinstance(value, tuple):
                self.sql("(").literal(*value).sql(")")
            else:
                raise NotImplementedError()
        return self

    def _list(self, func, iterable, separator=","):
        for i, x in enumerate(iterable):
            self.sql(separator if i else "")
            func(x)

    def SELECT(self, *args, **kwargs):
        self.sql("SELECT ")
        if not args:
            self.sql("*")
        else:
            self._list(self.quoted, args)
        return self

    def FROM(self, table, database=None):
        self.sql(" FROM ")
        if database:
            self.quoted(database).sql(".")
        self.quoted(table)
        return self

    def INSERT(self, table, **kwargs):
        self.sql("INSERT INTO ").quoted(table)
        self.sql(" (").quoted(*kwargs.keys()).sql(") VALUES (").literal(
            *kwargs.values()
        ).sql(")")
        return self

    def INSERT_CV(self, table, columns, *rows):
        self.sql("INSERT INTO ").quoted(table)
        self.sql(" (").quoted(*columns).sql(") VALUES ")
        for i, values in enumerate(rows):
            self.sql("," if i else "")
            self.sql("(").literal(*values).sql(")")
        return self

    def UPDATE(self, table, **kwargs):
        self.sql("UPDATE ").quoted(table).sql(" SET ")
        for i, (k, v) in enumerate(kwargs.items()):
            self.sql("," if i else "")
            self.quoted(k).sql("=").literal(v)
        return self

    def UPDATE_CV(self, table, columns, values):
        self.sql("UPDATE ").quoted(table).sql(" SET ")
        for i, (k, v) in enumerate(zip(columns, values)):
            self.sql("," if i else "")
            self.quoted(k).sql("=").literal(v)
        return self

    def DELETE(self, table):
        self.sql("DELETE FROM ").quoted(table)
        return self

    def WHERE(self, **kwargs):
        self.sql(" WHERE ")
        for i, (k, v) in enumerate(kwargs.items()):
            self.sql(" AND " if i else "")
            self.quoted(k).sql("=").literal(v)
        return self

    def WHERE_CV(self, columns, *keys):
        self.sql(" WHERE ")
        if isinstance(columns, str):
            self.quoted(columns).sql(" IN (")
            for i, value in enumerate(keys):
                self.sql("," if i else "")
                self.literal(value)
            self.sql(")")
        else:
            for i, values in enumerate(keys):
                self.sql(" OR (" if i else "(")
                for j, (k, v) in enumerate(zip(columns, values)):
                    self.sql(" AND " if j else "")
                    self.quoted(k).sql("=").literal(v)
                self.sql(")")
        return self
