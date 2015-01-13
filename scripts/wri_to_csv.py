
import csv
import xlrd
import utils.xls as xls


def main():
    path = '../data/wri/WRI to BEA02 Industry_030613.xlsx'
    workbook = xlrd.open_workbook(path)
    mat_sheet = workbook.sheet_by_name('WRI-to-BEA_MTL_2000')
    write_materials(mat_sheet)
    process_sheet(mat_sheet, 'wri_material_entries.csv')
    was_sheet = workbook.sheet_by_name('WRI-to-BEA_WST_2000')
    process_sheet(was_sheet, 'wri_waste_entries.csv')


def write_materials(sheet):
    cols = xls.get_column_range(sheet, 'Abrasives (Manufactured)', 'Zirconium', 6)
    names = []
    for col in cols:
        name = sheet.cell(6, col).value
        names.append(name)
    with open('../csv_out/wri_materials.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for name in names:
            writer.writerow([name, 'product'])


def process_sheet(sheet, file_name):
    rows = xls.get_row_range(sheet, 'Oilseed farming', 'Rest of the world adjustment', 1)
    cols = xls.get_column_range(sheet, 'Abrasives (Manufactured)', 'Zirconium', 6)
    entries = []
    for row in rows:
        for col in cols:
            val = sheet.cell(row, col).value
            if xls.is_zero(val):
                continue
            code = sheet.cell(row, 0).value
            sec_name = sheet.cell(row, 1).value
            sector = "%s - %s" % (code, sec_name)
            material = sheet.cell(6, col).value
            entries.append((sector, material, val))
    write_entries(entries, file_name)


def write_entries(entries, file_name):
    with open('../csv_out/' + file_name, 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for entry in entries:
            row = [xls.bea_code_str(entry[0]), entry[1], entry[2]]
            writer.writerow(row)

if __name__ == '__main__':
    main()