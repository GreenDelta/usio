import csv
import json
import uuid
import zipfile as azip


def make_package(tech_csv, product_csv, zip_path):
    pack = azip.ZipFile(zip_path, mode='w', compression=azip.ZIP_DEFLATED)
    _write_categories(product_csv, pack)
    _write_economic_units(pack)
    _write_products(product_csv, pack)
    with open(product_csv, mode='r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            uid = str(uuid.uuid3(uuid.NAMESPACE_OID, "Process/" + row[0]))
            p = init_process(row)
            path = "processes/%s.json" % uid
            print("write process %s" % path)
            pack.writestr(path, json.dumps(p))


def init_process(row):
    uid = str(uuid.uuid3(uuid.NAMESPACE_OID, "Process/" + row[0]))
    cat_id = get_category_id("PROCESS", row[4], row[3])
    flow_id = str(uuid.uuid3(uuid.NAMESPACE_OID, "Flow/" + row[0]))
    p = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "Process",
        "@id": uid,
        "name": row[2],
        "processTyp": "UNIT_PROCESS",
        "category": {"@type": "Category", "@id": cat_id},
        "processDocumentation": {"copyright": False},
        "exchanges": [
            {
                "@type": "Exchange",
                "avoidedProduct": False,
                "input": False,
                "amount": 1.0,
                "flow": {"@type": "Flow", "@id": flow_id},
                "unit": {
                    "@type": "Unit",
                    "@id": "3f90ee51-c78b-4b15-a693-e7f320c1e894"
                },
                "flowProperty": {
                    "@type": "FlowProperty",
                    "@id": "b0682037-e878-4be4-a63a-a7a81053a691"
                },
                "quantitativeReference": True
            }
        ]
    }
    return p


def _write_products(product_csv, pack):
    with open(product_csv, mode='r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            uid = str(uuid.uuid3(uuid.NAMESPACE_OID, "Flow/" + row[0]))
            cat_id = get_category_id("FLOW", row[4], row[3])
            flow = {
                "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
                "@type": "Flow",
                "@id": uid,
                "name": row[2],
                "category": {"@type": "Category", "@id": cat_id},
                "flowType": "PRODUCT_FLOW",
                "flowProperties": [
                    {
                        "@type": "FlowPropertyFactor",
                        "referenceFlowProperty": True,
                        "conversionFactor": 1.0,
                        "flowProperty": {
                            "@type": "FlowProperty",
                            "@id": "b0682037-e878-4be4-a63a-a7a81053a691"
                        }}]
            }
            path = "flows/%s.json" % uid
            print("write flow %s" % path)
            pack.writestr(path, json.dumps(flow))


def _write_categories(product_csv, pack):
    categories = []
    with open(product_csv, mode='r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            top = row[3]
            sub = row[4]
            top_flow = get_category_id("FLOW", top)
            if top_flow not in categories:
                _write_category("FLOW", top, pack)
                categories.append(top_flow)
            sub_flow = get_category_id("FLOW", sub, top)
            if sub_flow not in categories:
                _write_category("FLOW", sub, pack, top)
                categories.append(sub_flow)
            top_proc = get_category_id("PROCESS", top)
            if top_proc not in categories:
                _write_category("PROCESS", top, pack)
                categories.append(top_proc)
            sub_proc = get_category_id("PROCESS", sub, top)
            if sub_proc not in categories:
                _write_category("PROCESS", sub, pack, top)
                categories.append(sub_proc)


def _write_category(model_type, name, pack, parent_name=None):
    uid = get_category_id(model_type, name, parent_name)
    c = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "Category",
        "@id": uid,
        "name": name,
        "modelType": model_type
    }
    if parent_name is not None:
        parent_id = get_category_id(model_type, parent_name)
        c["parentCategory"] = {"@type": "Category", "@id": parent_id}
    path = "categories/%s.json" % uid
    pack.writestr(path, json.dumps(c))
    print("write category %s" % path)
    return uid


def get_category_id(model_type, name, parent_name=None):
    n = name
    if parent_name is not None:
        n = parent_name + "/" + n
    return str(uuid.uuid3(uuid.NAMESPACE_OID,
                          "Category/%s/%s" % (n, model_type)))


def _write_economic_units(pack):
    ug = {"@context": "http://greendelta.github.io/olca-schema/context.jsonld",
          "@type": "UnitGroup",
          "@id": "5df2915b-186f-4773-9ef4-04baca5e56a9",
          "name": "Units of currency 2002",
          "units": [{"@type": "Unit",
                     "@id": "3f90ee51-c78b-4b15-a693-e7f320c1e894",
                     "name": "USD",
                     "referenceUnit": True,
                     "conversionFactor": 1.0
                     }]}
    ug = json.dumps(ug)
    pack.writestr("unit_groups/5df2915b-186f-4773-9ef4-04baca5e56a9.json", ug)
    fp = {"@context": "http://greendelta.github.io/olca-schema/context.jsonld",
          "@type": "FlowProperty",
          "@id": "b0682037-e878-4be4-a63a-a7a81053a691",
          "name": "Market value US 2002",
          "flowPropertyType": "ECONOMIC_QUANTITY",
          "unitGroup": {
              "@type": "UnitGroup",
              "@id": "5df2915b-186f-4773-9ef4-04baca5e56a9"
          }}
    fp = json.dumps(fp)
    pack.writestr("flow_properties/b0682037-e878-4be4-a63a-a7a81053a691.json",
                  fp)


if __name__ == '__main__':
    make_package("../build/dr_coefficients.csv",
                 "../build/products.csv", '../build/package.zip')


