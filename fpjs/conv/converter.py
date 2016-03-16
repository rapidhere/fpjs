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

from contextlib import contextmanager

from fpjs.ast import ES5Parser
from fpjs.ast.absyn import *
from fpjs.ast.token import *

import const
from scope import Scope


class Converter(object):
    def __init__(self):
        self.parser = ES5Parser()

    def load(self, content):
        self.parser.load(content)
        self.var_scope = Scope()

    def convert(self, print_ast=False, print_conv=False):
        ast = self.parser.parse()
        assert ast == Program
        if print_ast:
            ast.ast_print()

        with self.scope_block(ast):
            ret = self.convert_program(ast)

        if print_conv:
            print ret

        return ret

    @contextmanager
    def scope_block(self, ast):
        self.var_scope.enter_scope()

        if ast == Program:
            for stat in ast:
                self.build_scope(stat)
        elif ast == FunctionExpression or ast == FunctionStatement:
            self.build_scope(ast.body_statement)
        else:
            raise AssertionError("cannot build scope for ast: " + ast.__class__.__name__)

        yield self.var_scope
        self.var_scope.leave_scope()

    def build_scope(self, ast):
        if ast == IfStatement:
            self.build_scope(ast.true_statement)
            if ast.false_statement:
                self.build_scope(ast.false_statement)
        elif (ast == WhileStatement or
                ast == DoWhileStatement or
                ast == ForStatement):
            self.build_scope(ast.body_statement)
        elif ast == VariableStatement:
            for var in ast:
                self.var_scope[var.var_id] = var
        elif ast == BlockStatement:
            for stat in ast:
                self.build_scope(stat)

    def build_scope_wrap_begin(self):
        return "((" + ",".join(self.var_scope) + ")=>"

    def build_scope_wrap_end(self):
        return ")()"

    def convert_program(self, prog):
        ret = const.CODE_FRAGMENT.RUNNER_WRAP_BEGIN
        ret += self.build_scope_wrap_begin()
        ret += "("

        stats = []
        for stat in prog:
            stats.append(self.convert_statement(stat))
        ret += ",".join(stats)

        ret += ")"
        ret += self.build_scope_wrap_end()
        ret += const.CODE_FRAGMENT.RUNNER_WRAP_END
        return ret

    def convert_statement(self, stat):
        if stat == ExpressionStatement:
            return self.convert_expression(stat.expression)
        elif stat == IfStatement:
            return self.convert_if_statement(stat)
        elif stat == WhileStatement:
            return self.convert_while_statement(stat)
        elif stat == VariableStatement:
            return self.convert_variable_statement(stat)

        raise NotImplementedError("unsupported ast yet: " + stat.__class__.__name__)

    def convert_variable_statement(self, stat):
        ret = []
        for var in stat:
            if var.init is not None:
                ret.append("%s=%s" % (var.var_id.value, self.convert_expression(var.init)))

        return "(" + ",".join(ret) + ")"

    def convert_if_statement(self, stat):
        if not stat.false_statement:
            return const.CODE_FRAGMENT.IF_FRAGMENT % (
                self.convert_statement(stat.true_statement),
                self.convert_expression(stat.test_expression))
        else:
            return const.CODE_FRAGMENT.IF_ELSE_FRAGMENT % (
                self.convert_statement(stat.true_statement),
                self.convert_statement(stat.false_statement),
                self.convert_expression(stat.test_expression))

    def convert_while_statement(self, stat):
        return const.CODE_FRAGMENT.WHILE_FRAGMENT % (
            self.convert_statement(stat.body_statement),
            self.convert_expression(stat.test_expression))

    def convert_expression(self, exp):
        if exp == CallExpression:
            return self.convert_call_expression(exp)
        elif exp == PrimaryExpression:
            return self.convert_primary_expression(exp)
        elif exp == BinaryExpression:
            return self.convert_binary_expression(exp)
        elif exp == UnaryExpression:
            return self.convert_unary_expression(exp)
        elif exp == MemberExpression:
            return self.convert_member_expression(exp)
        elif exp == MultipleExpression:
            return self.convert_multiple_expression(exp)

        raise NotImplementedError("unsupported ast yet: " + exp.__class__.__name__)

    def convert_multiple_expression(self, exp):
        ret = "("
        ret += ",".join([self.convert_expression(e) for e in exp])
        ret += ")"

        return ret

    def convert_call_expression(self, exp):
        assert exp.callee == MemberExpression
        ret = self.convert_member_expression(exp.callee)
        ret += self.convert_args(exp.arguments)

        return ret

    def convert_binary_expression(self, exp):
        ret = "(%s)" % self.convert_expression(exp.left)
        ret += self.convert_token(exp.operator)
        ret += "(%s)" % self.convert_expression(exp.right)

        return ret

    def convert_unary_expression(self, exp):
        expr = self.convert_expression(exp.expression)
        tok = self.convert_token(exp.operator)

        if exp.expression == PrimaryExpression:
            return "%s%s" % (tok, expr)
        else:
            return "%s(%s)" % (tok, expr)

    def convert_member_expression(self, exp):
        group = self.convert_expression(exp.group)

        if exp.identifier == ES5Id:
            if exp.group == PrimaryExpression:
                pattern = "%s.%s"
            else:
                pattern = "(%s).%s"

            return pattern % (group, self.convert_token(exp.identifier))
        else:
            return "%s[%s]" % (group, self.convert_expression(exp.identifier))

    def convert_primary_expression(self, exp):
        return self.convert_token(exp.value)

    def convert_args(self, args):
        ret = "("
        arg_rets = []
        for arg in args:
            arg_rets.append(self.convert_expression(arg))
        ret += ",".join(arg_rets) + ")"
        return ret

    def convert_token(self, tok):
        if tok == ES5String:
            return '"%s"' % tok.value

        return tok.value
