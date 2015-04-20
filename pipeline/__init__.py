import iodb
import pipeline.bea2002csv as bea
import pipeline.products as products
import pipeline.jsonld as jsonld
import shutil

import threading
import time
import sys


def execute(*transformations):
    for t in transformations:
        print(t.description())
        clock = make_clock_thread()
        clock.start()
        t.run()
        clock.stopped = True
        clock.join()


def make_clock_thread():

    class Clock(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.stopped = False

        def run(self):
            i = 0
            while not self.stopped:
                time.sleep(0.1)
                clock = ['|', '/', '-', '\\']
                c = i % 4
                if c == 0:
                    i = 1
                sys.stdout.write("\r%s" % clock[c])
                sys.stdout.flush()
                sys.stdout.write("\r")
                sys.stdout.flush()
                i += 1

    return Clock()


class Bea2002MakeTransformation:

    def __init__(self, bea_make_file, csv_output_file):
        self.bea_make = bea_make_file
        self.csv_make = csv_output_file
        pass

    @classmethod
    def of(cls, bea_makefile):
        return Bea2002MakeTransformation(bea_makefile, None)

    def to(self, csv_output_file):
        self.csv_make = csv_output_file
        return self

    def description(self):
        return "convert BEA 2002 make matrix %s to CSV matrix %s" % (
            self.bea_make, self.csv_make)

    def run(self):
        bea.convert_table(self.bea_make, self.csv_make)


class Bea2002UseTransformation:

    def __init__(self, bea_use_file, csv_output_file):
        self.bea_use = bea_use_file
        self.csv_use = csv_output_file

    @classmethod
    def of(cls, bea_use_file):
        return Bea2002UseTransformation(bea_use_file, None)

    def to(self, csv_output_file):
        self.csv_use = csv_output_file
        return self

    def description(self):
        return "convert BEA 2002 use matrix %s to CSV matrix %s" % (
            self.bea_use, self.csv_use)

    def run(self):
        bea.convert_table(self.bea_use, self.csv_use)


class TechMatrixTransformation:

    def __init__(self, make_csv_file, use_csv_file, dr_csv_file, scrap=None,
                 value_added=[]):
        self.make_csv = make_csv_file
        self.use_csv = use_csv_file
        self.dr_csv = dr_csv_file
        self.scrap = scrap
        self.value_added = value_added

    @classmethod
    def of(cls, make_csv_file, use_csv_file, scrap=None, value_added=[]):
        return TechMatrixTransformation(make_csv_file, use_csv_file, None,
                                        scrap=scrap, value_added=value_added)

    def to(self, dr_csv_file):
        self.dr_csv = dr_csv_file
        return self

    def description(self):
        return "calculate the DR coefficient matrix %s from %s and %s" % (
            self.dr_csv, self.make_csv, self.use_csv)

    def run(self):
        iodb.create_drc_matrix(self.make_csv, self.use_csv, self.dr_csv,
                               scrap=self.scrap, value_added=self.value_added)


class ProductExtraction:

    def __init__(self, tech_csv_file, category_json_file, out_csv_file):
        self.tech_csv = tech_csv_file
        self.cat_json = category_json_file
        self.out_csv = out_csv_file

    @classmethod
    def of(cls, tech_csv_file, category_json_file):
        return ProductExtraction(tech_csv_file, category_json_file, None)

    def to(self, out_csv_file):
        self.out_csv = out_csv_file
        return self

    def description(self):
        return "extract product/sector information from %s to %s" % (
            self.tech_csv, self.out_csv)

    def run(self):
        products.make_product_table(self.tech_csv, self.cat_json, self.out_csv)


class Copy:

    def __init__(self, from_file, to_file):
        self.from_file = from_file
        self.to_file = to_file

    @classmethod
    def of(cls, from_file):
        return Copy(from_file, None)

    def to(self, to_file):
        self.to_file = to_file
        return self

    def description(self):
        return "copy %s to %s" % (self.from_file, self.to_file)

    def run(self):
        shutil.copy(self.from_file, self.to_file)


class JsonTransformation:

    def __init__(self, tech_csv, products_csv, sat_csv, flows_csv, package_zip):
        self.tech_csv = tech_csv
        self.products_csv = products_csv
        self.sat_csv = sat_csv
        self.flows_csv = flows_csv
        self.package_zip = package_zip

    @classmethod
    def of(cls, tech_csv, products_csv, sat_csv, flows_csv):
        return JsonTransformation(tech_csv, products_csv, sat_csv, flows_csv,
                                  None)

    def to(self, package_zip):
        self.package_zip = package_zip
        return self

    def description(self):
        return "create JSON-LD package %s" % self.package_zip

    def run(self):
        jsonld.make_package(self.tech_csv, self.products_csv, self.sat_csv,
                            self.flows_csv, self.package_zip)
