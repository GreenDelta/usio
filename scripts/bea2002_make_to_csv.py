"""
This script converts the make table from the BEA 2002 benchmark (IOMakeDetail.txt)
to a CSV file with the following columns:

1) The industry sectors which indicate the rows in the make table
2) The commodities which are produced by the industries
3) The amount of the respective commodity produced by the industry.

"""

import csv


def main():
    with open('../csv_out/bea2002_make.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in get_rows():
            ind_code = row[0]
            ind_name = row[1]
            com_code = row[2]
            com_name = row[3]
            v = float(row[4])
            if v == 0:
                continue
            row_key = "%s - %s" % (ind_code, ind_name)
            col_key = "%s - %s" % (com_code, com_name)
            writer.writerow([row_key, col_key, v])


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