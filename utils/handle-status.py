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
Script to combine CI statuses, raise issues and write status to file
"""
import os
import argparse
import json
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
from typing import List
from mdakit import MDAKit


parser = argparse.ArgumentParser(
    description="Combine CI statuses, raise issues and write to file",
)

parser.add_argument(
    "--maindir",
    type=str,
    help="The main MDAKit directory",
    default="./mdakits",
)

parser.add_argument(
    "--excludesubdirs",
    type=str,
    nargs="+",
    help="subdirectories to exclude from constructed mdakit list",
    default="template",
)

parser.add_argument(
    "--statusdir",
    type=str,
    help="directory where temporary json status files are stored",
    default="json-statuses",
)


def update_from_json(mdakit, jsonfile, rtype) -> None:
    with open(jsonfile) as f:
        status_dict = json.load()

    status = getattr(mdakit.status.data, rtype)

    job_fail = False
    for key, item in status_dict.items():
        item = True if item == "success" else False
        if item is False:
            job_fail = True

        setattr(status, key, item)

    if job_fail:
        status.numfails += 1

    setattr(mdakit.status.data, rtype, status)
    

def get_mdakit_list(maindir: str, excludedirs: List[str]) -> List[str]:
    path = Path(f"./{maindir}")
    mdakits = []
    for entry in path.iterdir():
        if entry.is_dir():
            var = str(entry.relative_to(f"./{maindir}"))
            if var not in excludedirs:
                mdakits.append(MDAKit(var))
    return mdakits


def handle_mdakit(maindir: str, statusdir: str,
                  mdakit, jobtypes: List[str]):
    # get the status of the recent CI build
    statuses = []
    for job in jobtypes:
        jsonfile = (f"{jsondir}/cron-statuses-{mdakit}-"
                    f"{job}/{mdakit}-{job}-statuses.json")
        update_from_json(mdakit, jsonfile, job)

    # upate the badges
    mdakit.gen_badges()

    # raise issues
    mdakit.raise_issues()

    # write out the status
    mdakit.status.write_status(mdakit.path)


if __name__ == "__main__":
    args = parser.parse_args()

    mdakits = get_mdakit_list(args.maindir, args.excludesubdirs)

    for mdakit in mdakits:
        handle_mdakit(args.maindir, args.statusdir,
                      mdakit, ['develop', 'latest'])
