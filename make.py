import pipeline as pipe
import os

if __name__ == '__main__':

    # prepare the output directory
    build_dir = 'build'
    pipe_dir = 'build/pipe'
    if not os.path.exists(pipe_dir):
        os.makedirs(pipe_dir)

    # input data sources
    bea_make = 'data/bea2002/redef/IOMakeDetail.txt'
    bea_use = 'data/bea2002/redef/IOUseDetail.txt'

    categories = 'data/naics_categories.json'
    package_template = 'data/usio_ref_flows_wri.zip'
    sat = 'data/satellite_matrix/satellite_matrix_olca_ref_flows_wri.csv'
    flows = 'data/satellite_matrix/olca_ref_flow_infos_wri.csv'

    # (intermediate) outputs
    make = pipe_dir + '/make.csv'
    use = pipe_dir + '/use.csv'
    tech = pipe_dir + '/tech.csv'
    products = pipe_dir + '/products.csv'

    scrap = 'S00401 - Scrap'
    value_added = [
        'V00100 - Compensation of employees',
        'V00200 - Taxes on production and imports, less subsidies',
        'V00300 - Gross operating surplus'
    ]

    # no scrap adjustments but removal of value added sectors
    package = build_dir + '/usio_withScrap_vaRemoved.zip'
    pipe.execute(
        pipe.Bea2002MakeTransformation.of(bea_make).to(make),
        pipe.Bea2002UseTransformation.of(bea_use).to(use),
        pipe.TechMatrixTransformation.of(make, use,
                                         value_added=value_added).to(tech),
        pipe.ProductExtraction.of(tech, categories).to(products),
        pipe.Copy.of(package_template).to(package),
        pipe.JsonTransformation.of(tech, products, sat, flows).to(package)
    )
