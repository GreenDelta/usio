import argparse
import iodb
import iodb.products
import iodb.bea2002 as bea
import os
import shutil


def clean():
    print("clean:")
    s = 0
    if not os.path.isdir("./build"):
        os.makedirs("./build")
    if os.path.isdir("./build"):
        for fname in os.listdir("./build"):
            s += 1
            path = "./build/" + fname
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    print("  deleted %s file(s)" % s)


def tech():
    print("tech: ")

    def make_fn(name):
        make_bea = os.path.abspath("./data/bea2002/redef/IOMakeDetail.txt")
        make_csv = os.path.abspath("./build/" + name)
        bea.make_to_csv(make_bea, make_csv)

    def use_fn(name):
        use_bea = os.path.abspath("./data/bea2002/redef/IOUseDetail.txt")
        use_csv = os.path.abspath("./build/" + name)
        bea.use_to_csv(use_bea, use_csv)

    def dr_fn(name):
        make_table = iodb.read_sparse_matrix(
            os.path.abspath("./build/make_table.csv"))
        use_table = iodb.read_sparse_matrix(
            os.path.abspath("./build/use_table.csv"))
        dr = iodb.calculate_dr_coefficients(use_table, make_table)
        path = os.path.abspath("./build/" + name)
        dr.write_sparse_csv(path)

    make_resource("make_table.csv", make_fn)
    make_resource("use_table.csv", use_fn)
    make_resource("dr_coefficients.csv", dr_fn)


def products():
    tech()
    print("products: ")

    def fn(name):
        dr_csv = os.path.abspath("./build/dr_coefficients.csv")
        cat_json = os.path.abspath("./data/naics_categories.json")
        prod_csv = os.path.abspath("./build/" + name)
        iodb.products.make_product_table(dr_csv, cat_json, prod_csv)

    make_resource("products.csv", fn)


def make_resource(name, fn):
    if not os.path.isdir("./build"):
        os.makedirs("./build")
    if os.path.exists("./build/" + name):
        print("  %s already exists" % name)
        return
    else:
        fn(name)
        print("  %s created" % name)


def print_help():
    print("""
    iodb - Command line tool

    Command      Description
    ---------------------------------------------
    clean        cleans the build directory
    help         prints this help
    tech         build the technology matrix
    products     create the table with product flows
    envi         build the satellite matrices
    flows        create the table with elementary flows
    spold        create the EcoSpold files
    """)


def main():
    parser = argparse.ArgumentParser(description="iodb - Command line tool",
                                     add_help=False)
    parser.add_argument("commands", nargs="*",
                        help="The commands that should be executed")
    args = parser.parse_args()
    commands = args.commands
    if len(commands) == 0:
        print_help()
    for cmd in commands:
        if cmd == "clean":
            clean()
        elif cmd == "help":
            print_help()
        elif cmd == "tech":
            tech()
        elif cmd == "products":
            products()
        else:
            print("unknown command '%s'" % cmd)
            print_help()


if __name__ == '__main__':
    main()
