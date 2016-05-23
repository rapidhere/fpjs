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

es5 variable scope maintainer
"""

__author__ = "rapidhere"
__all__ = ["Scope"]

from fpjs.exception import UnknownVariable


class Scope(object):
    def __init__(self):
        self.scopes = []

    def enter_scope(self):
        self.scopes.append({})

    def leave_scope(self):
        self.scopes.pop(-1)

    def __getitem__(self, key):
        for scope in self.scopes[::-1]:
            r = scope.get(key.value, None)
            if r:
                return r

        raise UnknownVariable(key)

    def __contains__(self, key):
        return key.value in self.scopes[-1]

    def __setitem__(self, key, value):
        self.scopes[-1][key.value] = value
        return value

    def __iter__(self):
        return iter(sorted(self.scopes[-1].keys()))

    def values(self):
        return [self.scopes[-1][key] for key in self]

    def get_by_key_value(self, kv):
        return self.scopes[-1][kv]
