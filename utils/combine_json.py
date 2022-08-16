#!/usr/bin/env python3

# MIT License

# Copyright (c) 2022 MDAnalysis Development Team

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Script to generate an output matrix (in JSON) based on the
directories within `targetdir`, excluding any directories defined
under `excludedir`.
"""
import argparse
import json
from pathlib import Path
from typing import List


parser = argparse.ArgumentParser(
    description="Combine one or more JSON entries",
)

parser.add_argument(
    "--jsonstrs",
    type=str,
    nargs="+",
    help="Json strings to combine",
)


def combine_json(jsonstrs: List[str]) -> str:
    combined = {}
    for entry in jsonstrs:
        print(entry)
        combined.update(json.loads(entry))

    return json.dumps(combined)


if __name__ == "__main__":
    args = parser.parse_args()

    jsonreturn = combine_json(args.jsonstrs)

    print(jsonreturn)
