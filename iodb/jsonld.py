import csv
import json
import uuid
import zipfile as azip


class Ref:
    def __init__(self, schema_type, uuid, name=None):
        self.schema_type = schema_type
        self.uuid = uuid
        self.name = name

    def as_json(self):
        d = {"@type": self.schema_type, "@id": self.uuid}
        if self.name is not None:
            d["name"] = self.name
        return d


class RootEntity:
    def __init__(self):
        self.uuid = None
        self.name = None
        self.description = None

    def as_json(self):
        d = {
            "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
            "@type": self.__class__.__name__,
            "@id": self.uuid
        }
        if self.name is not None:
            d["name"] = self.name
        if self.description is not None:
            d["description"] = self.description
        return d


class Process(RootEntity):
    def __init__(self):
        super(Process, self).__init__()
        self.location = None

    def as_json(self):
        d = super(Process, self).as_json()
        if self.location is not None:
            d["location"] = self.location.as_json()
        return d


def make_package(tech_csv, products_csv, sat_csv):
    pass


def _read_products(products_csv):
    products = {}
    with open(products_csv, mode='r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            products[row[0]] = row
    return products


def _write_product_data(product_csv, pack):
    with open(product_csv, mode='r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            info = SectorInfo()
            name = row[2]
            info.name = name
            _write_categories(row[3], row[4], info)


def _write_categories(top_cat, sub_cat, info):
    tflow_id = uuid.uuid3(uuid.NAMESPACE_OID, "%s/%s" % (top_cat, "FLOW"))


def _write_category(name, model_type, pack, parent=None):
    id = uuid.uuid3(uuid.NAMESPACE_OID, "Category/%s/%s" % (name, model_type))
    c = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "Category",
        "name": name,
        "modelType": model_type
    }
    if parent is not None:
        c["parentCategory"] = {"@type": "Category", "@id": parent}
    path = "categories/%s.json" % id
    pack.writestr(path, json.dumps(c))
    print("write category %s" % path)
    return id


class SectorInfo:
    def __init__(self):
        self.name = None
        self.product_id = None
        self.process_id = None
        self.category_id = None




if __name__ == '__main__':

    pack = azip.ZipFile('../build/package.zip', mode='w',
                        compression=azip.ZIP_DEFLATED)
    # _write_product_data('../build/products.csv', pack)
    _write_category("buildings", "FLOW", pack)

    """
    p = Process()
    p.name = "Test"
    p.location = Ref("Location", "uuid")
    print(json.dumps(p.as_json()))
    """

