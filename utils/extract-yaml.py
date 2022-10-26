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
Script to extract relevant information from an mdakit metadata.yaml.
"""
import argparse
import yaml
from yaml.loader import SafeLoader


parser = argparse.ArgumentParser(
    description="Get metadata yaml info",
)

parser.add_argument(
    "--field",
    type=str,
    help="yaml field to get data from",
)

parser.add_argument(
    "--mdakit",
    type=str,
    help="name of mdakit to obtain info from",
)


def get_yaml_info(yamlfile: str, field: str):

    with open(yamlfile) as f:
        data = yaml.load(f, Loader=SafeLoader)

    value = data[field]

    if isinstance(value, list):
        return ';'.join(value)
    else:
        return value


if __name__ == "__main__":
    args = parser.parse_args()

    yamlfile = f"mdakits/{args.mdakit}/metadata.yaml"

    info = get_yaml_info(yamlfile, args.field)

    print(info)
