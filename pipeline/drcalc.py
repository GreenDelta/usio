import pipeline.indices as indices
import pipeline.csvmatrix as csvm
import numpy


def read_index(index_file):
    items = indices.read(index_file)
    idx = Index()
    for item in items:
        idx.add(item)
    return idx


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


def create_csv_matrix(array_matrix, row_index, col_index):
    rows, cols = array_matrix.shape
    csv_matrix = csvm.Matrix()
    for row in range(0, rows):
        for col in range(0, cols):
            val = array_matrix[row, col]
            if val == 0:
                continue
            row_key = row_index.key(row)
            col_key = col_index.key(col)
            csv_matrix.add_entry(row_key, col_key, val)
    return csv_matrix


class Index:
    def __init__(self):
        self.key_to_index = {}
        self.index_to_key = {}

    def size(self):
        return len(self.key_to_index)

    def add(self, key):
        idx = len(self.key_to_index)
        self.key_to_index[key] = idx
        self.index_to_key[idx] = key

    def index(self, key):
        return self.key_to_index[key]

    def key(self, idx):
        return self.index_to_key[idx]


if __name__ == '__main__':
    d = '../build/pipeline/'

    com_idx = read_index(d + 'commodities.csv')
    ind_idx = read_index(d + 'industries.csv')
    make_csv = csvm.read_sparse_csv(d + 'make.csv')
    use_csv = csvm.read_sparse_csv(d + 'use.csv')

    make = create_array_matrix(make_csv, ind_idx, com_idx)
    use = create_array_matrix(use_csv, com_idx, ind_idx)

    divide_by_col_sums(make)
    divide_by_col_sums(use)
    dr = numpy.dot(use, make)

    csv_dr = create_csv_matrix(dr, com_idx, com_idx)
    csv_dr.write_dense_csv(d + 'dr_dense.csv')

