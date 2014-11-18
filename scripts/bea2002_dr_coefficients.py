import iodb

if __name__ == '__main__':
    make_table = iodb.read_sparse_matrix('../csv_out/bea2002_make.csv')
    use_table = iodb.read_sparse_matrix('../csv_out/bea2002_use.csv')
    coefficients = iodb.calculate_dr_coefficients(use_table, make_table)
    coefficients.write_dense_csv('../csv_out/bea2002_dr_coefficients.csv')

