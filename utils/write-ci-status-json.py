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
Script to write out errors to a JSON file for temporary storage.
"""
import argparse
import os
import json
from typing import List, Dict


parser = argparse.ArgumentParser(
    description="Get metadata yaml info",
)

parser.add_argument(
    "--tag",
    type=str,
    help="Name to tag errors with",
)

parser.add_argument(
    "--mdakit",
    type=str,
    help="name of mdakit we are writing errors for",
)


def get_statuses(env_values: List[str]) -> Dict[str, str]:
    status_dict = {}

    for entry in env_values:
        status_dict[entry] = os.environ[entry]

    return status_dict


if __name__ == "__main__":
    args = parser.parse_args()

    env_statuses = ['install_python', 'install_mdakit', 'install_mda',
                    'install_test_deps', 'run_tests']

    status_dict = get_statuses(env_statuses)

    outfile = f"{args.mdakit}-{args.tag}-statuses.json"

    with open(outfile, 'w') as f:
        json.dump(status_dict, f)
