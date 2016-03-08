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

some constants
"""

__author__ = "rapidhere"


class CODE_FRAGMENT:
    Y_COMBINATOR = r"(F)=>((G)=>G(G))((self)=>F((...args)=>self(self).apply(this, args)))"

    RUNNER_WRAP_BEGIN = r"((Y)=>"
    RUNNER_WRAP_END = r")(%s);" % Y_COMBINATOR