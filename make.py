import pipeline as pipe

if __name__ == '__main__':

    # input data sources
    bea_make = 'data/bea2002/redef/IOMakeDetail.txt'
    bea_use = 'data/bea2002/redef/IOUseDetail.txt'

    # (intermediate) outputs
    out_dir = 'build/pipeline/'
    make = out_dir + 'make.csv'
    use = out_dir + 'use.csv'

    pipe.execute(
        pipe.Bea2002MakeTransformation(bea_make, make),
        pipe.Bea2002UseTransformation(bea_use, use)
    )
