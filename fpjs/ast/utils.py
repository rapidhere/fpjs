# -*-coding: utf-8-*-
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

some parser helpers
"""

__author__ = "rapidhere"
__all__ = ["expect_token", "expect_next", "expect_absyn"]

from fpjs.exception import UnexpectedTokenException, UnexpectedExpression
from token import *
from absyn import *


def expect_absyn(absyn, absyn_cls):
    """
    except the abstract syntax tree component to have exact class
    """
    if absyn != absyn_cls:
        raise UnexpectedExpression(absyn)

    return absyn


def expect_token(token, token_cls, token_val=None):
    """
    except the token to have the token_cls

    if token_val is not none, will check value as well

    return the token if check success

    raise UnexpectedTokenException if fail
    """
    if token != token_cls:
        raise UnexpectedTokenException(token)

    if token_val is not None and token_val != token.value:
        raise UnexpectedTokenException(token)

    return token


def expect_next(lexer, *args, **kwargs):
    """
    check next token with `expect_token`

    this function is resumable
    """
    token = lexer.peek_token()

    expect_token(token, *args, **kwargs)
    lexer.next_token()

    return token
