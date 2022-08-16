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
import operator
import argparse
import yaml
from yaml.loader import SafeLoader
from setuptools._vendor.packaging import specifiers, version
from typing import NamedTuple, Optional, Dict, Callable


Operator = Callable[[str, str], bool]


parser = argparse.ArgumentParser(
    description=("Get a Python version which satisfies the bounds "
                 "defined in the mdakit yamlm file"),
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


class TargetVersion(NamedTuple):
    major: int
    minor: int

    @classmethod
    def from_str(cls, input_str: str):
        ver = version.Version(input_str)
        return cls(
            major=ver.major,
            minor=ver.minor,
        )

    def to_version(self):
        return version.Version(self.to_string())

    def to_string(self):
        return f"{self.major}.{self.minor}"


# Taken from packaging under an Apache 2.0 and BSD license
_operators: Dict[str, Operator] = {
    "in": lambda lhs, rhs: lhs in rhs,
    "not in": lambda lhs, rhs: lhs not in rhs,
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    ">": operator.gt,
}


def get_python_spec(yamlfile: str) -> Optional[str]:

    with open(yamlfile) as f:
        data = yaml.load(f, Loader=SafeLoader)

    try:
        py_spec = data['python_requires']
    except KeyError:
        py_spec = None

    return py_spec


def get_allowed_version(python_pin: Optional[str], max_version: str,
                        min_version: str) -> str:
    if python_pin is None:
        return max_version

    current_version = TargetVersion.from_str(max_version)
    min_version = TargetVersion.from_str(min_version)

    version_spec = [specifiers.Specifier(i) for i in python_pin.split(',')]

    compatible_version = False

    while (current_version.to_version() >= min_version.to_version()):
        for spec in version_spec:
            compatible_version = _operators[spec.operator](
              current_version.to_string(),
              spec.version,
            )

        if compatible_version:
            break
        else:
            current_version.minor -= 1

    if not compatible_version:
        raise ValueError("Could not find compatible version which matched "
                         "the version specs")

    return current_version.to_string()


if __name__ == "__main__":
    args = parser.parse_args()

    yamlfile = f"mdakits/{args.mdakit}/metadata.yaml"

    python_spec = get_python_spec(yamlfile)

    retval = get_allowed_version(python_spec, args.maxpyver, args.minpyver)

    print(retval)
