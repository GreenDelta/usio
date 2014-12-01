import iodb
import iodb.openio as oio


def dr_matrix_from_oio():
    # generate the make and use table from the Excel files
    oio.use_to_csv('../data/open-io/Raw Use Matrix.xlsx',
                   '../csv_out/oio_use.csv')
    oio.make_to_csv('../data/open-io/Raw Make Matrix.xlsx',
                    '../csv_out/oio_make.csv')
    make_table = iodb.read_sparse_matrix('../csv_out/oio_make.csv')
    use_table = iodb.read_sparse_matrix('../csv_out/oio_use.csv')
    coefficients = iodb.calculate_dr_coefficients(use_table, make_table)
    coefficients.write_dense_csv('../csv_out/oio_dr_calculated.csv')


def dr_matrix_from_example():
    make_table = iodb.read_sparse_matrix('../data/example/make_table.csv')
    use_table = iodb.read_sparse_matrix('../data/example/use_table.csv')
    coefficients = iodb.calculate_dr_coefficients(use_table, make_table)
    for entry in coefficients.entries():
        print(entry)


if __name__ == '__main__':
    dr_matrix_from_oio()

