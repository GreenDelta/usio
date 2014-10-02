"""
This script converts the BEA Make table to a CSV file: bea_make.csv.
"""

import csv
import xlrd
import utils.xls as xls

__MAKE_START_COMMODITY = 'Oilseed farming'
__MAKE_END_COMMODITY = 'Scrap'
__MAKE_START_INDUSTRY = 'Oilseed farming'
__MAKE_END_INDUSTRY = 'Other state and local government enterprises'


def main():
    workbook = xlrd.open_workbook('../data/bea2007/IOMake_After_Redefinitions_2007_Detail.xlsx')
    sheet = workbook.sheet_by_name('2007')
    col_range = xls.get_column_range(sheet, __MAKE_START_COMMODITY, __MAKE_END_COMMODITY, 4)
    row_range = xls.get_row_range(sheet, __MAKE_START_INDUSTRY, __MAKE_END_INDUSTRY, 1)
    print("convert make table to csv rows=%s columns=%s: " % (row_range, col_range))
    f = open('../csv_out/bea_make.csv', 'w', newline='\n')
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in row_range:
        for col in col_range:
            val = sheet.cell(row, col).value
            if xls.is_zero(val):
                continue
            entry = init_entry(row, col, sheet)
            entry.append(val)
            writer.writerow(entry)
    f.close()


def init_entry(row, col, sheet):
    ind_id_val = sheet.cell(row, 0).value
    ind_id = xls.bea_code_str(ind_id_val)
    ind_name = sheet.cell(row, 1).value
    com_id_val = sheet.cell(5, col).value
    com_id = xls.bea_code_str(com_id_val)
    com_name = sheet.cell(4, col).value
    return [ind_id, ind_name, com_id, com_name]


if __name__ == '__main__':
    main()