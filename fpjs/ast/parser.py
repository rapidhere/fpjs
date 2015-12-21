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

implemented with recursive-descent

**FUCK LR1 and LALR1**

TODO:

automatic semicolon insertion (probably never support)

declare variable with out var
"""

__author__ = "rapidhere"
__all__ = ["ES5Parser"]

from lex import ES5Lexer
from absyn import *
from token import *
from utils import *
from fpjs.exception import UnexpectedTokenException


def is_literal(tok):
    return (
        tok == ES5Null or
        tok == ES5True or
        tok == ES5False or
        tok == ES5Number or
        tok == ES5String)


def parse_programm(lexer):
    prog = MultipleStatement()
    while lexer.has_next():
        ret = parse_statement(lexer)
        prog.append(ret)

    return prog


def parse_statement(lexer):
    token = lexer.peek_token()

    if token == ES5Var:
        return parse_var_statement(lexer)
    elif token == ES5SemiColon:
        lexer.next_token()
        return EmptyStatement(token)
    elif token == ES5If:
        pass
    elif token == ES5For:
        pass
    elif token == ES5While:
        pass
    elif token == ES5Function:
        return parse_function(lexer, token)
    elif token == ES5Return:
        pass
    elif token == ES5LeftBrace:
        # TODO: block statment or expression statment
        pass

    raise UnexpectedTokenException(token)


def parse_var_statement(lexer):
    # var a = 1, b = 2, c = 3;
    stat = VariableStatement(expect_next(lexer, ES5Var))

    while True:
        var_id = expect_next(lexer, ES5Id)
        tok = lexer.next_token()

        split = None
        # check if have init statement
        if tok == ES5BinaryOperator and tok.value == '=':
            assign = parse_assignment_expression(lexer)
            stat.append_declaration(VariableDeclaration(var_id, assign))
            split = lexer.next_token()
        else:
            stat.append_declaration(VariableDeclaration(var_id, None))
            split = tok

        # check split token to be comma or semicolon
        if split == ES5SemiColon:
            break
        else:
            expect_token(split, ES5Comma)

    return stat


def parse_if_statement(lexer):
    pass


def parse_for_statement(lexer):
    pass


def parse_while_statement(lexer):
    pass


def parse_function(lexer):
    pass


def parse_expression(lexer):
    exps = []

    while True:
        exp = parse_assignment_expression(lexer)
        if not exp:
            raise UnexpectedTokenException(lexer.peek_token())

        exps.append(exp)

        if lexer.peek_token() == ES5Comma:
            lexer.next_token()
        else:
            break

    assert(len(exps) > 0)

    if len(exps) == 1:
        return exps[0]
    else:
        exp = MultipleExpression()
        for e in exps:
            exp.append_expression(e)

        return exp


def parse_assignment_expression(lexer):
    # currently can only start with left_hand_expression
    left = parse_left_hand_expression(lexer)
    if not left:
        return None

    tok = lexer.next_token()
    if tok.value not in ["=", "*=", "/=", "%=", "+=", "-=", "<<=", ">>=", ">>>=", "&=", "^=", "|="]:
        raise UnexpectedTokenException(tok)

    right = parse_assignment_expression(lexer)

    return AssignmentExpression(left, right)


def parse_left_hand_expression(lexer):
    # current left_hand_expression can only be call-expression, member-expression
    # ignore new-expression
    ret = parse_member_expression(lexer)

    if ret:
        return ret

    # return parse_call_expression(lexer)


def parse_primary_expression(lexer):
    # `this` is not included
    # array literal and object literal is not support
    tok = lexer.peek_token()

    if tok == ES5Id:
        lexer.next_token()
        return PrimaryExpression(tok)
    elif is_literal(tok):
        lexer.next_token()
        return PrimaryExpression(tok)
    elif tok == ES5LeftParenthesis:
        lexer.next_token()
        # should alway success when enter this scope
        # if error, should be a uncoverable exception
        ret = parse_expression(lexer)
        expect_next(lexer, ES5RightParenthesis)

        return ret

    return None


def parse_member_expression(lexer):
    # no new expression
    exp = parse_primary_expression(lexer)
    if exp:
        return exp

    # exp = parse_function_expression(lexer)
    # if exp:
    #    return exp

    exp = parse_member_expression(lexer)
    if not exp:
        return None

    tok = lexer.next_token()
    if tok == ES5LeftBracket:
        idx_exp = parse_expression(lexer)
        if not idx_exp:
            raise UnexpectedTokenException(lexer.peek_token())
        expect_next(lexer, ES5RightBracket)

        return MemberExpression(exp, idx_exp)
    elif tok == ES5Dot:
        name = expect_next(lexer, ES5Id)

        return MemberExpression(exp, PrimaryExpression(name))

    raise UnexpectedTokenException(tok)


# def parse_call_expression(lexer):
    # current only can be function(arguments)
#    pass


# def parse_function_expression(lexer):
#    pass


class ES5Parser(object):
    def __init__(self):
        self.lexer = ES5Lexer()

    def load(self, content):
        """
        load the content to parse
        """
        self.lexer.update(content)

    def parse(self):
        """
        parse the loaded content and return the ast

        raise LexicalException, SyntaxExecption on error
        """
        return parse_programm(self.lexer)
