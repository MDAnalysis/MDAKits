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
Script to auto-generate doc file for the mdakits
"""
import sys
import argparse
import yaml
from yaml.loader import SafeLoader
import pathlib
from typing import List, Optional

import sys

abs_filepath = pathlib.Path(__file__).resolve()
REGISTRY_PATH = abs_filepath.parent.parent.parent
MDAKIT_PATH = REGISTRY_PATH / "mdakits"
UTILS_PATH = REGISTRY_PATH / "utils"
sys.path.insert(0, str(UTILS_PATH))

from mdakit import MDAKit


def get_mdakit_matrix(excludedirs=["template",]):
    """
    Get a list of all the mdakits
    """
    mdakits = []
    for entry in MDAKIT_PATH.iterdir():
        if entry.is_dir():
            var = str(entry.relative_to(str(MDAKIT_PATH)))
            if var not in excludedirs:
                mdakits.append(MDAKit(MDAKIT_PATH / var))

    return mdakits


def generate_mdakit_index(target='.', excludedirs=["template",]):

    mdakits = get_mdakit_matrix(excludedirs=["template",])

    title = ("*****************************************\n"
             "Registry of MDAnalysis Toolkits (MDAKits)\n"
             "*****************************************\n")

    body1 = ("The MDAKit registry contains a list of all MDAKits which have "
             "been added to this repository. The aim of this registry is to:\n"
             "  1. Inform members of the community about existing MDAKits\n"
             "  2. Provide sufficient details to allow others to use and "
             "potentially participate in the development of the MDAKits\n"
             "  3. Provide information about the current state of the MDAKits "
             "and how they interact with the latest versions of MDAnalysis\n"
             "Each of the MDAKits in the following table links to a page with "
             "more details about what the MDAKits do, how they can be "
             "installed and how to participate in their development.\n")

    urls = []
    toctree = []

    with open('mdakits.rst', 'w') as f:
        f.write(title)
        f.write(body1)

        f.write('\n.. list-table:: List of registered MDAKits\n')
        f.write('    :class: datatable\n')
        f.write('    :widths: 25 25 25 25\n')
        f.write('    :header-rows: 1\n\n')

        f.write('    * - MDAKit\n')
        f.write('      - Keywords\n')
        f.write('      - Authors\n')
        f.write('      - CI badges\n')

        toctree.append('.. toctree::\n')
        toctree.append('   :maxdepth: 1\n')
        toctree.append('   :hidden:\n\n')

        for kit in mdakits:
            kit.write_table_entry(f, urls, toctree)
            kit.write_mdakit_page()

        # write out the url data
        f.write('\n\n')

        for entry in toctree:
            f.write(entry)
        f.write('\n\n')

        for entry in urls:
            f.write(entry)
        # Terminate list table
        f.write('\n')
