#!/usr/bin/python
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

the main runner
"""
from fpjs.conv import Converter
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="fpjs",
        description="a horrible code destroyer",
        epilog="author & maintainer: rapidhere@gmail.com")

    parser.add_argument(
        "-v", "--version", action="version",
        help="print the version and exit",
        version="fpjs v0.1")

    parser.add_argument(
        "--print-ast", action="store_true",
        help="print the ast of the code when convert",
        default=False)

    parser.add_argument(
        "input_file", type=str,
        help="the file to convert")

    parser.add_argument(
        "output_file", type=str,
        help="the file to convert")

    args = parser.parse_args()

    converter = Converter()

    with open(args.input_file) as f:
        converter.load(f.read())

    with open(args.output_file, "w") as f:
        f.write(converter.convert(args.print_ast))
