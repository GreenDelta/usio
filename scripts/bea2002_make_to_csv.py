"""
This script converts the make table from the BEA 2002 benchmark (IOMakeDetail.txt)
to the following CSV files:

* bea_make.csv: 1) industry code, 2) commodity code, 3) make value
* bea_commodities: 1) commodity code, 2) commodity name
* bea_industries: 1) industry code, 2) industry name

"""

import csv


def main():
    ind_codes = {}
    com_codes = {}
    with open('../csv_out/bea_make.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in get_rows():
            ind_codes[row[0]] = row[1]
            com_codes[row[2]] = row[3]
            v = float(row[4])
            if v == 0:
                continue
            values = [row[0], row[2], v]
            writer.writerow(values)
    write_codes('../csv_out/bea_industries.csv', ind_codes)
    write_codes('../csv_out/bea_commodities.csv', com_codes)


def write_codes(path, codes):
    keys = [key for key in codes.keys()]
    keys.sort()
    with open(path, 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for key in keys:
            row = [key, codes[key]]
            writer.writerow(row)

def get_rows():
    with open('../data/bea2002/IOMakeDetail.txt', 'r', newline='\n') as f:
        i = 0
        for line in f:
            if i >= 1 and len(line) > 0:
                yield parse_line(line)
            i += 1


def parse_line(line):
    values = []
    text = ''
    spaces = 0
    i = 0
    while i < len(line):
        char = line[i]
        if char == ' ':
            spaces += 1
        else:
            spaces = 0
        if spaces <= 1:
            text += line[i]
            i += 1
            continue
        else:
            values.append(text.strip())
            text = ''
            spaces = 0
            for k in range(i+1, len(line)):
                if line[k] != ' ':
                    i = k
                    break
    if len(text.strip()) > 0:
        values.append(text.strip())
    if len(values) == 5:
        # the last row in the make file has only one space between the value
        # and the year
        v = values[4]
        values.remove(v)
        val, year = v.partition(' ')[::2]
        values.append(val)
        values.append(year)
    return values


if __name__ == '__main__':
    main()