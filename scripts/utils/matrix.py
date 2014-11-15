import csv


class Matrix:

    def __init__(self):
        self.row_index = {}
        self.col_index = {}
        self.values = {}

    @property
    def rows(self):
        return len(self.row_index)

    @property
    def cols(self):
        return len(self.col_index)

    def add_row(self, row_key):
        if row_key in self.row_index:
            return self.row_index[row_key]
        idx = len(self.row_index)
        self.row_index[row_key] = idx
        return idx

    def add_col(self, col_key):
        if col_key in self.col_index:
            return self.col_index[col_key]
        idx = len(self.col_index)
        self.col_index[col_key] = idx
        return idx

    def add_entry(self, row_key, col_key, value):
        if value is None:
            return 0
        v = float(value)
        if v == 0:
            return 0
        row = self.add_row(row_key)
        col = self.add_col(col_key)
        if not row in self.values:
            self.values[row] = {}
        self.values[row][col] = v
        return v

    def get_row_key(self, row):
        for key in self.row_index:
            if self.row_index[key] == row:
                return key
        return None

    def get_col_key(self, col):
        for key in self.col_index:
            if self.col_index[key] == col:
                return key
        return None

    def get_entry(self, row, col):
        r = row
        c = col
        if type(row) == str:
            r = self.row_index[row] if row in self.row_index else None
            c = self.col_index[col] if col in self.col_index else None
        if r is None or c is None:
            return 0
        if not r in self.values:
            return
        row_entries = self.values[r]
        return row_entries[col] if col in row_entries else 0

    @staticmethod
    def read_sparse_csv(file_path):
        m = Matrix()
        with open(file_path, 'r', newline='\n') as f:
            reader = csv.reader(f)
            for row in reader:
                m.add_entry(row[0], row[1], row[2])
        return m

    def write_dense_csv(self, file_path):
        with open(file_path, 'w', newline='\n') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            headers = ['']
            for col in range(0, self.cols):
                headers.append(self.get_col_key(col))
            writer.writerow(headers)
            for row in range(0, self.rows):
                entries = [self.get_row_key(row)]
                for col in range(0, self.cols):
                    entries.append(self.get_entry(row, col))
                writer.writerow(entries)