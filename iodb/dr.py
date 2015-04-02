import iodb.csvmatrix as csv
import numpy


def create_dr(make_csv_file, use_csv_file, dr_csv_file, scrap=None,
              value_added=[]):
    make_csv = csv.read_sparse_csv(make_csv_file)
    use_csv = csv.read_sparse_csv(use_csv_file)
    com_idx = create_combined_index(make_csv.col_keys, use_csv.row_keys)
    ind_idx = create_combined_index(make_csv.row_keys, use_csv.col_keys)
    make = create_array_matrix(make_csv, ind_idx, com_idx)
    use = create_array_matrix(use_csv, com_idx, ind_idx)
    divide_by_col_sums(make)
    divide_by_col_sums(use)

    # remove value added sectors
    removals = []
    for va in value_added:
        i = com_idx.index(va)
        if i > 0:
            com_idx.remove(va)
            removals.append(i)
    if len(removals) > 0:
        use = numpy.delete(use, removals, 0)
        make = numpy.delete(make, removals, 1)

    dr = numpy.dot(use, make)
    csv_dr = create_csv_matrix(dr, com_idx, com_idx)
    csv_dr.write_sparse_csv(dr_csv_file)


def create_array_matrix(csv_matrix, row_index, col_index):
    m = numpy.zeros((row_index.size(), col_index.size()))
    for entry in csv_matrix.entries():
        row = row_index.index(entry[0])
        col = col_index.index(entry[1])
        m[row][col] = entry[2]
    return m


def divide_by_col_sums(matrix):
    rows, cols = matrix.shape
    sums = numpy.sum(matrix, 0)  # column sums
    for col in range(0, cols):
        s = sums[col]
        if s == 0:
            continue
        for row in range(rows):
            matrix[row, col] = matrix[row, col] / s


def create_combined_index(keys1, keys2):
    items = combine_indices(keys1, keys2)
    idx = Index()
    for item in items:
        idx.add(item)
    return idx


def combine_indices(collection1, collection2):
    c = []
    for e1 in collection1:
        if e1 not in c:
            c.append(e1)
    for e2 in collection2:
        if e2 not in c:
            c.append(e2)
    c.sort()
    return c


def create_csv_matrix(array_matrix, row_index, col_index):
    rows, cols = array_matrix.shape
    csv_matrix = csv.Matrix()
    for row in range(0, rows):
        row_key = row_index.key(row)
        csv_matrix.add_row(row_key)
        for col in range(0, cols):
            col_key = col_index.key(col)
            if col == 0:
                csv_matrix.add_col(col_key)
            val = array_matrix[row, col]
            if val == 0:
                continue
            csv_matrix.add_entry(row_key, col_key, val)
    return csv_matrix


class Index:
    def __init__(self):
        self.keys = []
        self.idx = {}

    def size(self):
        return len(self.keys)

    def add(self, key):
        i = len(self.keys)
        self.keys.append(key)
        self.idx[key] = i

    def remove(self, key):
        if key not in self.keys:
            return
        i = self.idx[key]
        self.keys.remove(key)
        for j in range(i, len(self.keys)):
            old = self.idx[self.keys[i]]
            self.idx[self.keys[i]] = old - 1

    def index(self, key):
        if key not in self.idx:
            return -1
        return self.idx[key]

    def key(self, idx):
        return self.keys[idx]
