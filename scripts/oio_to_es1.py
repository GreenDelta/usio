
import csv
from string import Template
import utils.cattree as cattree
from xml.sax.saxutils import escape

def main():
    names = get_commodities()
    ctree = cattree.CategoryTree(open('../data/naics_categories.json'))
    elem_flows = get_elem_flows()
    make_totals = get_make_totals()
    for code in names.keys():
        name = names[code]
        category = ctree.get_category(code)
        xml = make_header(name, category)
        inputs = get_inputs(code)
        xml += make_inputs(inputs, names, ctree)
        interventions = get_interventions(code)
        xml += make_interventions(interventions, elem_flows)
        if code in make_totals.keys():
            material_inputs = get_material_inputs(code)
            xml += make_material_inputs(material_inputs, make_totals[code])
            waste_outputs = get_waste_outputs(code)
            xml += make_waste_outputs(waste_outputs, make_totals[code])
        else:
            print("code %s not in make table -> could not add materials" % code)
        xml += make_footer()
        f = open('../out/%s.xml' % code, 'w')
        f.write(xml)
        f.close()

def get_commodities():
    """
    :return: a map: commodity code -> commodity name
    """
    commodities = {}
    with f_open('oio_commodities.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            commodities[row[0]] = row[1]
    return commodities


def get_elem_flows():
    elem_flows = {}
    with f_open('oio_satellite_flows.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            key = row[0]
            flow = {'name': row[1],
                    'category': cattree.Category(row[2], row[3]),
                    'unit': row[4],
                    'direction': row[5]}
            elem_flows[key] = flow
    return elem_flows


def get_inputs(recipient_code):
    """
    :param recipient_code: the commodity code of the receiver
    :return: input values of other commodities as map: commodity -> value
    """
    inputs = {}
    with f_open('oio_dr_entries.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == recipient_code:
                inputs[row[0]] = float(row[2])
    return inputs


def get_interventions(code):
    interventions = {}
    with f_open('oio_satellite_entries.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                interventions[row[1]] = float(row[2])
    return interventions


def get_material_inputs(code):
    material_inputs = {}
    with f_open('wri_material_entries.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                material_inputs[row[1]] = float(row[2])
    return material_inputs


def get_waste_outputs(code):
    waste_outputs = {}
    with f_open('wri_waste_entries.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                waste_outputs[row[1]] = float(row[2])
    return waste_outputs


def get_make_totals():
    make_totals = {}
    with f_open('oio_make_totals_com.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            make_totals[row[0]] = float(row[1])
    return make_totals


def f_open(file_name):
    return open('../csv_out/' + file_name, 'r', newline='\n')


def make_header(name, category):
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
    return template.substitute(name=e(name),
                               category=e(category[0]),
                               subCategory=e(category[1]))


def make_inputs(inputs, names, ctree):
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
    for code in inputs.keys():
        name = names[code]
        category = ctree.get_category(code)
        value = inputs[code]
        xml_part += template.substitute(name=e(name),
                                        category=e(category[0]),
                                        sub_category=e(category[1]),
                                        i=i, value=value)
        i += 1
    return xml_part


def make_interventions(interventions, elem_flows):
    xml_part = ''
    template = Template("""
            <exchange number="$i"
                name="$name"
                category="$category"
                subCategory="$sub_category"
                unit="$unit"
                meanValue="$value">
                <outputGroup>4</outputGroup>
            </exchange>""")
    i = 1000
    for key in interventions.keys():
        if key not in elem_flows.keys():
            print('ignored flow: %s' % key)
            continue
        flow = elem_flows[key]
        category = flow['category']
        xml_part += template.substitute(i=i,
                                        name=e(flow['name']),
                                        value=interventions[key],
                                        category=e(category[0]),
                                        sub_category=e(category[1]),
                                        unit=flow['unit'])
        i += 1
    return xml_part


def make_material_inputs(material_inputs, total_dollars):
    xml_part = ""
    template = Template("""
            <exchange number="$i"
                category="$category"
                subCategory="$sub_category"
                name="$name"
                unit="kg"
                location="US"
                meanValue="$value"
                infrastructureProcess="false">
                <inputGroup>5</inputGroup>
            </exchange>""")
    i = 2000
    for material in material_inputs.keys():
        value = material_inputs[material] / total_dollars
        xml_part += template.substitute(name=e(material), category='WRI',
                                        sub_category='Materials', i=i, value=value)
        i += 1
    return xml_part


def make_waste_outputs(waste_inputs, total_dollars):
    xml_part = ""
    template = Template("""
            <exchange number="$i"
                category="$category"
                subCategory="$sub_category"
                name="$name"
                unit="kg"
                location="US"
                meanValue="$value"
                infrastructureProcess="false">
                <inputGroup>5</inputGroup>
            </exchange>""")
    i = 3000
    for waste in waste_inputs.keys():
        value = waste_inputs[waste] / total_dollars
        name = '%s, to waste treatment' % waste
        xml_part += template.substitute(name=e(name), category='WRI',
                                        sub_category='Wastes', i=i, value=value)
        i += 1
    return xml_part


def make_footer():
    return """
        </flowData>
    </dataset>
</ecoSpold>"""


def e(text):
    t = escape(text)
    return t.replace("’", "'")

if __name__ == '__main__':
    main()

