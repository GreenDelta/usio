import pipeline as pipe

if __name__ == '__main__':

    # input data sources
    bea_make = 'data/bea2002/redef/IOMakeDetail.txt'
    bea_use = 'data/bea2002/redef/IOUseDetail.txt'
    categories = 'data/naics_categories.json'

    # (intermediate) outputs
    out_dir = 'build/pipeline/'
    make = out_dir + 'make.csv'
    use = out_dir + 'use.csv'
    tech = out_dir + 'tech.csv'
    products = out_dir + 'products.csv'

    pipe.execute(
        pipe.Bea2002MakeTransformation.on(bea_make).to(make),
        pipe.Bea2002UseTransformation(bea_use, use),
        pipe.TechMatrixTransformation(make, use, tech),
        pipe.ProductExtractor(tech, categories, products)
    )
