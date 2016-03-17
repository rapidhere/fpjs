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

some decorators
"""

__author__ = "rapidhere"
__all__ = ["scope_block"]


from fpjs.ast.absyn import *


def scope_block(func):
    def _func(self, ast):
        self.var_scope.enter_scope()

        if ast == Program:
            for stat in ast:
                self.build_scope(stat)
        elif ast == FunctionExpression or ast == FunctionStatement:
            self.build_scope(ast.body_statement)
        else:
            raise AssertionError("cannot build scope for ast: " + ast.__class__.__name__)

        ret = self.build_scope_wrap_begin()
        ret += func(self, ast)
        ret += self.build_scope_wrap_end()

        self.var_scope.leave_scope()

        return ret

    return _func
