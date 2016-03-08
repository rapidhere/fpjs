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

converter test fragment tester
"""

__author__ = "rapidhere"

import os
import sys

BASE_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.realpath(os.path.join(BASE_DIR, "..", "..")))

import subprocess
import unittest
import argparse

from fpjs import Converter


class JSFragmentTestCase(unittest.TestCase):
    """
    custom fragment test case
    """
    def __init__(self, fragment_name, print_ast=False, print_conv=False, *args, **kwargs):
        super(JSFragmentTestCase, self).__init__(*args, **kwargs)
        self.fragment_name = fragment_name
        self.print_ast = print_ast
        self.print_conv = print_conv

        if not os.path.isfile(self.fragment_path):
            raise ValueError("no such fragment: " + self.fragment_name)

    @property
    def fragment_path(self):
        return os.path.join(BASE_DIR, self.fragment_name + ".js")

    @staticmethod
    def _run(content):
        return subprocess.check_output(["node", "--harmony_rest_parameters", "-e", content])

    @classmethod
    def load_fragment(cls, fragment_name, **kwargs):
        return cls(fragment_name, "test_fragment", **kwargs)

    def fail(self, msg):
        super(JSFragmentTestCase, self).fail("\n[FRAG: " + self.fragment_name + "] " + msg)

    def test_fragment(self):
        with open(self.fragment_path) as f:
            raw_content = f.read()

            conv = Converter(self.print_ast, self.print_conv)
            conv.load(raw_content)
            content = conv.convert()

            try:
                raw_ret = self._run(raw_content)
                ret = self._run(content)
            except Exception as e:
                self.fail("should not raise exceptions when run fragment: " + e.message)

            if raw_ret != ret:
                self.fail("fragment result not same:\nraw:\n%s \n==========\nconv:\n %s" % (raw_ret, ret))


def load_all(**kwargs):
    ts = unittest.TestSuite()

    for fname in os.listdir(BASE_DIR):
        if fname.endswith(".js"):
            ts.addTest(JSFragmentTestCase.load_fragment(fname[:-3], **kwargs))

    return ts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="fpjs js fragment tester",
        description="test converter",
        epilog="maintainer: rapidhere@gmail.com")

    parser.add_argument(
        "-v", "--version", action="version",
        help="print the version and exit",
        version="fpjs js fragment tester v0.1")
    parser.add_argument("--print-ast", help="print ast when print", action="store_true", default=False)
    parser.add_argument(
        "--print-conv", help="print converted result when print", action="store_true", default=False)

    parser.add_argument("fragment", type=str, help="the fragment to test", default="all")

    args = parser.parse_args()

    ts = unittest.TestSuite()

    opt = {
        "print_ast": args.print_ast,
        "print_conv": args.print_conv}

    if args.fragment == "all":
        ts.addTest(load_all(**opt))
    else:
        ts.addTest(JSFragmentTestCase.load_fragment(args.fragment, **opt))

    tr = unittest.TextTestRunner()
    tr.run(ts)
