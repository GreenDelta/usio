import pipeline.bea2002 as bea
import pipeline.dr as dr
import pipeline.products as products


def execute(*transformations):
    for t in transformations:
        print(t.description())
        t.run()


class Bea2002MakeTransformation:

    def __init__(self, bea_make_file, csv_output_file):
        self.bea_make = bea_make_file
        self.csv_make = csv_output_file
        pass

    @classmethod
    def on(cls, bea_makefile):
        return Bea2002MakeTransformation(bea_makefile, None)

    def to(self, csv_output_file):
        self.csv_make = csv_output_file
        return self

    def description(self):
        return "convert BEA 2002 make matrix %s to CSV matrix %s" % (
            self.bea_make, self.csv_make)

    def run(self):
        bea.make_to_csv(self.bea_make, self.csv_make)


class Bea2002UseTransformation:

    def __init__(self, bea_use_file, csv_output_file):
        self.bea_use = bea_use_file
        self.csv_use = csv_output_file

    def description(self):
        return "convert BEA 2002 use matrix %s to CSV matrix %s" % (
            self.bea_use, self.csv_use)

    def run(self):
        bea.use_to_csv(self.bea_use, self.csv_use)


class TechMatrixTransformation:

    def __init__(self, make_csv_file, use_csv_file, dr_csv_file):
        self.make_csv = make_csv_file
        self.use_csv = use_csv_file
        self.dr_csv = dr_csv_file

    def description(self):
        return "calculate the DR coefficient matrix %s from %s and %s" % (
            self.dr_csv, self.make_csv, self.use_csv)

    def run(self):
        make_table = dr.read_sparse_matrix(self.make_csv)
        use_table = dr.read_sparse_matrix(self.use_csv)
        dr_matrix = dr.calculate_dr_coefficients(use_table, make_table)
        dr_matrix.write_sparse_csv(self.dr_csv)


class ProductExtractor:

    def __init__(self, tech_csv_file, category_json_file, out_csv_file):
        self.tech_csv = tech_csv_file
        self.cat_json = category_json_file
        self.out_csv = out_csv_file

    def description(self):
        return "extract product/sector information from %s to %s" % (
            self.tech_csv, self.out_csv)

    def run(self):
        products.make_product_table(self.tech_csv, self.cat_json, self.out_csv)