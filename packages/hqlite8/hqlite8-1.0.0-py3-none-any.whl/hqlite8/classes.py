import sqlite3
from typing import Union
# import enums
from hqlite8 import private_classes


class Database:
    def __init__(self, path: str):
        self.db = sqlite3.connect(path)

    # def create(self, create_type: enums.CreateType):
    #     # todo finish
    #     pass

    def select(self, columns: Union[str, tuple, None], table: str, **kwargs):
        c = self.db.cursor()
        if isinstance(columns, str):
            item = columns
        elif isinstance(columns, tuple):
            item = ', '.join(map(str, columns))
        else:
            item = "*"

        if kwargs:
            it = list(kwargs)[0]
            where = f" where {it} = \"{kwargs[it]}\""
        else:
            where = ""

        c.execute(f"select {item} from {table}{where}")  # sorry but there's no way to do this with string connotation
        return private_classes.SelectInstance(c, columns)
