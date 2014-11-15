from utils.matrix import Matrix
import csv


def main():
    m = Matrix.read_sparse_csv('../csv_out/bea2002_make.csv')
    sums = m.get_col_sums()
    with open('../csv_out/bea2002_market_shares.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for entry in m.entries():
            row_key = entry[0]
            col_key = entry[1]
            val = entry[2]
            total = sums[col_key]
            dr = val / total
            writer.writerow([row_key, col_key, dr])


if __name__ == '__main__':
    main()
