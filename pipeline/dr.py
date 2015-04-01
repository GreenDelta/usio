import pipeline.csvmatrix
from pipeline.csvmatrix import Matrix


def read_sparse_matrix(file_path):
    return pipeline.matrix.read_sparse_csv(file_path)


def calculate_dr_coefficients(use_table, make_table):
    """
    Calculates the direct requirement coefficients from the given use table and
    make table.

    TODO: there is currently no option for scrap adjustments included.

    :param use_table: The use table as commodity-by-industry matrix.
    :type use_table: Matrix
    :param make_table: The make table as industry-by-commodity matrix.
    :type make_table: Matrix
    :return: A commodity-by-commodity matrix with the direct requirement
             coefficients.
    """
    commodities = use_table.row_keys
    industries_use = use_table.col_keys
    industries_make = make_table.row_keys
    industries = []
    for ind in industries_use:
        if ind in industries_make:
            industries.append(ind)
    dr_table = calculate_dr_table(use_table)
    share_table = calculate_market_shares(make_table)
    dr_table = dr_table.filter(commodities, industries)
    share_table = share_table.filter(industries, commodities)
    return dr_table.mult(share_table)


def calculate_dr_table(use_table):
    """
    Calculates the direct requirement table from the given use table.

    :param use_table: The use table as commodity-by-industry matrix.
    :type use_table: Matrix
    :return: The direct requirement table as commodity-by-industry matrix
    """
    totals = use_table.get_col_sums()
    requirements = Matrix()
    for entry in use_table.entries():
        commodity = entry[0]
        industry = entry[1]
        total = totals[industry]
        dr = entry[2] / total
        requirements.add_entry(commodity, industry, dr)
    return requirements


def calculate_market_shares(make_table):
    """
    Calculates a matrix that contains the market shares from the given make
    table.

    :param make_table: The make table as industry-by-commodity matrix.
    :type make_table: Matrix
    :return: The market shares as industry-by-commodity matrix.
    """
    totals = make_table.get_col_sums()
    shares = Matrix()
    for entry in make_table.entries():
        industry = entry[0]
        commodity = entry[1]
        total = totals[commodity]
        share = entry[2] / total
        shares.add_entry(industry, commodity, share)
    return shares

