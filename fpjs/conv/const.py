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

    WHILE_FRAGMENT = r"((__WA,__WN)=>%s)(%%s,%%s)" % (Y_COMBINATOR_FRAGMENT % "(__W)=>(%s)?(%s):__WA()")
    WN_WHILE_FRAGMENT = r"(__W,__WA)=>__W()"

    DO_WHILE_FRAGMENT = r"((__WA,__WN)=>%s)(%%s,%%s)" % (Y_COMBINATOR_FRAGMENT % "(__W)=>%s")
    WN_DO_WHILE_FRAGMENT = r"(__W,__WA)=>(%s)?__W():__WA()"

    FOR_FRAGMENT = r"((__WA,__WN)=>(%s))(%%s,%%s)" % ("%s," + (Y_COMBINATOR_FRAGMENT % "(__W)=>%s"))
    WN_FOR_FRAGMENT = r"(__W,__WA)=>(%s,(%s)?__W():__WA())"

    OBJECT_CONSTRUCTOR_NAME = r"__OC"
    OBJECT_CONSTRUCTOR_FRAGMENT = OBJECT_CONSTRUCTOR_NAME + r"(%s)"
    OBJECT_CONSTRUCTOR = r"(o, ro)=>(ro=new Object(),o.forEach((i)=>(ro[i[0]]=i[1])),ro)"

    RUNNER_WRAP_BEGIN = r"((%s,%s)=>" % (Y_COMBINATOR_NAME, OBJECT_CONSTRUCTOR_NAME)
    RUNNER_WRAP_END = r")(%s,%s);" % (Y_COMBINATOR, OBJECT_CONSTRUCTOR)

    IF_ELSE_FRAGMENT = r"((__T,__A)=>(__T?(%s):(%s)))(%s,%s)"
