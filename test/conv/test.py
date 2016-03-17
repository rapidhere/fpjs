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
    def __init__(self, fragment_name, print_ast=False, print_conv=False, print_result=False, *args, **kwargs):
        super(JSFragmentTestCase, self).__init__(*args, **kwargs)
        self.fragment_name = fragment_name
        self.print_ast = print_ast
        self.print_conv = print_conv
        self.print_result = print_result

        if not os.path.isfile(self.fragment_path):
            raise ValueError("no such fragment: " + self.fragment_name)

    @property
    def fragment_path(self):
        return os.path.join(BASE_DIR, self.fragment_name + ".js")

    @staticmethod
    def _run(content):
        return subprocess.check_output(["node", "-e", content])

    @classmethod
    def load_fragment(cls, fragment_name, **kwargs):
        kwargs["methodName"] = "test_fragment"
        return cls(fragment_name, **kwargs)

    def fail(self, msg):
        super(JSFragmentTestCase, self).fail("\n[FRAG: " + self.fragment_name + "] " + msg)

    def test_fragment(self):
        with open(self.fragment_path) as f:
            raw_content = f.read()

            conv = Converter()
            conv.load(raw_content)
            content = conv.convert(self.print_ast, self.print_conv)

            try:
                raw_ret = self._run(raw_content)
                ret = self._run(content)
            except Exception as e:
                self.fail("should not raise exceptions when run fragment: " + e.message)

            if self.print_result:
                print "=" * 20
                print "raw:"
                print raw_ret
                print "=" * 20
                print "conv:"
                print ret
                print "=" * 20

            if raw_ret != ret:
                self.fail("fragment result not same:\nraw:\n%s \n==========\nconv:\n%s" % (raw_ret, ret))


def load_all(**kwargs):
    ts = unittest.TestSuite()

    for fname in os.listdir(BASE_DIR):
        if fname.endswith(".js") and not fname.startswith("__"):
            ts.addTest(JSFragmentTestCase.load_fragment(fname[:-3], **kwargs))

    return ts


def _main():
    parser = argparse.ArgumentParser(
        prog="test.py",
        description="test converter",
        epilog="maintainer: rapidhere@gmail.com")

    parser.add_argument(
        "-v", "--version", action="version",
        help="print the version and exit",
        version="fpjs js fragment tester v0.1")

    parser.add_argument(
        "--print-ast", action="store_true",
        help="print ast when tst",
        default=False)

    parser.add_argument(
        "--print-conv", action="store_true",
        help="print converted result when test",
        default=False)

    parser.add_argument(
        "--print-result", action="store_true",
        help="print outputs when test",
        default=False)

    parser.add_argument(
        "fragment", type=str,
        help="the fragment to test, when set to all, will test fragment-files not starts with `__`",
        default="all")

    args = parser.parse_args()

    ts = unittest.TestSuite()

    opt = {
        "print_ast": args.print_ast,
        "print_conv": args.print_conv,
        "print_result": args.print_result}

    if args.fragment == "all":
        ts.addTest(load_all(**opt))
    else:
        ts.addTest(JSFragmentTestCase.load_fragment(args.fragment, **opt))

    tr = unittest.TextTestRunner()
    ret = tr.run(ts)

    if ret.wasSuccessful():
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    _main()
