import iodb.csvmatrix as csv
import iodb.drc as drc


def read_csv_matrix(file_path):
    return csv.read_sparse_csv(file_path)


def create_drc_matrix(make_csv_file, use_csv_file, dr_csv_file, scrap=None,
                      value_added=[]):
    """
    Creates a direct requirement coefficient matrix from the given use and make
    tables and writes the result into a CSV file.

    :param use_csv_file: The path to a CSV matrix file of the use table.
    :param make_csv_file: The path to a CSV matrix file of the make table.
    :param dr_csv_file: The path to the file to which the direct requirement
    matrix should be written.
    :param scrap: An optional identifier of the scrap sector for scrap
    adjustments.
    :param value_added: An optional list of value added sectors that should be
    removed.
    """
    drc.create_drc(make_csv_file, use_csv_file, dr_csv_file, scrap, value_added)


