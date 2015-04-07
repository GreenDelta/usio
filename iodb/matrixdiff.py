import iodb


def create_report(matrix_a, matrix_b, report_file, epsilon=0.0000001):
    """
    :type matrix_a: iodb.matrix.Matrix
    :type matrix_b: iodb.matrix.Matrix
    """
    with open(report_file, 'w') as writer:
        row_keys = [r for r in matrix_a.row_keys]
        row_keys.sort()
        col_keys = [c for c in matrix_a.col_keys]
        col_keys.sort()
        height = len(row_keys) * 5
        width = len(col_keys) * 5
        _write_header(width, height, writer)
        _write_cells(row_keys, col_keys, matrix_a, matrix_b, writer, epsilon)
        writer.write('</svg></body></html>')


def _write_header(width, height, writer):
    header = """<!DOCTYPE html>
<html>
<body>
<svg width="%s" height="%s">
""" % (width, height)
    writer.write(header)


def _write_cells(row_keys, col_keys, matrix_a, matrix_b, writer, epsilon):
    row = 0
    for row_key in row_keys:
        col = 0
        for col_key in col_keys:
            val_a = matrix_a.get_entry(row_key, col_key)
            val_b = matrix_b.get_entry(row_key, col_key)
            if abs(val_a) < epsilon and abs(val_b) < epsilon:
                col += 1
                continue
            color = ('rgb(140,255,140)' if val_a - val_b < epsilon
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

