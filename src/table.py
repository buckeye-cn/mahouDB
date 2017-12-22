class Table():
    """
    the database table

    self._table: the list containing all the values, each row is a dataset
    self._cols: the list containing all column names, i.e. ("id", "name")
    """

    def __init__(self, cols: list):
        """initialize an empty table with needed columns"""
        self._table = []
        self._cols = cols

    def add(self, row):
        """
        add a new row into the table

        row as list:
        add each data into the row according to the column order

        row as dict:
        add each pair into the table and column-data 
        """
        _row = [None] * len(self._cols)
        if isinstance(row, list):
            for i in range(min(len(self._cols), len(row))):
                _row[i] = row[i]
        elif isinstance(row, dict):
            for i, k in enumerate(self._cols):
                if k in row:
                    _row[i] = row[k]
        else:
            raise "row should be instance of list or map"
        self._table.append(tuple(_row))

    def find(self, col: str, value: str) -> list:
        """
        find all rows given the column string and value string

        return all corresponding rows appended as a list
        """
        i = self._cols.index(col)
        # TODO use index
        ret = []
        for r in self._table:
            if r[i] == value:
                ret.append(r)
        return ret

if __name__ == "__main__":
    table = Table(["id", "name"])
    table.add(["1", "liu"])
    table.add({"id": "2", "name": "wang"})
    table.add({"id": "2", "name": "wang1"})
    print(table.find("id", "2"))
