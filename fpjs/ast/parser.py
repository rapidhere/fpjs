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
        tok == ES5String or
        tok == ES5Undefined)


def parse_program(lexer):
    prog = Program()
    while lexer.has_next():
        ret = parse_statement(lexer)
        if not ret:
            raise UnexpectedTokenException(lexer.next_token())
        prog.append(ret)

    return prog


def parse_statement(lexer):
    token = lexer.peek_token()

    if token == ES5Var:
        return parse_var_statement(lexer)
    elif token == ES5Function:
        lexer.next_token()

        func_id = expect_next(lexer, ES5Id)

        expect_next(lexer, ES5LeftParenthesis)
        pars = parse_formal_parameter_list(lexer)
        expect_next(lexer, ES5RightParenthesis)

        # must be block statment
        expect_token(lexer.peek_token(), ES5LeftBrace)
        body = parse_statement(lexer)
        assert body == BlockStatement

        return FunctionStatement(token, func_id, pars, body)
    elif token == ES5SemiColon:
        lexer.next_token()
        return EmptyStatement(token)
    elif token == ES5If:
        lexer.next_token()

        expect_next(lexer, ES5LeftParenthesis)
        test_exp = parse_expression(lexer)
        expect_next(lexer, ES5RightParenthesis)

        true_stat = parse_statement(lexer)

        else_tok = lexer.peek_token()
        false_stat = None
        if else_tok == ES5Else:
            lexer.next_token()
            false_stat = parse_statement(lexer)

        return IfStatement(token, test_exp, true_stat, false_stat)
    elif token == ES5For:
        return parse_for_statement(lexer)
    elif token == ES5Do:
        lexer.next_token()

        body = parse_statement(lexer)
        expect_next(lexer, ES5While)
        expect_next(lexer, ES5LeftParenthesis)
        test_exp = parse_expression(lexer)
        expect_next(lexer, ES5RightParenthesis)
        expect_next(lexer, ES5SemiColon)

        return DoWhileStatement(token, test_exp, body)
    elif token == ES5While:
        lexer.next_token()

        expect_next(lexer, ES5LeftParenthesis)
        test_exp = parse_expression(lexer)
        expect_next(lexer, ES5RightParenthesis)

        body = parse_statement(lexer)
        return WhileStatement(token, test_exp, body)
    elif token == ES5Return:
        # TODO: there should be no \n here, not checked
        lexer.next_token()

        exp = parse_expression(lexer)
        expect_next(lexer, ES5SemiColon)

        return ReturnStatement(token, exp)
    elif token == ES5Break:
        lexer.next_token()
        expect_next(lexer, ES5SemiColon)
        return BreakStatement(token, None)
    elif token == ES5Continue:
        lexer.next_token()
        expect_next(lexer, ES5SemiColon)
        return ContinueStatement(token, None)
    elif token == ES5LeftBrace:
        r = BlockStatement()
        lexer.next_token()
        while lexer.has_next():
            stat = parse_statement(lexer)
            if not stat:
                break
            r.append(stat)
        expect_next(lexer, ES5RightBrace)
        return r
    else:
        return parse_expression_statement(lexer)


def parse_formal_parameter_list(lexer):
    ret = FormalParameterList()

    if lexer.peek_token() != ES5Id:
        return ret

    while True:
        ret.append_parameter(expect_next(lexer, ES5Id))

        if lexer.peek_token() == ES5Comma:
            lexer.next_token()
        else:
            break

    return ret


def parse_argument_list(lexer):
    ret = ArgumentList()

    exp = parse_assignment_expression(lexer)
    if not exp:
        return ret

    while True:
        ret.append_argument(exp)

        if lexer.peek_token() == ES5Comma:
            lexer.next_token()
            exp = parse_assignment_expression(lexer)
            if not exp:
                raise UnexpectedTokenException(lexer.next_token())
        else:
            break

    return ret


def parse_expression_statement(lexer):
    tok = lexer.peek_token()

    if tok == ES5LeftBrace or tok == ES5Function:
        return None

    exp = parse_expression(lexer)

    if not exp:
        return None
    expect_next(lexer, ES5SemiColon)

    return ExpressionStatement(exp)


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


def parse_for_statement(lexer):
    # var in statement is not supported currently
    # var declartion in for is no supported
    for_tok = expect_next(lexer, ES5For)
    init_exp = None
    test_exp = None
    inc_exp = None

    expect_next(lexer, ES5LeftParenthesis)
    if lexer.peek_token() != ES5SemiColon:
        init_exp = parse_expression(lexer)
    expect_next(lexer, ES5SemiColon)

    if lexer.peek_token() != ES5SemiColon:
        test_exp = parse_expression(lexer)
    expect_next(lexer, ES5SemiColon)

    if lexer.peek_token() != ES5RightParenthesis:
        inc_exp = parse_expression(lexer)
    expect_next(lexer, ES5RightParenthesis)

    body_stat = parse_statement(lexer)

    return ForStatement(for_tok, init_exp, test_exp, inc_exp, body_stat)


def parse_expression(lexer):
    exps = []

    while True:
        exp = parse_assignment_expression(lexer)
        if not exp:
            break

        exps.append(exp)

        if lexer.peek_token() == ES5Comma:
            lexer.next_token()
        else:
            break

    if not exps:
        return None
    elif len(exps) == 1:
        return exps[0]
    else:
        exp = MultipleExpression()
        for e in exps:
            exp.append_expression(e)

        return exp


def parse_assignment_expression(lexer):
    """
    this function is design according to es5's grammar specification

    the return value of this function can be AssignmentExpression, BinaryOperatorExpression, UnaryOperatorExpression,
    LeftHandExpression
    """
    ret = parse_conditional_expression(lexer)

    if not ret:
        return None

    if ret != LeftHandExpression:
        return ret

    tok = lexer.peek_token()
    if tok.value not in ["=", "*=", "/=", "%=", "+=", "-=", "<<=", ">>=", ">>>=", "&=", "^=", "|="]:
        return ret

    lexer.next_token()
    right = parse_assignment_expression(lexer)

    if not right:
        raise UnexpectedTokenException(lexer.next_token())

    return AssignmentExpression(ret, tok, right)


def parse_conditional_expression(lexer):
    # currently only return binary expression
    return parse_binary_expression(lexer)

op_priority = (
    ("||", ),
    ("&&", ),
    ("|", ),
    ("^", ),
    ("&", ),
    ("==", "!=", "===", "!=="),
    ("<", ">", "<=", ">="),  # TODO: instanceof
    ("<<", ">>", ">>>"),
    ("+", "-"),
    ("*", "/", "%"))

# convret the op priority
_op_priority = {}
for i in range(0, len(op_priority)):
    for op in op_priority[i]:
        _op_priority[op] = i


def parse_binary_expression(lexer):
    toks = []
    exps = []

    # pop up tokens from token stack and calculate binary expression
    def _pop_tok(tok=None):
        while toks and (not tok or (tok and _op_priority[tok.value] <= _op_priority[toks[-1].value])):
            exp1 = exps.pop()
            exp0 = exps.pop()

            exps.append(BinaryExpression(exp0, toks.pop(), exp1))

    # read up first expression
    exp = parse_unary_expression(lexer)
    if not exp:
        return None
    exps.append(exp)

    # then should one token and one expression
    while True:
        tok = lexer.peek_token()

        if (tok == ES5BinaryOperator and
                tok.value not in ["=", "*=", "/=", "%=", "+=", "-=", "<<=", ">>=", ">>>=", "&=", "^=", "|="]):
            _pop_tok(tok)
            toks.append(lexer.next_token())

            # should have a exp
            exp = parse_unary_expression(lexer)
            if not exp:
                raise UnexpectedTokenException(lexer.next_token())
            exps.append(exp)
        else:
            break

    # pop up left
    _pop_tok()
    return exps[0]


def parse_unary_expression(lexer):
    tok = lexer.peek_token()

    # can only be +,-,~,!
    if (tok == ES5UnaryOperator and tok.value in ["~", "!"]) or (tok == ES5BinaryOperator and tok.value in ["+", "-"]):
        lexer.next_token()
        exp = parse_unary_expression(lexer)

        return UnaryExpression(tok, exp)
    else:
        return parse_postfix_expression(lexer)


def parse_postfix_expression(lexer):
    # can only be left-handside-expression
    return parse_left_hand_expression(lexer)


def parse_left_hand_expression(lexer):
    exp = parse_new_expression(lexer)
    if exp != MemberExpression or lexer.peek_token() != ES5LeftParenthesis:
        return exp

    expect_next(lexer, ES5LeftParenthesis)
    args = parse_argument_list(lexer)
    expect_next(lexer, ES5RightParenthesis)

    exp = CallExpression(exp, args)

    while True:
        tok = lexer.peek_token()

        if tok == ES5LeftParenthesis:
            lexer.next_token()
            args = parse_argument_list(lexer)
            expect_next(lexer, ES5RightParenthesis)
            exp = CallExpression(exp, args)
        elif tok == ES5LeftBracket:
            lexer.next_token()
            idexp = parse_expression(lexer)
            expect_next(lexer, ES5RightBracket)
            exp = MemberExpression(exp, idexp)
        elif tok == ES5Dot:
            lexer.next_token()
            idtok = expect_next(lexer, ES5Id)
            exp = MemberExpression(exp, idtok)
        else:
            break

    return exp


def parse_new_expression(lexer):
    # cannot be new
    return parse_member_expression(lexer)


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
    elif tok == ES5LeftBrace:
        # parse object literal
        lexer.next_token()
        while True:
            tok = lexer.next_token()
            if tok != ES5Id or tok != ES5String or tok != ES5Number:
                raise UnexpectedTokenException(tok)

            expect_next(lexer, ES5Comma)
        expect_next(lexer, ES5RightBracket)
    elif tok == ES5LeftBracket:
        # pass array literal
        # TODO
        pass

    return None


def parse_member_expression(lexer):
    # no new expression
    # can only parse primary expression
    exp = parse_primary_expression(lexer)
    if not exp and lexer.peek_token() == ES5Function:
        exp = parse_function_expression(lexer)

    if not exp:
        return None

    while True:
        tok = lexer.peek_token()

        if tok == ES5LeftBracket:
            lexer.next_token()
            idexp = parse_expression(lexer)
            expect_next(lexer, ES5RightBracket)
            exp = MemberExpression(exp, idexp)
        elif tok == ES5Dot:
            lexer.next_token()
            idtok = expect_next(lexer, ES5Id)
            exp = MemberExpression(exp, idtok)
        else:
            break

    return exp


def parse_function_expression(lexer):
    # currently function expression can only be anonymous function
    tok = expect_next(lexer, ES5Function)
    expect_next(lexer, ES5LeftParenthesis)
    pars = parse_formal_parameter_list(lexer)
    expect_next(lexer, ES5RightParenthesis)

    # must be block statment
    expect_token(lexer.peek_token(), ES5LeftBrace)
    body = parse_statement(lexer)
    assert body == BlockStatement

    # id always been none
    return FunctionExpression(tok, None, pars, body)


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
        return parse_program(self.lexer)
