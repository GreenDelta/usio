"""
This script generates the CSV file for the elementary flow mapping from the
oio_flows_mapping_to_openlca.xlsx Excel file. The generated CSV file has the
following columns:

1) OpenIO full name
2) openLCA name
3) openLCA compartment
4) openLCA sub-compartment
5) openLCA unit
6) 'input' or 'output' depending on the flow direction

"""

import csv
import xlrd
import utils.xls as xls


def main():
    workbook = xlrd.open_workbook('../data/mappings/oio_flows_mapping_to_openlca.xlsx')
    sheet = workbook.sheet_by_name('flows_mapping')
    rows = xls.get_row_range(sheet, 'Land use III-IV, Raw, unspecified',
                             'Xylene, Soil, agricultural', col=1)
    with open('../csv_out/oio_olca_flow_mapping.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in rows:
            r = lambda col: sheet.cell(row, col).value
            olca_id = r(6)
            if olca_id.strip() == '':
                writer.writerow(create_unmapped(r))
            else:
                writer.writerow(create_mapped(r))


def create_unmapped(row):
    flow = [row(1),
            row(2),
            get_olca_compartment(row(3)),
            row(4),
            get_olca_unit(row(5)),
            get_direction(row)]
    return flow


def create_mapped(row):
    flow = [row(1),
            row(7),
            row(10),
            row(11),
            row(16),
            get_direction(row)]
    return flow


def get_olca_compartment(oio_compartment):
    if oio_compartment == 'Raw':
        return 'resource'
    else:
        return oio_compartment.lower()


def get_olca_unit(oio_unit):
    if oio_unit == 'Gallon':
        return 'gal (US liq)'
    else:
        return oio_unit


def get_direction(row):
    return 'input' if row(3) == 'Raw' else 'output'


if __name__ == '__main__':
    main()
