
import csv
from string import Template
import zipfile as zip
from xml.sax.saxutils import escape


def make_package(tech_csv, products_csv, sat_csv, flows_csv, zip_path):
    pack = zip.ZipFile(zip_path, mode='w', compression=zip.ZIP_DEFLATED)
    pack.writestr("test.xml", "<a></a>")
    products = _read_products(products_csv)
    flows = _read_flows(flows_csv)
    i = 0
    for product_key in products:
        text = ""
        text += _make_header(products[product_key])
        text += _make_inputs(_get_inputs(product_key, tech_csv), products)
        text += _make_interventions(_get_interventions(product_key, sat_csv),
                                    flows)
        text += _make_footer()
        pack.writestr("%s.xml" % i, text)
        i += 1


def _read_products(products_csv):
    products = {}
    with open(products_csv, mode='r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            products[row[0]] = row
    return products


def _read_flows(flows_csv):
    flows = {}
    with open(flows_csv, mode='r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            flows[row[0]] = row
    return flows


def _get_inputs(recipient_key, tech_csv):
    inputs = {}
    with open(tech_csv, mode='r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == recipient_key:
                inputs[row[0]] = float(row[2])
    return inputs


def _make_inputs(inputs, products):
    xml_part = ""
    template = Template("""
            <exchange number="$i"
                category="$category"
                subCategory="$sub_category"
                name="$name"
                unit="USD"
                location="US"
                meanValue="$value"
                infrastructureProcess="false">
                <inputGroup>5</inputGroup>
            </exchange>""")
    i = 2
    for key in inputs:
        product = products[key]
        xml_part += template.substitute(name=e(product[2]),
                                        category=e(product[3]),
                                        sub_category=e(product[4]),
                                        i=i, value=inputs[key])
        i += 1
    return xml_part


def _get_interventions(product_key, sat_csv):
    interventions = {}
    with open(sat_csv, mode='r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == product_key:
                interventions[row[1]] = float(row[2])
    return interventions


def _make_interventions(interventions, elem_flows):
    xml_part = ''
    template = Template("""
            <exchange number="$i"
                name="$name"
                category="$category"
                subCategory="$sub_category"
                unit="$unit"
                meanValue="$value">
                <$direction>4</$direction>
            </exchange>""")
    i = 1000
    for key in interventions:
        if key not in elem_flows:
            # print('ignored flow: %s' % key)
            continue
        flow = elem_flows[key]
        group = 'inputGroup' if flow[5] == 'input' else 'outputGroup'
        xml_part += template.substitute(i=i,
                                        name=e(flow[1]),
                                        value=interventions[key],
                                        category=e(flow[2]),
                                        sub_category=e(flow[3]),
                                        unit=flow[4],
                                        direction=group)
        i += 1
    return xml_part


def _make_header(product_info):
    template = Template("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ecoSpold xmlns="http://www.EcoInvent.org/EcoSpold01">
    <dataset number="1" timestamp="2014-09-30T10:00:00.000+02:00">
        <metaInformation>
            <processInformation>
                <referenceFunction
                    datasetRelatesToProduct="true"
                    name="$name"
                    infrastructureProcess="false"
                    amount="1.0"
                    unit="USD"
                    category="$category"
                    subCategory="$subCategory" />
                <geography location="US"/>
                <timePeriod dataValidForEntirePeriod="true">
                    <startDate>2002-01-01</startDate>
                    <endDate>2002-31-12</endDate>
                </timePeriod>
                <dataSetInformation type="1"
                    impactAssessmentResult="false"
                    timestamp="2014-09-30T10:00:00.000+02:00"
                    version="1.0" internalVersion="0.0" energyValues="0"/>
            </processInformation>
        </metaInformation>
        <flowData>
            <exchange number="1"
                category="$category"
                subCategory="$subCategory"
                name="$name"
                unit="USD"
                meanValue="1.0"
                location="US"
                infrastructureProcess="false">
                <outputGroup>0</outputGroup>
            </exchange>""")
    return template.substitute(name=e(product_info[2]),
                               category=e(product_info[3]),
                               subCategory=e(product_info[4]))


def _make_footer():
    return """
        </flowData>
    </dataset>
</ecoSpold>"""


def e(text):
    t = escape(text)
    return t.replace("’", "'")