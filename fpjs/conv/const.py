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
    Y_COMBINATOR = r"(F)=>((G)=>G(G))((self)=>F(()=>self(self)))"
    Y_COMBINATOR_NAME = r"__Y"
    Y_COMBINATOR_FRAGMENT = Y_COMBINATOR_NAME + r"(%s)"

    RUNNER_WRAP_BEGIN = r"((%s)=>" % Y_COMBINATOR_NAME
    RUNNER_WRAP_END = r")(%s);" % Y_COMBINATOR

    IF_ELSE_FRAGMENT = r"((__T,__A)=>(__T&&(%s))||(!__T&&(%s)))(%s,%s)"

    WHILE_FRAGMENT = r"((__WA)=>%s)(%%s)" % (Y_COMBINATOR_FRAGMENT % "(__W)=>(%s)?(%s):__WA()")

    DO_WHILE_FRAGMENT = r"((__WA)=>%s)(%%s)" % (Y_COMBINATOR_FRAGMENT % "(__W)=>%s")

    FOR_FRAGMENT = r"((__WA)=>(%s))(%%s)" % ("%s," + (Y_COMBINATOR_FRAGMENT % "(__W)=>%s"))
