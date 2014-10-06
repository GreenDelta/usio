"""
Converts the data from the OpenIO satellite matrix to CSV files.
"""

import csv
import xlrd
import utils.xls as xls


def main():
    workbook = xlrd.open_workbook('../data/open-io/Satellite xwalked.xlsx')
    sheet = workbook.sheet_by_name('Data')
    rows = xls.get_row_range(sheet, 'Carbon monoxide, Air, unspecified', 'Xylene, Soil, agricultural')
    cols = xls.get_column_range(sheet, '1111A0 - Oilseed farming', 'S00900 - Rest of the world adjustment')
    write_entries(sheet, rows, cols)
    write_flows(sheet, rows)


def write_entries(sheet, rows, cols):
    with open('../csv_out/oio_satellite_entries.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in get_entries(sheet, rows, cols):
            writer.writerow(row)


def get_entries(sheet, rows, cols):
    for row in rows:
        flow = sheet.cell(row, 0).value
        for col in cols:
            val = sheet.cell(row, col).value
            if xls.is_zero(val):
                continue
            sector = sheet.cell(0, col).value
            code = sector.partition(' - ')[0]
            yield [code, flow, val]


def write_flows(sheet, rows):
    with open('../csv_out/oio_satellite_flows.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in rows:
            flow = sheet.cell(row, 0).value
            values = [x.strip() for x in flow.rsplit(',', 2)]
            if len(values) != 3:
                print('ignored elementary flow: %s' % flow)
                continue
            values.insert(0, flow)
            values.append('kg')
            values.append('output')
            writer.writerow(values)


if __name__ == '__main__':
    main()