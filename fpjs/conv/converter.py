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

the converter
"""

__author__ = "rapidhere"


from fpjs.ast import ES5Parser
from fpjs.ast.absyn import *
from fpjs.ast.token import *

import const


def convert_program(prog):
    ret = const.CODE_FRAGMENT.RUNNER_WRAP_BEGIN
    ret += "("

    stats = []
    for stat in prog:
        stats.append(convert_statement(stat))
    ret += ",".join(stats)

    ret += ")"
    ret += const.CODE_FRAGMENT.RUNNER_WRAP_END
    return ret


def convert_statement(stat):
    if stat == ExpressionStatement:
        return convert_expression(stat.expression)

    raise NotImplementedError("unsupported ast yet: " + stat.__class__.__name__)


def convert_expression(exp):
    if exp == CallExpression:
        return convert_call_expression(exp)
    elif exp == PrimaryExpression:
        return convert_primary_expression(exp)
    elif exp == BinaryExpression:
        return convert_binary_expression(exp)

    raise NotImplementedError("unsupported ast yet: " + exp.__class__.__name__)


def convert_call_expression(exp):
    assert exp.callee == MemberExpression
    ret = convert_member_expression(exp.callee)
    ret += convert_args(exp.arguments)

    return ret


def convert_binary_expression(exp):
    pass


def convert_member_expression(exp):
    ret = convert_expression(exp.group)

    if exp.identifier == ES5Id:
        ret += "." + convert_token(exp.identifier)
    else:
        raise NotImplementedError("unsupported identifier for member expression: " + str(exp.identifier))

    return ret


def convert_primary_expression(exp):
    return convert_token(exp.value)


def convert_args(args):
    ret = "("
    arg_rets = []
    for arg in args:
        arg_rets.append("(" + convert_expression(arg) + ")")
    ret += ",".join(arg_rets) + ")"
    return ret


def convert_token(tok):
    if tok == ES5Id:
        return tok.value
    elif tok == ES5String:
        return '"%s"' % tok.value

    raise NotImplementedError("unsupported token yet: " + tok.__class__.__name__)


class Converter(object):
    def __init__(self):
        self.parser = ES5Parser()

    def load(self, content):
        self.parser.load(content)

    def convert(self, print_ast=False, print_conv=False):
        ast = self.parser.parse()
        assert ast == Program
        if print_ast:
            ast.ast_print()

        ret = convert_program(ast)
        if print_conv:
            print ret

        return ret
