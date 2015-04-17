import iodb.csvmatrix as csv
import numpy
from numpy.linalg import inv


def create_tr(drc_csv_file, tr_csv_file):
    drc_csv = csv.read_sparse_csv(drc_csv_file)
    idx = Index()
    for key in drc_csv.row_keys:
        if not idx.contains_key(key):
            idx.add(key)
    for key in drc_csv.col_keys:
        if not idx.contains_key(key):
            idx.add(key)
    drc = create_array_matrix(drc_csv, idx, idx)
    dim = idx.size()
    eye = numpy.eye(dim, dim)
    m = numpy.subtract(eye, drc)
    tr = inv(m)
    tr_csv = create_csv_matrix(tr, idx, idx)
    tr_csv.write_sparse_csv(tr_csv_file)


def create_drc(make_csv_file, use_csv_file, dr_csv_file, scrap=None,
               value_added=[]):

    # initialize the matrices
    make_csv = csv.read_sparse_csv(make_csv_file)
    use_csv = csv.read_sparse_csv(use_csv_file)
    com_idx = create_combined_index(make_csv.col_keys, use_csv.row_keys)
    ind_idx = create_combined_index(make_csv.row_keys, use_csv.col_keys)
    make = create_array_matrix(make_csv, ind_idx, com_idx)
    use = create_array_matrix(use_csv, com_idx, ind_idx)

    # calculate non-scrap ratios
    non_scrap_ratios = None
    if scrap is not None:
        scrap_idx = com_idx.index(scrap)
        if scrap_idx >= 0:
            non_scrap_ratios = calculate_non_scrap_ratios(make, scrap_idx)

    # calculate market shares and direct requirements
    divide_by_col_sums(make)
    divide_by_col_sums(use)

    # remove value added sectors
    removals = []
    for va in value_added:
        i = com_idx.index(va)
        if i >= 0:
            com_idx.remove(va)
            removals.append(i)
    if len(removals) > 0:
        use = numpy.delete(use, removals, 0)  # delete rows
        make = numpy.delete(make, removals, 1)  # delete columns

    # scrap adjustments
    if non_scrap_ratios is not None:
        apply_non_scrap_ratios(make, non_scrap_ratios)
        scrap_idx = com_idx.index(scrap)
        com_idx.remove(scrap)
        use = numpy.delete(use, scrap_idx, 0)
        make = numpy.delete(make, scrap_idx, 1)

    # calculate and write the direct requirement coefficients
    dr = numpy.dot(use, make)
    csv_dr = create_csv_matrix(dr, com_idx, com_idx)
    csv_dr.write_sparse_csv(dr_csv_file)


def apply_non_scrap_ratios(market_shares, non_scrap_ratios):
    rows, cols = market_shares.shape
    for row in range(0, rows):
        ratio = non_scrap_ratios[row]
        if ratio == 0:
            continue
        for col in range(0, cols):
            market_shares[row, col] = market_shares[row, col] / ratio


def calculate_non_scrap_ratios(make, scrap_idx):
    rows, cols = make.shape
    totals = numpy.zeros(rows)
    non_scrap_totals = numpy.zeros(rows)
    for row in range(0, rows):
        total = 0
        non_scrap_total = 0
        for col in range(0, cols):
            val = make[row, col]
            total += val
            if col != scrap_idx:
                non_scrap_total += val
        totals[row] = total
        non_scrap_totals[row] = non_scrap_total
    for row in range(0, rows):
        if totals[row] != 0:
            totals[row] = non_scrap_totals[row] / totals[row]
    return totals


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

    def contains_key(self, key):
        return self.index(key) >= 0
