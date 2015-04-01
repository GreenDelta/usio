import pipeline.csvmatrix as matrix


def extract(csv_make_table, csv_use_table, commodity_file, industry_file):
    make = matrix.read_sparse_csv(csv_make_table)
    use = matrix.read_sparse_csv(csv_use_table)
    commodities = combine(make.col_keys, use.row_keys)
    industries = combine(make.row_keys, use.col_keys)
    with open(commodity_file, mode='w', newline='\n') as f:
        for c in commodities:
            f.write(c + '\n')
    with open(industry_file, mode='w', newline='\n') as f:
        for i in industries:
            f.write(i + '\n')


def read(index_file):
    index = []
    with open(index_file, 'r', newline='\n') as f:
        for i in f:
            if i not in index:
                index.append(i.strip())
    index.sort()
    return index


def combine(collection1, collection2):
    c = []
    for e1 in collection1:
        if e1 not in c:
            c.append(e1)
    for e2 in collection2:
        if e2 not in c:
            c.append(e2)
    c.sort()
    return c


def write_diff(list1, list2):
    c = combine(list1, list2)
    word_len = 1
    for e in c:
        word_len = max(len(e), word_len)
    word_len += 2

    for e in c:
        if (e in list1) and (e in list2):
            print('  %s %s' % (e.ljust(word_len), e.ljust(word_len)))
        elif e in list1:
            print('+ %s %s' % (e.ljust(word_len), '-'.ljust(word_len)))
        elif e in list2:
            print('- %s %s' % ('-'.ljust(word_len), e.ljust(word_len)))

