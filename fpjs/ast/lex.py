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

javascript(es5) tokens
"""

__author__ = "rapidhere"

import types
import copy
from token import _lex_cls_order, ES5String
from fpjs.exception import LexicalException, UnexpectEOF

__all__ = ["ES5Lexer"]


class ES5Lexer(object):
    """
    A simple(not full version) ES5 Lexer
    """

    def __init__(self, content=""):
        self.content = ""
        self.update(content)

        self._state_start_ch = None
        self._stored_tokens = []
        self._pos = [1, 1]

    def update(self, content):
        """
        update the content to parse
        """
        self.content += content

    def _on_state_comment(self):
        while self.content:
            self._pos[1] += 1
            ch = self.content[0]
            self.content = self.content[1:]

            if ch == '\n':
                self._pos = [self._pos[0] + 1, 1]

                if self._state_start_ch == "//":
                    return
            elif ch == "*" and self.content[0] == "/":
                self._pos[1] += 1
                self.content = self.content[1:]
                return

    def _on_state_string(self):
        ch = self._state_start_ch
        self.content = self.content[1:]
        self._pos[1] += 1
        ret = ""

        while self.content:
            self._pos[1] += 1
            ch = self.content[0]
            self.content = self.content[1:]

            if ch == "\n":
                raise LexicalException(self._pos, "unexpected new line in string literal")
            elif ch == "\\":
                self._pos[1] += 1
                next_ch = self.content[0]
                self.content = self.content[1:]

                if next_ch == "n":
                    ret += "\n"
                elif next_ch == "r":
                    ret += "\r"
                elif next_ch == '"':
                    ret += '"'
                elif next_ch == "'":
                    ret += "'"
                elif next_ch == "\\":
                    ret += "\\"
                else:
                    raise LexicalException(self._pos, "unknown escape char")
            elif ch == self._state_start_ch:
                return ret
            else:
                ret += ch

    def _handle_white_space(self):
        if self.content[0] == '\n':
            self._pos = [self._pos[0] + 1, 1]
        else:
            self._pos[1] += 1

        self.content = self.content[1:]

    def back_token(self, token):
        """
        back a token to the queue
        """
        self._stored_tokens = [token] + self._stored_tokens

    def has_next(self):
        """
        if has left token to parse
        """
        return self.peek_token() is not None

    def peek_token(self):
        """
        get a token, without remove it from content
        """
        if not self._stored_tokens:
            self._stored_tokens.append(self._next_token())

        ret = self._stored_tokens[0]
        if not ret:
            raise UnexpectEOF()
        return ret

    def next_token(self):
        """
        get next token, and remove it from content
        """
        if not self._stored_tokens:
            self._stored_tokens.append(self._next_token())

        ret = self._stored_tokens.pop(0)
        if not ret:
            raise UnexpectEOF()
        return ret

    def _next_token(self):
        """
        get next token

        return None on no token

        raise LexicalException on parse error
        """
        _next_token = None

        while self.content:
            if self.content[0] == "'" or self.content[0] == '"':
                self._state_start_ch = self.content[0]
                _next_token = ES5String(copy.deepcopy(self._pos), self._on_state_string())
                self._state_start_ch = None
            elif self.content.startswith("//") or self.content.startswith("/*"):
                self._state_start_ch = self.content[:2]
                self._on_state_comment()
                self._state_start_ch = None
                continue
            elif self.content[0] in "\r\n\t \f\v":
                self._handle_white_space()
                continue
            else:
                for token in _lex_cls_order:
                    pat = token.pattern
                    if isinstance(pat, types.StringType):
                        if self.content.startswith(pat):
                            _next_token = token.on_match(self, self._pos, pat)
                            self.content = self.content[len(pat):]
                            self._pos[1] += len(pat)
                    else:
                        r = pat.match(self.content)

                        if r:
                            _next_token = token.on_match(self, self._pos, r)

                    if _next_token is not None:
                        break

            if _next_token is None:
                raise LexicalException(self._pos, "cannot parse token")

            return _next_token

        return None

    def __iter__(self):
        while True:
            token = self.next_token()

            if token is None:
                break

            yield token
