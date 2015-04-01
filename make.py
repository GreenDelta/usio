import pipeline as pipe
import os

if __name__ == '__main__':

    # input data sources
    bea_make = 'data/bea2002/redef/IOMakeDetail.txt'
    bea_use = 'data/bea2002/redef/IOUseDetail.txt'
    categories = 'data/naics_categories.json'
    package_template = 'data/iodb_ref_flows_wri.zip'
    sat = 'data/satellite_matrix_olca_ref_flows_wri.csv'
    flows = 'data/olca_ref_flow_infos_wri.csv'

    # (intermediate) outputs
    out_dir = 'build/pipeline/'
    make = out_dir + 'make.csv'
    use = out_dir + 'use.csv'
    tech = out_dir + 'tech.csv'
    products = out_dir + 'products.csv'
    package = out_dir + 'iodb.zip'

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    pipe.execute(
        pipe.Bea2002MakeTransformation.of(bea_make).to(make),
        pipe.Bea2002UseTransformation.of(bea_use).to(use),
        #pipe.TechMatrixTransformation.of(make, use).to(tech),
        #pipe.ProductExtraction.of(tech, categories).to(products),
        #pipe.Copy.of(package_template).to(package),
        #pipe.JsonTransformation.of(tech, products, sat, flows).to(package)
    )
