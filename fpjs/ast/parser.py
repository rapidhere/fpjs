# -*-codiing: utf-8 -*-
"""
Copyright (c) 2015 by rapidhere, RANTTU. INC. All Rights Reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the Lesser GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

predefined licenses headers
ref from http://opensource.org

parse javascript code into AST(abstract syntax tree)
"""

__author__ = "rapidhere"
__all__ = ["ES5Parser"]

from lex import ES5Lexer
from absyn import *
from token import *


def _parse_programm(self):
    prog = ES5MultipleStatement()
    while self.lexer.has_next():
        prog.append(self._parse_statement())

    return prog


def _parse_statement(self):
    token = self.lexer.next_token()

    if token == ES5Function:
        return self._parse_function(token)
    elif token == ES5For:
        pass
    elif token == ES5While:
        pass
    elif token == ES5If:
        pass


def _parse_function(self, func_token):
    pass


class ES5Parser(object):
    def __init__(self):
        self.lexer = ES5Lexer()

    def load(self, content):
        self.lexer.update(content)

    def parse(self):
        return _parse_programm(self.lexer)
