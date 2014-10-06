
import csv
import xlrd
import utils.xls as xls


def main():
    workbook = xlrd.open_workbook('../data/open-io/Raw Make Matrix.xlsx')
    sheet = workbook.sheet_by_name('Data')
    rows = xls.get_row_range(sheet, '1111A0 - Oilseed farming',
                             'S00700 - General state and local government services')
    cols = xls.get_column_range(sheet, '1111A0 - Oilseed farming',
                                'S00900 - Rest of the world adjustment')
    write_entries(sheet, rows, cols)


def write_entries(sheet, rows, cols):
    with open('../csv_out/oio_make.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for entry in get_entries(sheet, rows, cols):
            writer.writerow(entry)


def get_entries(sheet, rows, cols):
    code = lambda text: text.partition(' - ')[0]
    for row in rows:
        industry = sheet.cell(row, 0).value
        for col in cols:
            val = sheet.cell(row, col).value
            if xls.is_zero(val):
                continue
            commodity = sheet.cell(0, col).value
            yield [code(industry), code(commodity), val]

if __name__ == '__main__':
    main()