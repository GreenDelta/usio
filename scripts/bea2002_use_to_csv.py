"""
This script converts the use table from the BEA 2002 benchmark (IOUseDetail.txt)
to a CSV file with the following columns:

1) commodity
2) industry
3) value (producers' prices)

"""

import csv


def main():
    with open('../csv_out/bea2002_use.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in get_rows():
            com_code = row['Commodity']
            com_name = row['CommodityDescription']
            ind_code = row['Industry']
            ind_name = row['IndustryDescription']
            val = float(row['ProVal'])
            if val != 0:
                row_key = "%s - %s" % (com_code, com_name)
                col_key = "%s - %s" % (ind_code, ind_name)
                writer.writerow([row_key, col_key, val])


def get_rows():
    with open('../data/bea2002/IOUseDetail.txt', 'r', newline='\n') as f:
        headers = None
        i = 0
        for line in f:
            if i == 0:
                headers = parse_header(line)
            else:
                yield parse_line(line, headers)
            i += 1


def parse_header(line):
    headers = []
    header = ''
    in_header = False
    start = -1
    for i in range(0, len(line)):
        c = line[i]
        if c == ' ' and in_header:
            headers.append((header.strip(), start))
            header = ''
            in_header = False
            start = -1
        if c != ' ':
            header += c
            if not in_header:
                in_header = True
                start = i
    return headers


def parse_line(line, headers):
    vals = {}
    for h in range(0, len(headers)):
        header = headers[h]
        start = header[1]
        if h < (len(headers) -1):
            end = headers[h+1][1]
            vals[header[0]] = line[start:end].strip()
        else:
            vals[header[0]] = line[start:].strip()
    return vals


if __name__ == '__main__':
    main()