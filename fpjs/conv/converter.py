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

from fakesyn import *
import const
from scope import Scope
from contextlib import contextmanager


class Converter(object):
    def __init__(self):
        self.parser = ES5Parser()

    def load(self, content):
        self.parser.load(content)
        self.var_scope = Scope()
    
    @contextmanager
    def scope_context(self, ast):
        self.var_scope.enter_scope()
        if ast == Program:
            for stat in ast:
                self.build_scope(stat)
        elif ast == FunctionExpression or ast == FunctionStatement:
            self.build_scope(ast.body_statement)
        else:
            raise AssertionError("cannot build scope for ast: " + ast.__class__.__name__)
            
        yield
        
        self.var_scope.leave_scope()
         

    def convert(self, print_ast=False, print_conv=False):
        ast = self.parser.parse()
        assert ast == Program
        if print_ast:
            ast.ast_print()

        ret = self.wrap_runner(ast)

        if print_conv:
            print ret

        return ret

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
                if var.var_id not in self.var_scope:
                    self.var_scope[var.var_id] = var
        elif ast == BlockStatement:
            for stat in ast:
                self.build_scope(stat)
        elif ast == FunctionStatement:
            self.var_scope[ast.id] = ast

    def build_scope_wrap_begin(self):
        return "((" + ",".join(self.var_scope) + ")=>"

    def build_scope_wrap_end(self):
        return ")()"

    def wrap_runner(self, ast):
        ret = const.CODE_FRAGMENT.RUNNER_WRAP_BEGIN
        ret += self.convert_program(ast)
        ret += const.CODE_FRAGMENT.RUNNER_WRAP_END

        return ret

    def convert_program(self, prog):
        with self.scope_context(prog):
            ret = self.build_scope_wrap_begin()
            ret += self._convert_multiple_statements(iter(prog))
            ret += self.build_scope_wrap_end()
            
        return ret

    def _convert_multiple_statements(self, stats):
        rstats = []

        # de iter
        func_stats = [s for s in stats]
        stats = []

        # filter function statement, put it in front
        for stat in func_stats:
            if stat == FunctionStatement:
                rstats.append("%s = %s" % (stat.id.value, self.convert_function_statement(stat)))
            else:
                stats.append(stat)

        idx = 0
        for stat in stats:
            idx += 1

            if (stat == IfStatement or
                    stat == WhileStatement or
                    stat == DoWhileStatement or
                    stat == ForStatement):
                after = "(()=>%s)" % self._convert_multiple_statements(stats[idx:])
                rstats.append(self._convert_with_after_statement(stat, after))
                break
            elif stat == ReturnStatement:
                rstats.append(self.convert_return_statement(stat))
                break
            elif stat == BreakStatement:
                rstats.append(self.convert_break_statement(stat))
                break
            elif stat == ContinueStatement:
                rstats.append(self.convert_continue_statement(stat))
                break
            elif stat == FakeBreakStatement:
                rstats.append("__A()")
                break
            elif stat == FakeContinueStatement:
                rstats.append("__WN(__W,__WA)")
                break
            elif stat != FunctionStatement:
                rstats.append(self.convert_statement(stat))

        if rstats:
            return "(" + ",".join(rstats) + ")"
        else:
            return "undefined"

    def convert_statement(self, stat):
        if stat == ExpressionStatement:
            return self.convert_expression(stat.expression)
        elif stat == VariableStatement:
            return self.convert_variable_statement(stat)
        elif stat == BlockStatement:
            return self.convert_block_statement(stat)
        elif stat == FunctionStatement:
            return self.convert_function_statement(stat)

        raise NotImplementedError("unsupported ast yet: " + stat.__class__.__name__)
        
    def convert_function_statement(self, stat):
        with self.scope_context(stat):
            ret = "(" + ",".join([arg_id.value for arg_id in stat.arguments]) + ")=>"
            ret += self.build_scope_wrap_begin()
            ret += self.convert_statement(stat.body_statement)
            ret += self.build_scope_wrap_end()
        
        return ret

    def convert_break_statement(self, stat):
        return "__WA()"

    def convert_continue_statement(self, stat):
        return "__WN(__W,__WA)"

    def convert_block_statement(self, stat):
        return self._convert_multiple_statements(iter(stat))

    def convert_return_statement(self, stat):
        return self.convert_expression(stat.expression)

    def convert_variable_statement(self, stat):
        ret = []
        for var in stat:
            if var.init is not None:
                ret.append("%s=%s" % (var.var_id.value, self.convert_expression(var.init)))

        if ret:
            return "(" + ",".join(ret) + ")"
        return "undefined"

    def _convert_with_after_statement(self, stat, after):
        ret = None

        if stat == IfStatement:
            ret = self.convert_if_statement(stat, after)
        elif stat == WhileStatement:
            ret = self.convert_while_statement(stat, after)
        elif stat == DoWhileStatement:
            ret = self.convert_do_while_statement(stat, after)
        elif stat == ForStatement:
            ret = self.convert_for_statement(stat, after)

        if not ret:
            raise AssertionError("not a with-after statement or not implemented: " + stat.__class__.__name__)

        return ret

    def convert_if_statement(self, stat, after):
        stat.true_statement.append(FakeBreakStatement())
        stat.false_statement.append(FakeBreakStatement())

        return const.CODE_FRAGMENT.IF_ELSE_FRAGMENT % (
            self._convert_multiple_statements(iter(stat.true_statement)),
            self._convert_multiple_statements(iter(stat.false_statement)),
            self.convert_expression(stat.test_expression),
            after)

    def convert_while_statement(self, stat, after):
        stat.body_statement.append(FakeContinueStatement())
        return const.CODE_FRAGMENT.WHILE_FRAGMENT % (
            self.convert_expression(stat.test_expression),
            self._convert_multiple_statements(iter(stat.body_statement)),
            after,
            const.CODE_FRAGMENT.WN_WHILE_FRAGMENT)

    def convert_do_while_statement(self, stat, after):
        stat.body_statement.append(FakeContinueStatement())
        wnext = const.CODE_FRAGMENT.WN_DO_WHILE_FRAGMENT % self.convert_expression(stat.test_expression)
        return const.CODE_FRAGMENT.DO_WHILE_FRAGMENT % (
            self._convert_multiple_statements(iter(stat.body_statement)),
            after,
            wnext)

    def convert_for_statement(self, stat, after):
        stat.body_statement.append(FakeContinueStatement())
        return const.CODE_FRAGMENT.FOR_FRAGMENT % (
            self.convert_expression(stat.init_expression),
            self._convert_multiple_statements(iter(stat.body_statement)),
            after,
            const.CODE_FRAGMENT.WN_FOR_FRAGMENT % (
                self.convert_expression(stat.increment_expression),
                self.convert_expression(stat.test_expression)))

    def convert_expression(self, exp):
        if not exp:
            return "undefined"

        if exp == CallExpression:
            return self.convert_call_expression(exp)
        elif exp == PrimaryExpression:
            return self.convert_primary_expression(exp)
        elif exp == BinaryExpression:
            return self.convert_binary_expression(exp)
        elif exp == UnaryExpression:
            return self.convert_unary_expression(exp)
        elif exp == FunctionExpression:
            return self.convert_function_expression(exp)
        elif exp == MemberExpression:
            return self.convert_member_expression(exp)
        elif exp == MultipleExpression:
            return self.convert_multiple_expression(exp)
        elif exp == AssignmentExpression:
            return self.convert_assign_expression(exp)

        raise NotImplementedError("unsupported ast yet: " + exp.__class__.__name__)

    def convert_function_expression(self, exp):
        with self.scope_context(exp):
            ret = "(" + ",".join([arg_id.value for arg_id in exp.arguments]) + ")=>"
            ret += self.build_scope_wrap_begin()
            ret += self.convert_statement(exp.body_statement)
            ret += self.build_scope_wrap_end()
        
        return ret

    def convert_assign_expression(self, exp):
        return (self.convert_expression(exp.left_hand) +
                self.convert_token(exp.operator) +
                self.convert_expression(exp.right_hand))

    def convert_multiple_expression(self, exp):
        ret = "("
        ret += ",".join([self.convert_expression(e) for e in exp])
        ret += ")"

        return ret

    def convert_call_expression(self, exp):
        callee = self.convert_expression(exp.callee)
        if exp.callee == FunctionExpression:
            callee = "(%s)" % callee
            
        return callee + self.convert_args(exp.arguments)

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
        if exp.value == ObjectLiteral:
            return self.convert_object_literal(exp.value)
        elif exp.value == ArrayLiteral:
            return self.convert_array_literal(exp.value)
        else:
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

    def convert_object_literal(self, o):
        props = "["
        for k, v in o.iteritems():
            props += "[%s,%s]," % (self.convert_token(k), self.convert_expression(v))

        props = props[:-1] + "]"

        return const.CODE_FRAGMENT.OBJECT_CONSTRUCTOR_FRAGMENT % props

    def convert_array_literal(self, arr):
        ret = "["
        trim = False

        for v in arr:
            if v is None:
                ret += ","
                trim = False
            else:
                ret += "%s," % self.convert_expression(v)
                trim = True

        if trim:
            ret = ret[:-1]
        ret += "]"
        return ret
