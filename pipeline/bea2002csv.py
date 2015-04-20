"""
This script converts the raw BEA 2002 make and use tables into the CSV matrix
format that can be processed by the iodb module. The BEA 2002 use and make
tables are provided in a fixed size table format:

use table:
(0, 10),     # commodity IO code
(10, 100),   # commodity description
(100, 110),  # industry IO code
(110, 200),  # industry description
(200, 210)   # use table value

make table:
(0, 10),     # industry IO code
(10, 100),   # industry description
(100, 110),  # commodity IO code
(110, 200),  # commodity description
(200, 210)   # make table value
"""

import csv


def read_lines(file_path):
    with open(file_path, 'r', newline='\n') as f:
        i = -1
        for line in f:
            i += 1
            if i == 0:
                continue  # ignore header
            yield line


def get_field_value(field, line):
    f = line[field[0]:field[1]]
    return f.strip()


def convert_table(raw_file, csv_file):
    fields = [
        (0, 10),     # row IO code
        (10, 100),   # row description
        (100, 110),  # column IO code
        (110, 200),  # column description
        (200, 210)   # table value
    ]
    with open(csv_file, 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for line in read_lines(raw_file):
            row_code = get_field_value(fields[0], line)
            row_name = get_field_value(fields[1], line)
            col_code = get_field_value(fields[2], line)
            col_name = get_field_value(fields[3], line)
            value = float(get_field_value(fields[4], line))
            row = get_identifier(row_code, row_name)
            col = get_identifier(col_code, col_name)
            writer.writerow([row, col, value])


def get_identifier(code, description):
    name = description
    if name.endswith('/1/'):
        name = name.replace('/1/', '').strip()
    return '%s - %s' % (code, name)
