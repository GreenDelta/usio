import pipeline.bea2002 as bea


def execute(*transformations):
    for t in transformations:
        print(t.description())
        t.run()


class Bea2002MakeTransformation:

    def __init__(self, bea_make_file, csv_output_file):
        self.bea_make = bea_make_file
        self.csv_make = csv_output_file
        pass

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