import iodb.csvmatrix as csv
import iodb.req as req


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
    req.create_drc(make_csv_file, use_csv_file, dr_csv_file, scrap, value_added)


def create_tr_matrix(drc_csv_file, tr_csv_file):
    """
    Creates a total requirements matrix from the given direct requirements
    coefficient matrix and writes the result into a CSV file.

    :param drc_csv_file: The path to a CSV matrix file that contains the
    direct requirements coefficient matrix.
    :param tr_csv_file: The path to the CSV file where the resulting total
    requirements matrix should be written.
    """
    req.create_tr(drc_csv_file, tr_csv_file)