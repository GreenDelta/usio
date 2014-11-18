
from utils.matrix import Matrix

use_table = Matrix.read_sparse_csv('../csv_out/bea2002_use.csv')
make_table = Matrix.read_sparse_csv('../csv_out/bea2002_make.csv')

print('use table: %s x %s' % (use_table.rows, use_table.cols))
print('make table: %s x %s' % (make_table.rows, use_table.cols))

commodities_use = use_table.row_keys
commodities_make = make_table.col_keys
commodities = []
for com in commodities_use:
    # if com in commodities_make:
    commodities.append(com)
commodities.sort()

industries_use = use_table.col_keys
industries_make = make_table.row_keys
industries = []
for ind in industries_use:
    if ind in industries_make:
        industries.append(ind)
industries.sort()

dr_table = Matrix.read_sparse_csv('../csv_out/bea2002_dr_table.csv')
dr_filtered = Matrix()
for entry in dr_table.entries():
    com = entry[0]
    ind = entry[1]
    val = entry[2]
    if com in commodities and ind in industries:
        dr_filtered.add_entry(com, ind, val)

print('dr filtered: %s x %s' % (dr_filtered.rows, dr_filtered.cols))

shares = Matrix.read_sparse_csv('../csv_out/bea2002_market_shares.csv')
shares_filtered = Matrix()
for entry in shares.entries():
    ind = entry[0]
    com = entry[1]
    val = entry[2]
    if com in commodities and ind in industries:
        shares_filtered.add_entry(ind, com, val)

print('shares filtered: %s x %s' % (shares_filtered.rows, shares_filtered.cols))

result = dr_filtered.mult(shares_filtered)

result.write_dense_csv('../csv_out/bea2002_dr_coefficients.csv')