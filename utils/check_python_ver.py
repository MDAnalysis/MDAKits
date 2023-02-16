#!/usr/bin/env python3

# MIT License

# Copyright (c) 2022 MDAnalysis Development Team

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Script to check for a compatible python version given an set input
and a python spec defined in the mdakit metadata.yaml file
"""
import argparse
from mdakit import MDAKit


parser = argparse.ArgumentParser(
    description=("Get a Python version which satisfies the bounds "
                 "defined in the mdakit yaml file"),
)


parser.add_argument(
    "--maxpyver",
    type=str,
    help="Maximum allowed python version",
    default="3.9",
)


parser.add_argument(
    "--minpyver",
    type=str,
    help="Minimum allowed python version",
    default="3.6",
)


parser.add_argument(
    "--mdakit",
    type=str,
    help="name of mdakit to obtain info from",
)


if __name__ == "__main__":
    args = parser.parse_args()
    kit = MDAKit(f"mdakits/{args.mdakit}")
    python_ver = kit.get_matching_version(max_ver=args.maxpyver,
                                          min_ver=args.minpyver)
    print(python_ver)
