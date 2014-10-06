"""
This script converts the use table from the BEA 2002 benchmark (IOUseDetail.txt)
to the following CSV files:

* bea_use.csv: 1) industry code, 2) commodity code, 3) use value

"""

import csv


def main():
    with open('../csv_out/bea_use.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in get_rows():
            val = float(row['ProVal'])
            if val != 0:
                values = [row['Industry'], row['Commodity'], val]
                writer.writerow(values)


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


if __name__ == '__main__':
    main()