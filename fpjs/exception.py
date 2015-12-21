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

javascript(es5) tokens
"""

__author__ = "rapidhere"
__all__ = ["LexicalException", "SyntaxExecption", "UnexpectedTokenException", "ExceptTokenToBe"]


class LexicalException(Exception):
    def __init__(self, pos, msg):
        Exception.__init__(self, "line %d, %d: %s" % (pos[0], pos[1], msg))


class SyntaxExecption(Exception):
    def __init__(self, pos, msg):
        Exception.__init__(self, "line %d, %d: %s" % (pos[0], pos[1], msg))


class UnexpectedTokenException(SyntaxExecption):
    def __init__(self, token):
        Exception.__init__(self, token.position, "unexpeted token: " + token.value)


class UnexpectEOF(SyntaxExecption):
    def __init__(self):
        Exception.__init__(self, "unexpected end of file")


class UnexpectedExpression(SyntaxExecption):
    def __init__(self, expression):
        Exception.__init__(self, expression.position, "unexpected expression")
