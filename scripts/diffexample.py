# This is a small example for using the matrix diff tool

import pipeline as pipe
import iodb.matrixdiff as diff
import os

if __name__ == '__main__':

    # prepare the output directory
    build_dir = '../build'
    pipe_dir = '../build/pipe'
    if not os.path.exists(pipe_dir):
        os.makedirs(pipe_dir)

    make_raw = '../data/bea2002/no_redef/REV_NAICSMakeDetail 4-24-08.txt'
    make_redef_raw = '../data/bea2002/redef/IOMakeDetail.txt'

    make = pipe_dir + '/diffex_make.csv'
    make_redef = pipe_dir + '/diffex_make_redef.csv'

    pipe.Bea2002MakeTransformation.of(make_raw).to(make).run()
    pipe.Bea2002MakeTransformation.of(make_redef_raw).to(make_redef).run()

    diff_file = pipe_dir + '/diffex_report.html'

    diff.create_report(make, make_redef, diff_file)
