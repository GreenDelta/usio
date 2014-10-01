"""
This script converts the BEA Make table to a CSV file: bea_make.csv.
"""

import csv
import xlrd

__MAKE_START_COMMODITY = 'Oilseed farming'
__MAKE_END_COMMODITY = 'Scrap'
__MAKE_START_INDUSTRY = 'Oilseed farming'
__MAKE_END_INDUSTRY = 'Other state and local government enterprises'


def main():
    workbook = xlrd.open_workbook('../data/bea2007/IOMake_After_Redefinitions_2007_Detail.xlsx')
    sheet = workbook.sheet_by_name('2007')
    col_range = get_column_range(sheet)
    row_range = get_row_range(sheet)
    print("convert make table to csv rows=%s columns=%s: " % (row_range, col_range))
    f = open('../csv_out/bea_make.csv', 'w', newline='\n')
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in row_range:
        for col in col_range:
            val = sheet.cell(row, col).value
            if (type(val) in [int, float]) and val != 0:
                entry = init_entry(row, col, sheet)
                entry.append(val)
                writer.writerow(entry)
    f.close()


def init_entry(row, col, sheet):
    ind_id_val = sheet.cell(row, 0).value
    ind_id = int(ind_id_val) if type(ind_id_val) == float else ind_id_val
    ind_name = sheet.cell(row, 1).value
    com_id_val = sheet.cell(5, col).value
    com_id = int(com_id_val) if type(com_id_val) == float else com_id_val
    com_name = sheet.cell(4, col).value
    return [str(ind_id), ind_name, str(com_id), com_name]


def get_column_range(sheet):
    start = -1
    end = -1
    row = 4
    i = 0
    while True:
        val = sheet.cell(row, i).value
        if start == -1 and val == __MAKE_START_COMMODITY:
            start = i
        if val == __MAKE_END_COMMODITY:
            end = i
            break
        i += 1
    return range(start, end+1)


def get_row_range(sheet):
    start = -1
    end = -1
    col = 1
    i = 0
    while True:
        val = sheet.cell(i, col).value
        if start == -1 and val == __MAKE_START_INDUSTRY:
            start = i
        if val == __MAKE_END_INDUSTRY:
            end = i
            break
        i += 1
    return range(start, end+1)

if __name__ == '__main__':
    main()