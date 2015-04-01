"""
Provides methods for converting the BEA 2002 statistics file into the CSV
matrix format that is used for further data processing.
"""

import csv


def use_to_csv(bea_use, csv_use):
    """
    Converts the use table from the BEA 2002 statistics into a
    commodity-by-industry CSV matrix.  See the raw data file and the file
    information of the use table in the data folder.

    The resulting CSV file has the following columns:
    1) commodity
    2) industry
    3) value (producers' prices)
    """
    with open(csv_use, 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in _get_use_rows(bea_use):
            com_code = row['Commodity']
            com_name = row['CommodityDescription']
            ind_code = row['Industry']
            ind_name = row['IndustryDescription']
            val = float(row['ProVal'])
            row_key = "%s - %s" % (com_code, com_name)
            col_key = "%s - %s" % (ind_code, ind_name)
            writer.writerow([row_key, col_key, val])


def _get_use_rows(bea_use):
    with open(bea_use, 'r', newline='\n') as f:
        headers = None
        i = 0
        for line in f:
            if i == 0:
                headers = _parse_use_header(line)
            else:
                yield _parse_use_line(line, headers)
            i += 1


def _parse_use_header(line):
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


def _parse_use_line(line, headers):
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


def make_to_csv(bea_make, csv_make):
    """
    Converts the make table from the BEA 2002 statistics into a
    industry-by-commodity CSV matrix. See the raw data file and the file
    information of the make table in the data folder.

    The resulting CSV file has the following columns:

    1) The industry sectors which indicate the rows in the make table
    2) The commodities which are produced by the industries
    3) The amount of the respective commodity produced by the industry.
    """
    with open(csv_make, 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in _get_make_rows(bea_make):
            ind_code = row[0]
            ind_name = row[1]
            com_code = row[2]
            com_name = row[3]
            v = float(row[4])
            row_key = "%s - %s" % (ind_code, ind_name)
            col_key = "%s - %s" % (com_code, com_name)
            writer.writerow([row_key, col_key, v])


def _get_make_rows(bea_make):
    with open(bea_make, 'r', newline='\n') as f:
        i = 0
        for line in f:
            if i >= 1 and len(line) > 0:
                yield _parse_make_line(line)
            i += 1


def _parse_make_line(line):
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
