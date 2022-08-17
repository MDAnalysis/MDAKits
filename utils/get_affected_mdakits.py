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
Script to generate an output matrix (in JSON) based on the
directories within `targetdir`, excluding any directories defined
under `excludedir`.
"""
import argparse
import json
from pathlib import Path
from typing import List, Optional


parser = argparse.ArgumentParser(
    description="Get a matrix of directories",
)

parser.add_argument(
    "--json",
    type=str,
    help="input json list of affected files",
)

parser.add_argument(
    "--exclude",
    type=str,
    nargs="+",
    help="mdakit subdirectories to exclude from constructed matrix",
    default="template",
)

parser.add_argument(
    "--matrixname",
    type=str,
    help="name of matrix name writen to json",
    default=None,
)


def get_affected_mdakit_matrix(inputjson: str, excludedirs: List[str],
                               matrixname: Optional[str]) -> str:
    file_list = json.loads(inputjson)

    mdakits = []

    for entry in file_list:
        f_entry = Path(entry)
        if f_entry.name == 'metadata.yaml':
            if f_entry.parts[-2] not in excludedirs:
                mdakits.append(f_entry.parts[-2])

    if matrixname is None:
        return json.dumps(mdakits)
    else:
        return json.dumps({matrixname: mdakits})


if __name__ == "__main__":
    args = parser.parse_args()

    jsonreturn = get_affected_mdakit_matrix(args.json, args.exclude,
                                            args.matrixname)

    print(jsonreturn)
