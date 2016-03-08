import os
import sys

BASE_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.realpath(os.path.join(BASE_DIR, "..", "..")))

from fpjs.ast import ES5Lexer

if __name__ == "__main__":
    lex = ES5Lexer()
    lex.update(file(os.path.join(BASE_DIR, "demo.js")).read())
    for tok in lex:
        print tok
