"""
Append the WRI flows to the JSON-LD package
"""
import csv
import json
import shutil
import zipfile as azip
import uuid


def add_categories(pack):
    top = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "Category",
        "@id": "b99e1786-aa68-4588-b9aa-ccca6168c964",
        "name": "WRI",
        "modelType": "FLOW"
    }
    pack.writestr("categories/b99e1786-aa68-4588-b9aa-ccca6168c964.json",
                  json.dumps(top))
    w = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "Category",
        "@id": "2a59b331-3e76-4263-84bb-e03b30ebbd11",
        "name": "Wastes",
        "modelType": "FLOW",
        "parentCategory": {
            "@type": "Category",
            "@id": "b99e1786-aa68-4588-b9aa-ccca6168c964"
        }
    }
    pack.writestr("categories/2a59b331-3e76-4263-84bb-e03b30ebbd11.json",
                  json.dumps(w))
    m = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "Category",
        "@id": "41a15ac3-7a9f-4fb1-8ff4-366702e31e50",
        "name": "Materials",
        "modelType": "FLOW",
        "parentCategory": {
            "@type": "Category",
            "@id": "b99e1786-aa68-4588-b9aa-ccca6168c964"
        }
    }
    pack.writestr("categories/41a15ac3-7a9f-4fb1-8ff4-366702e31e50.json",
                  json.dumps(m))


def create_waste_flow(name, pack):
    uid = str(uuid.uuid3(uuid.NAMESPACE_OID, "Flow/Waste/" + name))
    f = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "Flow",
        "@id": uid,
        "name": name,
        "category": {
            "@type": "Category",
            "@id": "2a59b331-3e76-4263-84bb-e03b30ebbd11",
        },
        "flowType": "ELEMENTARY_FLOW",
        "flowProperties": [
            {
                "@type": "FlowPropertyFactor",
                "referenceFlowProperty": True,
                "conversionFactor": 1.0,
                "flowProperty": {
                    "@type": "FlowProperty",
                    "@id": "93a60a56-a3c8-11da-a746-0800200b9a66"
                }
            }]
    }
    pack.writestr("flows/%s.json" % uid, json.dumps(f))


def create_material_flow(name, pack):
    uid = str(uuid.uuid3(uuid.NAMESPACE_OID, "Flow/Material/" + name))
    f = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "Flow",
        "@id": uid,
        "name": name,
        "category": {
            "@type": "Category",
            "@id": "41a15ac3-7a9f-4fb1-8ff4-366702e31e50",
        },
        "flowType": "ELEMENTARY_FLOW",
        "flowProperties": [
            {
                "@type": "FlowPropertyFactor",
                "referenceFlowProperty": True,
                "conversionFactor": 1.0,
                "flowProperty": {
                    "@type": "FlowProperty",
                    "@id": "93a60a56-a3c8-11da-a746-0800200b9a66"
                }
            }]
    }
    pack.writestr("flows/%s.json" % uid, json.dumps(f))


def write_flow_infos(flows, csv_path):
    with open(csv_path, mode='w', encoding='utf-8', newline='\n') as f:
        writer = csv.writer(f)
        for flow in flows:
            was_uid = str(uuid.uuid3(uuid.NAMESPACE_OID, "Flow/Waste/" + flow))
            mat_uid = str(uuid.uuid3(uuid.NAMESPACE_OID, "Flow/Material/" + flow))
            writer.writerow([was_uid, "output",
                             "20aadc24-a391-41cf-b340-3e4529f44bde",
                             "93a60a56-a3c8-11da-a746-0800200b9a66"])
            writer.writerow([mat_uid, "input",
                             "20aadc24-a391-41cf-b340-3e4529f44bde",
                             "93a60a56-a3c8-11da-a746-0800200b9a66"])


if __name__ == '__main__':
    zip_path = "../build/iodb_ref_flows_wri.zip"
    shutil.copy("../data/iodb_ref_flows.zip", zip_path)
    pack = azip.ZipFile(zip_path, mode='a', compression=azip.ZIP_DEFLATED)
    add_categories(pack)
    flows = []
    with open('../data/wri/flows.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            flows.append(row[0])
            create_waste_flow(row[0], pack)
            create_material_flow(row[0], pack)
    write_flow_infos(flows, "../csv_out/wri_flow_infos.csv")

