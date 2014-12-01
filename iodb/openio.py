"""
Provides methods for converting the tables from the OpenIO databases files to
CSV matrices.
"""
import csv
import xlrd
import iodb.xlsutils as xls


def make_to_csv(raw_make_xls, csv_file):
    """
    Converts the Excel file with the raw make matrix from the OpenIO technology
    module to a industry-by-commodity CSV matrix.
    """
    workbook = xlrd.open_workbook(raw_make_xls)
    sheet = workbook.sheet_by_name('Data')
    rows = xls.get_row_range(sheet, '1111A0 - Oilseed farming',
                             'S00700 - General state and local government services')
    cols = xls.get_column_range(sheet, '1111A0 - Oilseed farming',
                                'S00900 - Rest of the world adjustment')
    _write_entries(sheet, rows, cols, csv_file)


def use_to_csv(raw_use_xls, csv_file):
    """
    Converts the Excel file with the raw use matrix from the OpenIO technology
    module to a commodity-by-industry CSV matrix.
    """
    workbook = xlrd.open_workbook(raw_use_xls)
    sheet = workbook.sheet_by_name('Data')
    rows = xls.get_row_range(sheet, '1111A0 - Oilseed farming',
                             'S00202 - State and local government electric utilities')
    cols = xls.get_column_range(sheet, '1111A0 - Oilseed farming',
                                'S00401 - Scrap')
    _write_entries(sheet, rows, cols, csv_file)


def _write_entries(sheet, rows, cols, csv_file):
    with open(csv_file, 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for entry in _get_entries(sheet, rows, cols):
            writer.writerow(entry)


def _get_entries(sheet, rows, cols):
    for row in rows:
        row_key = sheet.cell(row, 0).value
        for col in cols:
            val = sheet.cell(row, col).value
            if xls.is_zero(val):
                continue
            col_key = sheet.cell(0, col).value
            yield [row_key, col_key, val]