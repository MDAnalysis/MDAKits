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
import argparse
import json
import yaml
from yaml.loader import SafeLoader
import pathlib
from typing import List, Optional


# shamelessly copying from the cookiecutter
abs_filepath = pathlib.Path(__file__).resolve()
REGISTRY_PATH = abs_filepath.parent.parent.parent
MDAKIT_PATH = REGISTRY_PATH / "mdakits"


def get_mdakit_matrix(excludedirs=["template",]):
    """
    Get a list of all the mdakits
    """
    mdakits = []
    for entry in MDAKIT_PATH.iterdir():
        if entry.is_dir():
            var = str(entry.relative_to(str(MDAKIT_PATH)))
            if var not in excludedirs:
                mdakits.append(var)

    return mdakits


def get_yaml(mdakit, yamlname):

    path = MDAKIT_PATH / mdakit / yamlname

    with open(str(path)) as f:
        data = yaml.load(f, Loader=SafeLoader)

    return data


def get_custom_badge(left, right, colour):
    return f"https://img.shields.io/badge/{left}-{right}-{colour}.svg"


def write_table_entry(f, kit, urls, toctree):
    kit_data = get_yaml(kit, 'metadata.yaml')
    ci_data = get_yaml(kit, 'status.yaml')

    mdakit_name = kit_data['project_name']
    keywords = ', '.join(kit_data['keywords'])

    # authors can be a link to a file
    if 'https' in kit_data['authors'][0]:
        authors = f"`{mdakit_name} authors`_"
        urls.append(f".. _`{mdakit_name} authors`:\n"
                    f"   {kit_data['authors'][0]}\n\n")
    else:
        authors = ', '.join(kit_data['authors'])

    latest = f"|{mdakit_name}_latest|"

    latest_badge = get_custom_badge(
            mdakit_name,
            "latest",
            "red" if ci_data['latest']['numfails'] > 0 else 'green',
    )
    urls.append(f".. |{mdakit_name}_latest| image:: {latest_badge}\n"
                f"   :alt: {mdakit_name} latest CI status\n"
                f"   :target: https://github.com/MDAnalysis/MDAKits/actions\n\n")

    develop = f"|{mdakit_name}_develop|"
    develop_badge = get_custom_badge(
            mdakit_name,
            "develop",
            "red" if ci_data['develop']['numfails'] > 0 else 'green',
    )
    urls.append(f".. |{mdakit_name}_develop| image:: {develop_badge}\n"
               f"   :alt: {mdakit_name} develop CI status\n"
               f"   :target: https://github.com/MDAnalysis/MDAKits/actions\n\n")

    f.write(f'    * - :ref:`{mdakit_name}`\n')
    f.write(f'      - {keywords}\n')
    f.write(f'      - {authors}\n')
    f.write(f'      - {latest} {develop}\n')
    toctree.append(f'   {mdakit_name}\n')


def write_mdakit_page(mdakit):
    kit_data = get_yaml(mdakit, 'metadata.yaml')
    ci_data = get_yaml(mdakit, 'status.yaml')

    mdakit_name = kit_data['project_name']
    urls = []

    title = ("************************\n"
             f"{mdakit_name}\n"
             "************************\n\n")

    description = f"| **MDAKit description:** {kit_data['description']}\n"

    keywords = f"| **Keywords:** {', '.join(kit_data['keywords'])}\n"

    if 'https' in kit_data['authors'][0]:
        auths = f"`{mdakit_name} authors`_"
        urls.append(f".. _`{mdakit_name} authors`:\n"
                    f"   {kit_data['authors'][0]}\n\n")
    else:
        auths = ', '.join(kit_data['authors'])

    authors = f"| **Authors:** {auths}\n"

    project_home = f"| **Project home:** `🏠`_\n"

    urls.append(".. _`🏠`:\n"
                f"   {kit_data['project_home']}\n\n")

    documentation_home = f"| **Documentation:** `📙`_\n"

    urls.append(".. _`📙`:\n"
                f"   {kit_data['documentation_home']}\n\n")

    license = f"| **License:** {kit_data['license']}\n"

    if (kit_data['install'] is not None) or (kit_data['src_install'] is not None):
        installation_instructions = (
                "Installation instructions\n"
                "=========================\n\n")

        if kit_data['install'] is not None:
            installation_instructions += (
                    f"The latest version of {mdakit_name} can be "
                    "installed using the following:\n\n"
                    ".. code-block:: bash\n\n"
                    f"    {kit_data['install']}\n\n"
            )

        if kit_data['src_install'] is not None:
            installation_instructions += (
                    f"The source code of {mdakit_name} can be "
                    "installed using the following:\n\n"
                    ".. code-block:: bash\n\n"
                    f"    {kit_data['src_install']}\n\n"
            )
    else:
        installation_instructions = None

    with open(f"{mdakit_name}.rst", 'w') as kitf:

        kitf.write(f".. _{mdakit_name}:\n\n")
        kitf.write(title)
        kitf.write(description)
        kitf.write(keywords)
        kitf.write(authors)
        kitf.write(project_home)
        kitf.write(documentation_home)
        kitf.write(license)
        kitf.write("\n\n")

        if installation_instructions is not None:
            kitf.write(installation_instructions)

        for entry in urls:
            kitf.write(entry)
        

def generate_mdakit_index(target='.', excludedirs=["template",]):

    mdakits = get_mdakit_matrix(excludedirs=["template",])

    title = ("*****************************************\n"
             "Registry of MDAnalysis Toolkits (MDAKits)\n"
             "*****************************************\n")

    body1 = ("The MDAKit registry contains a list of all MDAKits which have "
             "been voluntarily added to this repository. The aim of this "
             "registry is to provide sufficient details to allow others to "
             "use and potentially participate in the development of the "
             "MDAKits. Each of the following links provides more information "
             "about what the MDAKits do, how they can be installed and "
             "how to participate in their development. We also provide a set "
             "of badges which detail the current status of the MDAKits.\n\n")

    urls = []
    toctree = []

    with open('mdakits.rst', 'w') as f:
        f.write(title)
        f.write(body1)

        f.write('\n.. list-table:: List of registered MDAKits\n')
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
            write_table_entry(f, kit, urls, toctree)
            write_mdakit_page(kit)

        # write out the url data
        f.write('\n\n')

        for entry in toctree:
            f.write(entry)
        f.write('\n\n')

        for entry in urls:
            f.write(entry)
