import iodb

if __name__ == '__main__':
    make_table = iodb.read_sparse_matrix('../data/example/make_table.csv')
    use_table = iodb.read_sparse_matrix('../data/example/use_table.csv')
    coefficients = iodb.calculate_dr_coefficients(use_table, make_table)
    for entry in coefficients.entries():
        print(entry)

