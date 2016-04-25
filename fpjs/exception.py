# -*-coding: utf-8 -*-
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
__all__ = ["LexicalException", "SyntaxException", "UnexpectedTokenException", "UnknownVariable"]


class LexicalException(Exception):
    def __init__(self, pos, msg):
        Exception.__init__(self, "line %d, %d: %s" % (pos[0], pos[1], msg))


class SyntaxException(Exception):
    def __init__(self, pos, msg):
        Exception.__init__(self, "line %d, %d: %s" % (pos[0], pos[1], msg))


class UnexpectedTokenException(SyntaxException):
    def __init__(self, token):
        SyntaxException.__init__(self, token.position, "unexpeted token: " + token.value)


class UnexpectEOF(Exception):
    def __init__(self):
        Exception.__init__(self, "unexpected end of file")


class UnknownVariable(Exception):
    def __init__(self, id):
        Exception.__init__(self, "line %d, %d: unknown variable `%s`" % (id.pos[0], id.pos[1], id.value))
