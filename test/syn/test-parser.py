import os
import sys

BASE_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.realpath(os.path.join(BASE_DIR, "..", "..")))

from fpjs.ast import ES5Parser

if __name__ == "__main__":
    parser = ES5Parser()
    parser.load(file(os.path.join(BASE_DIR, "demo.js")).read())
    parser.parse().ast_print()
    print ""
