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
    elif exp == UnaryExpression:
        return convert_unary_expression(exp)
    elif exp == MemberExpression:
        return convert_member_expression(exp)
    elif exp == MultipleExpression:
        return convert_multiple_expression(exp)

    raise NotImplementedError("unsupported ast yet: " + exp.__class__.__name__)


def convert_multiple_expression(exp):
    ret = "("
    ret += ",".join([convert_expression(e) for e in exp])
    ret += ")"

    return ret


def convert_call_expression(exp):
    assert exp.callee == MemberExpression
    ret = convert_member_expression(exp.callee)
    ret += convert_args(exp.arguments)

    return ret


def convert_binary_expression(exp):
    ret = "(%s)" % convert_expression(exp.left)
    ret += convert_token(exp.operator)
    ret += "(%s)" % convert_expression(exp.right)

    return ret


def convert_unary_expression(exp):
    expr = convert_expression(exp.expression)
    tok = convert_token(exp.operator)

    if exp.expression == PrimaryExpression:
        return "%s%s" % (tok, expr)
    else:
        return "%s(%s)" % (tok, expr)


def convert_member_expression(exp):
    group = convert_expression(exp.group)

    if exp.identifier == ES5Id:
        if exp.group == PrimaryExpression:
            pattern = "%s.%s"
        else:
            pattern = "(%s).%s"

        return pattern % (group, convert_token(exp.identifier))
    else:
        return "%s[%s]" % (group, convert_expression(exp.identifier))


def convert_primary_expression(exp):
    return convert_token(exp.value)


def convert_args(args):
    ret = "("
    arg_rets = []
    for arg in args:
        arg_rets.append(convert_expression(arg))
    ret += ",".join(arg_rets) + ")"
    return ret


def convert_token(tok):
    if tok == ES5String:
        return '"%s"' % tok.value

    return tok.value


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
