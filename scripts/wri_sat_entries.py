import csv
import uuid


def calc_make_totals(make_csv):
    totals = {}
    with open(make_csv, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            commodity = row[1]
            val = float(row[2])
            if commodity not in totals:
                totals[commodity] = val
            else:
                totals[commodity] += val
    return totals


def write_sat_entries(material_entries, waste_entries, make_totals, sat_csv):
    with open(sat_csv, mode='w', encoding='utf-8', newline='\n') as sat:
        writer = csv.writer(sat)
        with open(material_entries, mode='r', encoding='utf-8') as mat:
            reader = csv.reader(mat)
            for row in reader:
                commodity = row[0]
                val = float(row[2])
                entry = val / make_totals[commodity]
                flow_id = str(uuid.uuid3(uuid.NAMESPACE_OID, "Flow/Material/"
                                         + row[1]))
                writer.writerow([commodity, flow_id, entry])
        with open(waste_entries, mode='r', encoding='utf-8') as was:
            reader = csv.reader(was)
            for row in reader:
                commodity = row[0]
                val = float(row[2])
                entry = val / make_totals[commodity]
                flow_id = str(uuid.uuid3(uuid.NAMESPACE_OID, "Flow/Waste/"
                                         + row[1]))
                writer.writerow([commodity, flow_id, entry])

if __name__ == '__main__':
    make_totals = calc_make_totals('../build/make_table.csv')
    write_sat_entries('../data/wri/material_entries.csv',
                      '../data/wri/waste_entries.csv',
                      make_totals,
                      '../build/wri_sat_entries.csv')

