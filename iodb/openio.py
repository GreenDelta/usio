
import csv


def make_flow_table(satellite_csv, flow_csv):
    """
    Extracts the flow information from an OpenIO satellite matrix and writes
    this information into the given CSV file.

    TODO: mapping file + flow units

    :param satellite_csv: the file path to the OpenIO satellite matrix
    :param flow_csv: the file path to the CSV file where the flow information
        should be written
    """
    flows = _get_flows(satellite_csv)
    with open(flow_csv, "w", encoding="utf-8", newline="\n") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for key in flows:
            writer.writerow(flows[key])

def _get_flows(satellite_csv):
    flows = {}
    with open(satellite_csv, "r", encoding="utf-8", newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            key = row[1]
            if key in flows:
                continue
            flow = _make_flow(key)
            if flow is not None:
                flows[key] = flow
    return flows


def _make_flow(key):
    if key is None:
        return None
    values = [x.strip() for x in key.rsplit(',', 2)]
    if len(values) != 3:
        print("  ignored elementary flow: %s" % key)
        return None
    values.append("kg")
    values.append("output")
    return values