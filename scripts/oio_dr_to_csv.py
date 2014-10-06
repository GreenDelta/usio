
import csv
import xlrd
import utils.xls as xls


def main():
    workbook = xlrd.open_workbook('../data/open-io/DR Coefficients.xlsx')
    sheet = workbook.sheet_by_name('Data')
    rows = xls.get_row_range(sheet, '1111A0 - Oilseed farming',
                             'S00202 - State and local government electric utilities')
    cols = xls.get_column_range(sheet, '1111A0 - Oilseed farming',
                                'S00202 - State and local government electric utilities')
    write_entries(sheet, rows, cols)
    write_commodities(sheet, rows)


def write_entries(sheet, rows, cols):
    with open('../csv_out/oio_dr_entries.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for entry in get_entries(sheet, rows, cols):
            writer.writerow(entry)


def get_entries(sheet, rows, cols):
    code = lambda sector: sector.partition(' - ')[0]
    for row in rows:
        provider = sheet.cell(row, 0).value
        for col in cols:
            val = sheet.cell(row, col).value
            if xls.is_zero(val):
                continue
            recipient = sheet.cell(col, 0).value
            yield [code(provider), code(recipient), val]


def write_commodities(sheet, rows):
    with open('../csv_out/oio_commodities.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in rows:
            com = sheet.cell(row, 0).value
            code, description = com.partition(' - ')[::2]
            writer.writerow([code, description])

if __name__ == '__main__':
    main()
