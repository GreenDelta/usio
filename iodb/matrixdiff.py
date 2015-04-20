import iodb


def create_report(matrix_a_csv, matrix_b_csv, report_file, title='',
                  epsilon=0.0000001):
    matrix_a = iodb.read_csv_matrix(matrix_a_csv)
    matrix_b = iodb.read_csv_matrix(matrix_b_csv)
    with open(report_file, 'w', encoding='utf-8') as writer:
        row_keys = [r for r in matrix_a.row_keys]
        row_keys.sort()
        col_keys = [c for c in matrix_a.col_keys]
        col_keys.sort()
        _write_header(title, epsilon, writer)
        _write_cells(matrix_a, matrix_b, writer, epsilon)
        writer.write('</svg></body></html>')


def _write_header(title, epsilon, writer):
    header = """<!DOCTYPE html>
<html>
<body>
<h2>%s</h2>
<h3>e = %s</h3>
""" % (title, epsilon)
    writer.write(header)


def _write_cells(matrix_a, matrix_b, writer, epsilon):
    row_keys = _get_keys(matrix_a.row_keys, matrix_b.row_keys)
    col_keys = _get_keys(matrix_a.col_keys, matrix_b.col_keys)
    height = len(row_keys) * 5
    width = len(col_keys) * 5
    svg = '<svg width="%s" height="%s">' % (width, height)
    writer.write(svg)
    row = 0
    for row_key in row_keys:
        col = 0
        for col_key in col_keys:
            val_a = matrix_a.get_entry(row_key, col_key)
            val_b = matrix_b.get_entry(row_key, col_key)
            color = ('rgb(140,255,140)' if abs(val_a - val_b) < epsilon
                     else 'rgb(255,140,140)')
            title = "%s :: %s :: a=%s b=%s" % (row_key, col_key, val_a, val_b)
            _write_rect(col * 5, row * 5, color, title, writer)
            col += 1
        row += 1


def _write_rect(x, y, color, title, writer):
    text = """
    <rect x="%s" y="%s" width="5" height="5" style="fill:%s;">
        <title>%s</title>
    </rect>""".strip() % (x, y, color, title)
    writer.write(text)


def _get_keys(keys_a, keys_b):
    keys = []
    keys.extend(keys_a)
    for k in keys_b:
        if k not in keys:
            keys.append(k)
    keys.sort()
    return keys