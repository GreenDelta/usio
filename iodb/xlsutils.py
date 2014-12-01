"""
This module contains some utility functions for reading Excel files using the xlrd
module.
"""


def get_column_range(sheet, start_value, end_value, row=0, limit=32000):
    """
    Search for the indices of the columns with the given start and end value
    in the given Excel sheet and return a range beginning at the start index
    and including the end index.

    :param sheet: the Excel sheet (instance from the xlrd module)
    :param start_value: the cell value that indicates the start of the range
    :param end_value: the cell value that indicates the end of the range (inclusively)
    :param row: the row where the start and end values should be searched (default is 0)
    :param limit: the maximum size of the range (default is 32000)
    :return: a range(start_index, end_index+1)
    """
    start = -1
    end = -1
    i = 0
    while True:
        val = sheet.cell(row, i).value
        if start == -1 and val == start_value:
            start = i
        if val == end_value:
            end = i
            break
        if i >= limit:
            if start == -1:
                start = 0
            end = i
            break
        i += 1
    return range(start, end + 1)


def get_row_range(sheet, start_value, end_value, col=0, limit=32000):
    start = -1
    end = -1
    i = 0
    while True:
        val = sheet.cell(i, col).value
        if start == -1 and val == start_value:
            start = i
        if val == end_value:
            end = i
            break
        if i >= limit:
            if start == -1:
                start = 0
            end = i
        i += 1
    return range(start, end + 1)


def is_zero(value):
    """
    Returns true if the given cell value is numerically zero (0).

    :param value: the cell value
    :return: True if the cell value is a 0 or if the cell value is not a number;
    otherwise False
    """
    if type(value) not in [int, float]:
        return True
    return True if value == 0 else False


def bea_code_str(value):
    if type(value) is str:
        return value
    if type(value) is float:
        return str(int(value))
    else:
        return str(value)