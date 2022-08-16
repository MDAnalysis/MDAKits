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
    "--targetdir",
    type=str,
    help="directory to get a list od subdirectories from",
    default="./mdakits",
)

parser.add_argument(
    "--excludesubdirs",
    type=str,
    nargs="+",
    help="subdirectories to exclude from constructed matrix",
    default="template",
)

parser.add_argument(
    "--matrixname",
    type=str,
    help="name of matrix name writen to json",
    default=None,
)
    

def get_json_subdir_matrix(maindir: str, excludedirs: List[str],
                           matrixname: Optional[str]) -> str:
    path = Path(f"./{maindir}")

    # get list of subdirectories
    subdirs = []
    for entry in path.iterdir():
        if entry.is_dir():
            var = str(entry.relative_to(f"./{maindir}"))
            if var not in excludedirs:
                subdirs.append(var)
    if matrixname is None:
        return json.dumps(subdirs)
    else:
        return json.dumps({matrixname: subdirs})


if __name__ == "__main__":
    args = parser.parse_args()

    jsonreturn = get_json_subdir_matrix(args.targetdir, args.excludesubdirs,
                                        args.matrixname)

    print(jsonreturn)
