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

javascript(es5) tokens
"""

__author__ = "rapidhere"

import types
from token import _lex_cls_order
from fpjs.exception import LexicalException

__all__ = ["ES5Lexer"]


class ES5Lexer(object):
    """
    A simple(not full version) ES5 Lexer
    """

    def __init__(self, content=""):
        self.content = ""
        self.update(content)

        self._state_start_ch = None
        self._next_token = None
        self._pos = [1, 1]

    def update(self, content):
        """
        update the content to parse
        """
        self.content += content

    def _on_state_comment(self):
        pass

    def _handle_white_space(self):
        if self.content[0] == '\n':
            self._pos = [self._pos[0] + 1, 1]
        else:
            self._pos[1] += 1

        self.content = self.content[1:]

    def next_token(self):
        """
        get next token

        return None on no token

        raise LexicalException on parse error
        """
        self._next_token = None

        while self.content:
            if self.content[0] == "'" or self.content[0] == '"':
                self._on_state_string()
            elif self.content.startswith("//") or self.content.startswith("/*"):
                self._on_state_comment()
            elif self.content[0] in " \t\n\r":

                continue
            else:
                for token in _lex_cls_order:
                    pat = token.pattern
                    if isinstance(pat, types.StringType):
                        if self.content.startswith(pat):
                            self._next_token = token.on_match(self, self._pos, pat)
                            self.content = self.content[len(pat):]
                            self._pos[1] += len(pat)
                    else:
                        r = pat.match(self.content)

                        if r:
                            self._next_token = token.on_match(self, self._pos, r)

                    if self._next_token is not None:
                        break

            if self._next_token is None:
                raise LexicalException()

            return self._next_token

        return None

    def __iter__(self):
        while True:
            token = self.next_token()

            if token is None:
                break

            yield token
