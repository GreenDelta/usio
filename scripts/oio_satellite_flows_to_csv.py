"""
Reads the elementary flows from the OpenIO satellite matrix and writes them to
the CSV file: oio_satellite_flows.csv.
"""

import csv
import xlrd
import utils.xls as xls


def main():
    workbook = xlrd.open_workbook('../data/open-io/Satellite xwalked.xlsx')
    sheet = workbook.sheet_by_name('Data')
    rows = xls.get_row_range(sheet, 'Carbon monoxide, Air, unspecified', 'Xylene, Soil, agricultural')
    write_flows(sheet, rows)


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
            # TODO: we need the unit and flow direction for the openLCA database
            # currently we use the following defaults: unit=kg, direction=output
            """
            values.append('kg')
            values.append('output')
            """
            writer.writerow(values)

if __name__ == '__main__':
    main()