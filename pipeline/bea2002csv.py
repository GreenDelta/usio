"""
This script converts the raw BEA 2002 make and use tables into the CSV matrix
format that can be processed by the iodb module. The BEA 2002 use and make
tables are provided in a fixed size table format.
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


def convert_use_table(raw_file, csv_file):
    use_fields = [
        (0, 10),     # commodity IO code
        (10, 100),   # commodity description
        (100, 110),  # industry IO code
        (110, 200),  # industry description
        (200, 210)   # use table value
    ]
    with open(csv_file, 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for line in read_lines(raw_file):
            com_code = get_field_value(use_fields[0], line)
            com_name = get_field_value(use_fields[1], line)
            ind_code = get_field_value(use_fields[2], line)
            ind_name = get_field_value(use_fields[3], line)
            value = float(get_field_value(use_fields[4], line))
            commodity = '%s - %s' % (com_code, com_name)
            industry = '%s - %s' % (ind_code, ind_name)
            writer.writerow([commodity, industry, value])


def convert_make_table(raw_file, csv_file):
    make_fields = [
        (0, 10),     # industry IO code
        (10, 100),   # industry description
        (100, 110),  # commodity IO code
        (110, 200),  # commodity description
        (200, 210)   # make table value
    ]
    with open(csv_file, 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for line in read_lines(raw_file):
            ind_code = get_field_value(make_fields[0], line)
            ind_name = get_field_value(make_fields[1], line)
            com_code = get_field_value(make_fields[2], line)
            com_name = get_field_value(make_fields[3], line)
            value = float(get_field_value(make_fields[4], line))
            industry = '%s - %s' % (ind_code, ind_name)
            commodity = '%s - %s' % (com_code, com_name)
            writer.writerow([industry, commodity, value])
