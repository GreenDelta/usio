import argparse
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

    make_resource("make_table.csv", make_fn)


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
        else:
            print("unknown command '%s'" % cmd)
            print_help()


if __name__ == '__main__':
    main()
