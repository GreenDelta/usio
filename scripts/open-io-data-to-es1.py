import json
from string import Template
import xlrd

techBook = xlrd.open_workbook('../data/open-io/DR Coefficients.xlsx')
techSheet = techBook.sheet_by_name('Data')
categories = json.load(open('../data/naics_categories.json'))

# number of sectors in the table
NUM = 430


def find_category(sector_code):
    for cat in categories:
        if not match_category_code(sector_code, cat['prefixes']):
            continue
        for subCat in cat['childs']:
            if match_category_code(sector_code, subCat['prefixes']):
                return cat['name'], subCat['name']


def match_category_code(code, prefixes):
    for p in prefixes:
        if code.startswith(p):
            return True
    return False


def sector_info(text):
    code, name = text.partition(' - ')[::2]
    return {'code': code, 'name': name}


def make_header(column_label):
    sector = sector_info(column_label)
    category = find_category(sector['code'])
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
    return template.substitute(name=sector['name'], category=category[0], subCategory=category[1])


def make_input(i, row_label, value):
    sector = sector_info(row_label)
    category = find_category(sector['code'])
    template = Template("""
            <exchange number="$i"
                category="$category"
                subCategory="$subCategory"
                name="$name"
                unit="USD"
                location="US"
                meanValue="$value"
                infrastructureProcess="false">
                <inputGroup>5</inputGroup>
            </exchange>""")
    return template.substitute(name=sector['name'], category=category[0],
                               subCategory=category[1], i=i, value=value)


def make_footer():
    return """
        </flowData>
    </dataset>
</ecoSpold>"""


for col in range(1, NUM+1):
    colLabel = techSheet.cell(0, col).value
    text = make_header(colLabel)
    for row in range(1, NUM+1):
        val = techSheet.cell(row, col).value
        if val == 0:
            continue
        rowLabel = techSheet.cell(row, 0).value
        text += make_input(row+1, rowLabel, val)

    text += make_footer()
    f = open('../out/%s.xml' % col, 'w')
    f.write(text)
    f.close()

