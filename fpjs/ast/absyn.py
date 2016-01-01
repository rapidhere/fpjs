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

javascript(es5) abstract syntax tree components

for more info please refer to the ES5 stantards (https://es5.github.io/)
"""

__author__ = "rapidhere"


class ES5AbstractSyntax(object):
    _indent_char = "  "

    def __eq__(self, b):
        return issubclass(self.__class__, b.__class__) or issubclass(self.__class__, b)

    def __ne__(self, b):
        return not self.__eq__(b)

    @property
    def position(self):
        pass

    def _print(self, indent, msg):
        print (self._indent_char * indent) + str(msg)

    def ast_print(self, indent=0):
        self._print(indent, self)


class Statement(ES5AbstractSyntax):
    pass


class Program(ES5AbstractSyntax):
    def __init__(self):
        self.statments = []

    def append(self, statement):
        self.statments.append(statement)

    def __iter__(self):
        return iter(self.statments)

    def ast_print(self, indent=0):
        self._print(indent, "MultipleStatement:")

        for stat in self.statments:
            stat.ast_print(indent + 1)


class BlockStatement(Statement):
    def __init__(self):
        self.statments = []

    def append(self, statement):
        self.statments.append(statement)

    def __iter__(self):
        return iter(self.statments)

    def ast_print(self, indent=0):
        self._print(indent, "BlockStatement")

        for stat in self.statments:
            stat.ast_print(indent + 1)


class FunctionStatement(Statement):
    def __init__(self, tok, id, args, body):
        self.token = tok
        self.id = id
        self.arguments = args
        self.body_statement = body

    def position(self):
        return self.token.position

    def ast_print(self, indent=0):
        self._print(indent, "FunctionStatement:")
        self._print(indent + 1, self.id)
        self.arguments.ast_print(indent + 1)
        self._print(indent + 1, "Body:")
        self.body_statement.ast_print(indent + 2)


class ArgumentList(ES5AbstractSyntax):
    def __init__(self):
        self.arguments = []

    def __iter__(self):
        return iter(self.arguments)

    def append_argument(self, arg):
        self.arguments.append(arg)

    def position(self):
        return self.arguments[0].position

    def ast_print(self, indent=0):
        self._print(indent, "Arguments:")
        for arg in self.arguments:
            self._print(indent + 1, arg)


class ReturnStatement(Statement):
    def __init__(self, tok, exp):
        self.expression = exp
        self.token = tok

    def position(self):
        return self.token.position

    def ast_print(self, indent=0):
        self._print(indent, "ReturnStatement:")
        if self.expression:
            self.expression.ast_print(indent + 1)
        else:
            self._print(indent + 1, "None")


class IfStatement(Statement):
    def __init__(self, if_tok, test_exp, true_stat, false_stat):
        self.if_token = if_tok
        self.test_expression = test_exp
        self.true_statement = true_stat
        self.false_statement = false_stat

    def position(self):
        return self.if_token.position

    def ast_print(self, indent=0):
        self._print(indent, "IfStatement:")
        self._print(indent + 1, "Test:")
        self.test_expression.ast_print(indent + 2)
        self._print(indent + 1, "True:")
        self.true_statement.ast_print(indent + 2)
        self._print(indent + 1, "False:")
        if self.false_statement:
            self.false_statement.ast_print(indent + 2)
        else:
            self._print(indent + 2, "None")


class VariableStatement(Statement):
    def __init__(self, var_token):
        self.var = var_token
        self.declartions = []

    def append_declaration(self, dec):
        self.declartions.append(dec)

    def __iter__(self):
        return iter(self.declartions)

    def position(self):
        return self.var.position

    def ast_print(self, indent=0):
        self._print(indent, "VariableStatement:")

        for dec in self.declartions:
            dec.ast_print(indent + 1)


class ExpressionStatement(Statement):
    def __init__(self, exp):
        self.expression = exp

    def position(self):
        return self.expression.position

    def ast_print(self, indent=0):
        self._print(indent, "ExpressionStatement:")
        self.expression.ast_print(indent + 1)


class WhileStatement(Statement):
    def __init__(self, tok, test_exp, body_stat):
        self.token = tok
        self.test_expression = test_exp
        self.body_statement = body_stat

    def position(self):
        return self.token.position

    def ast_print(self, indent=0):
        self._print(indent, "WhileStatement:")
        self._print(indent + 1, "Test:")
        self.test_expression.ast_print(indent + 2)
        self._print(indent + 1, "Body:")
        self.body_statement.ast_print(indent + 2)


class DoWhileStatement(Statement):
    def __init__(self, tok, test_exp, body_stat):
        self.token = tok
        self.test_expression = test_exp
        self.body_statement = body_stat

    def position(self):
        return self.token.position

    def ast_print(self, indent=0):
        self._print(indent, "DoWhileStatement:")
        self._print(indent + 1, "Body:")
        self.body_statement.ast_print(indent + 2)
        self._print(indent + 1, "Test:")
        self.test_expression.ast_print(indent + 2)


class ForStatement(Statement):
    def __init__(self, tok, init_exp, test_exp, inc_exp, body_stat):
        self.token = tok
        self.init_expression = init_exp
        self.test_expression = test_exp
        self.increment_expression = inc_exp
        self.body_statement = body_stat

    def position(self):
        return self.token.position

    def ast_print(self, indent=0):
        self._print(indent, "ForStatement:")

        self._print(indent + 1, "Init:")
        if self.init_expression:
            self.init_expression.ast_print(indent + 2)
        else:
            self._print(indent + 2, "None")

        self._print(indent + 1, "Test:")
        if self.test_expression:
            self.test_expression.ast_print(indent + 2)
        else:
            self._print(indent + 2, "None")

        self._print(indent + 1, "Increment:")
        if self.increment_expression:
            self.increment_expression.ast_print(indent + 2)
        else:
            self._print(indent + 2, "None")

        self._print(indent + 1, "Body:")
        self.body_statement.ast_print(indent + 2)


class EmptyStatement(Statement):
    def __init__(self, semicolon):
        self.semicolon = semicolon

    def position(self):
        return self.semicolon.position

    def ast_print(self, indent=0):
        self._print(indent, "EmptyStatement")


class VariableDeclaration(ES5AbstractSyntax):
    def __init__(self, var_id, init=None):
        self.var_id = var_id
        self.init = init

    def position(self):
        return self.var_id.position

    def ast_print(self, indent=0):
        self._print(indent, "VariableDeclaration")
        self._print(indent + 1, "var_id: " + str(self.var_id))
        if self.init:
            self.init.ast_print(indent + 1)


class Expression(ES5AbstractSyntax):
    pass


class MultipleExpression(Expression):
    def __init__(self):
        self.expressions = []

    def append_expression(self, exp):
        self.expressions.append(exp)

    def position(self):
        self.expressions[0].position

    def ast_print(self, indent=0):
        self._print(indent, "MultipleExpression:")
        for exp in self.expressions:
            exp.ast_print(indent + 1)


class AssignmentExpression(Expression):
    def __init__(self, left_hand, op, right_hand):
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.operator = op

    def position(self):
        return self.left_hand.position

    def ast_print(self, indent=0):
        self._print(indent, "AssignmentExpression:")
        self._print(indent + 1, self.operator)
        self.left_hand.ast_print(indent + 1)
        self.right_hand.ast_print(indent + 1)


class BinaryExpression(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.operator = op
        self.right = right

    def position(self):
        return self.left.position

    def ast_print(self, indent=0):
        self._print(indent, "BinaryExpression:")
        self._print(indent + 1, self.operator)
        self.left.ast_print(indent + 1)
        self.right.ast_print(indent + 1)


class UnaryExpression(Expression):
    def __init__(self, op, exp):
        self.operator = op
        self.expression = exp


class LeftHandExpression(Expression):
    pass


class MemberExpression(LeftHandExpression):
    def __init__(self, group, member):
        self.group = group
        self.member = member

    def position(self):
        return self.group.position


class CallExpression(LeftHandExpression):
    pass


class PrimaryExpression(MemberExpression):
    def __init__(self, value):
        self.value = value

    def position(self):
        # compatible for all tokens and expressions
        return self.value.position

    def ast_print(self, indent=0):
        self._print(indent, "PrimaryExpression:")
        self._print(indent + 1, self.value)
