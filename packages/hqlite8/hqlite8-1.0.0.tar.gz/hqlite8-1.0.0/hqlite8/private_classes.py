from sqlite3 import Cursor


class SelectInstance:
    def __init__(self, cursor: Cursor, columns):
        self.c = cursor
        self.columns = columns

    def fetchone(self):
        original = self.c.fetchone()

        if original is None:
            return original

        if isinstance(self.columns, str):
            return original[0]
        else:
            return original

    def fetchall(self):
        # todo fix [('h',), ('h',)]

        original = self.c.fetchall()

        if not original:
            return original

        if len(original[0]) == 1:
            new = []

            for _tuple in original:
                new.append(_tuple[0])

            return new
        else:
            return original

    # todo add fetchmany
