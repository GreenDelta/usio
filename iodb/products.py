import csv
import json


def make_product_table(dr_csv, category_json, product_csv):
    """
    Writes the product information of the given technology matrix and category
    tree to a CSV file.

    :param dr_csv: Path to the direct requirement coefficient file (sparse
        matrix in CSV format)
    :param category_json: Path to the category tree file (JSON format)
    :param product_csv: The path to the product table that should be created.
    """
    names = _read_product_names(dr_csv)
    tree = _read_category_tree(category_json)
    with open(product_csv, 'w', newline='\n') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for full_name in names:
            code, name = full_name.partition(" - ")[::2]
            cat = tree.get_category(code)
            writer.writerow([full_name, code, name, cat[0], cat[1], "USD"])


def _read_product_names(dr_csv):
    names = []
    with open(dr_csv, 'r', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] not in names:
                names.append(row[0])
            if row[1] not in names:
                names.append(row[1])
    names.sort()
    return names


def _read_category_tree(file_path):
    with open(file_path) as stream:
        return CategoryTree(stream)


class Category:

    def __init__(self, category, sub_category):
        self._category = category
        self._sub_category = sub_category

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def sub_category(self):
        return self._sub_category

    @sub_category.setter
    def sub_category(self, sub_category):
        self._sub_category = sub_category

    def __getitem__(self, item):
        if item == 0:
            return self.category
        elif item == 1:
            return self.sub_category
        else:
            return None

    def __str__(self):
        return "%s / %s" % (self.category, self.sub_category)


class CategoryTree:

    def __init__(self, stream):
        self.categories = json.load(stream)

    def get_category(self, sector_code):
        for cat in self.categories:
            if not CategoryTree.match_code(sector_code, cat['prefixes']):
                continue
            for subCat in cat['childs']:
                if CategoryTree.match_code(sector_code, subCat['prefixes']):
                    return Category(cat['name'], subCat['name'])
        return Category('Other', 'Other')

    @staticmethod
    def match_code(code, prefixes):
        for p in prefixes:
            if code.startswith(p):
                return True
        return False




