
from utils.matrix import Matrix

def print_matrix(m):
    for entry in m.entries():
        print(entry)

make_table = Matrix.read_sparse_csv('../example/make_table.csv')
use_table = Matrix.read_sparse_csv('../example/use_table.csv')

# calculate market shares
make_sums = make_table.get_col_sums()
share_table = Matrix()
for entry in make_table.entries():
    ind = entry[0]
    com = entry[1]
    val = entry[2]
    total = make_sums[com]
    share_table.add_entry(ind, com, val/total)
# print_matrix(share_table)

# calculate direct requirements
use_sums = use_table.get_col_sums()
dr_table = Matrix()
for entry in use_table.entries():
    com = entry[0]
    ind = entry[1]
    val = entry[2]
    total = use_sums[ind]
    dr_table.add_entry(com, ind, val/total)
#print_matrix(dr_table)

commodities_use = use_table.row_keys
commodities_make = make_table.col_keys
commodities = []
for com in commodities_use:
    if com in commodities_make:
        commodities.append(com)
commodities.sort()
print(commodities)

industries_use = use_table.col_keys
industries_make = make_table.row_keys
industries = []
for ind in industries_use:
    if ind in industries_make:
        industries.append(ind)
industries.sort()
print(industries)

dr_filtered = Matrix()
for entry in dr_table.entries():
    com = entry[0]
    ind = entry[1]
    val = entry[2]
    if com in commodities and ind in industries:
        dr_filtered.add_entry(com, ind, val)
# print_matrix(dr_filtered)

shares_filtered = Matrix()
for entry in share_table.entries():
    ind = entry[0]
    com = entry[1]
    val = entry[2]
    if com in commodities and ind in industries:
        shares_filtered.add_entry(ind, com, val)
#print_matrix(shares_filtered)

result = dr_filtered.mult(shares_filtered)
print_matrix(result)