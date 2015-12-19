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

es5 tokens (not full version)

TODO:

regex

?:, ++, --

with, instanceof, typeof, switch, case, try, catch, finally, void, break, continue,
this, default, throw, delete, in

octocal and hexical number

line-continuation, more esacpe sequence
"""

__author__ = "rapidhere"
__all__ = [
    "ES5Var", "ES5New", "ES5Function", "ES5Null", "ES5True", "ES5False", "ES5Undefined", "ES5For", "ES5Do",
    "ES5While", "ES5If", "ES5Else", "ES5Comma", "ES5Colon", "ES5Dot", "ES5SemiColon", "ES5LeftParenthesis",
    "ES5RightParenthesis", "ES5LeftBracket", "ES5RightBracket", "ES5LeftBrace", "ES5RightBrace", "ES5Minus",
    "ES5UnaryOperator", "ES5BinaryOperator", "ES5Number", "ES5SemiColon", "ES5Id"]

import re
import types

import copy


class ES5Token(object):
    pattern = None

    def __init__(self, position, value):
        self.position = position
        self.value = value

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "TOKEN@(%03s, %03s): %-30s %s" % (
            str(self.position[0]), str(self.position[1]),
            self.__class__.__name__, self.value)

    def __eq__(self, b):
        """
        just compile class
        """
        return self.__class__ == b.__class__ or self.__class == b

    @classmethod
    def on_match(cls, lexer, position, ret):
        """
        call on match
        """
        cur_pos = copy.deepcopy(position)

        if not isinstance(ret, types.StringType):
            ret = ret.group()
            lexer.content = lexer.content[len(ret):]
            lexer._pos[1] += len(ret)

        return cls(cur_pos, ret)

boundary = r"(?=[^_$a-zA-Z0-9])"


class ES5Var(ES5Token):
    pattern = re.compile(r"var" + boundary)


class ES5Function(ES5Token):
    pattern = re.compile(r"function" + boundary)


class ES5Return(ES5Token):
    pattern = re.compile("return" + boundary)


class ES5Null(ES5Token):
    pattern = re.compile("null" + boundary)


class ES5True(ES5Token):
    pattern = re.compile("true" + boundary)


class ES5False(ES5Token):
    pattern = re.compile("false" + boundary)


class ES5Undefined(ES5Token):
    pattern = re.compile("undefined" + boundary)


class ES5For(ES5Token):
    pattern = re.compile("for" + boundary)


class ES5Do(ES5Token):
    pattern = re.compile("do" + boundary)


class ES5While(ES5Token):
    pattern = re.compile("while" + boundary)


class ES5If(ES5Token):
    pattern = re.compile("if" + boundary)


class ES5Else(ES5Token):
    pattern = re.compile("else" + boundary)


class ES5New(ES5Token):
    pattern = re.compile("new" + boundary)


class ES5Comma(ES5Token):
    pattern = ","


class ES5Colon(ES5Token):
    pattern = ":"


class ES5Dot(ES5Token):
    pattern = "."


class ES5SemiColon(ES5Token):
    pattern = ";"


class ES5LeftParenthesis(ES5Token):
    pattern = "("


class ES5RightParenthesis(ES5Token):
    pattern = ")"


class ES5LeftBracket(ES5Token):
    pattern = "["


class ES5RightBracket(ES5Token):
    pattern = "]"


class ES5LeftBrace(ES5Token):
    pattern = "{"


class ES5RightBrace(ES5Token):
    pattern = "}"


class ES5Minus(ES5Token):
    pattern = "-"


class ES5UnaryOperator(ES5Token):
    pattern = re.compile(r"[~!]")


class ES5BinaryOperator(ES5Token):
    pattern = re.compile(r"[\+\-\*/%><\|&=^]|==|===|>=|<=|>==|<==|!=|!==|&&|\|\|\+=|\-=|\*=|\=|%=|\|=|&=|^=|<<|>>|>>>|"
                         r"<<=|>>=|>>>=")


class ES5Number(ES5Token):
    pattern = re.compile(r"(?:0[x|X])?\d+" + boundary)


class ES5String(ES5Token):
    pass  # handle by lexer


class ES5Id(ES5Token):
    pattern = re.compile(r"[_$a-zA-Z][_$a-zA-Z0-9]*" + boundary)


_lex_cls_order = (
    ES5Var,
    ES5New,
    ES5Function,
    ES5Null,
    ES5True,
    ES5False,
    ES5Undefined,
    ES5For,
    ES5Do,
    ES5While,
    ES5If,
    ES5Else,
    ES5Comma,
    ES5Colon,
    ES5Dot,
    ES5SemiColon,
    ES5LeftParenthesis,
    ES5RightParenthesis,
    ES5LeftBracket,
    ES5RightBracket,
    ES5LeftBrace,
    ES5RightBrace,
    ES5Minus,
    ES5UnaryOperator,
    ES5BinaryOperator,
    ES5Number,
    ES5SemiColon,
    ES5Id)
