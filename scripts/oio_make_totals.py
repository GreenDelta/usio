
import csv


def main():
    ind_totals = {}
    com_totals = {}
    with open('../csv_out/oio_make.csv', 'r', newline='\n') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            val = row[2]
            ind_id = row[0]
            put_value(ind_totals, ind_id, val)
            com_id = row[1]
            put_value(com_totals, com_id, val)
    write_totals(ind_totals, 'oio_make_totals_ind.csv')
    write_totals(com_totals, 'oio_make_totals_com.csv')


def put_value(totals, key, value):
    if not key in totals.keys():
        totals[key] = value
    else:
        totals[key] = totals[key] + value


def write_totals(totals, file_name):
    with open('../csv_out/' + file_name, "w", newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for key in totals.keys():
            writer.writerow([key, totals[key]])


if __name__ == '__main__':
    main()