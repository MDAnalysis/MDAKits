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
import os
import sys
import inspect
import importlib
from urllib import request
from pathlib import Path
import requests
from packaging import specifiers
import json
import yaml
from yaml.loader import SafeLoader
import version
from pydantic import BaseModel, validator, Extra
from typing import Dict, List, Union, Optional, Any, Iterable
from github import Github


def read_yaml(filepath):
    with open(filepath) as f:
        data = yaml.load(f, Loader=SafeLoader)
    return data


class Status:
    def __init__(self, path):
        if path.is_file():
            status = read_yaml(path)
            develop = TestStatusDict(**status['develop'])
            latest = TestStatusDict(**status['latest'])
            badges = BadgesStatusDict(**status['badges'])
            self.data = StatusData(develop, latest, badges)
        else:
            self.data = StatusData()

    def write_status(self, basepath):
        outfile = basepath / "status.yaml"
        with open(outfile, 'w') as f:
            yaml.dump(self.data.dict(), f, default_flow_style=False)


class TestStatusDict(BaseModel):
    install_python: bool = True
    install_mdakit: bool = True
    install_mdanalysis: bool = True
    install_test_deps: bool = True
    run_tests: bool = True
    numfails: int = 0


class BadgesStatusDict(BaseModel):
    coverage: bool = False
    converter: bool = False
    reader: bool = False
    writer: bool = False
    topology: bool = False
    transformation: bool = False
    analysis: bool = False


class StatusData(BaseModel):
    """
    Pydantic class to hold the mdakit status data
    """
    develop: TestStatusDict = TestStatusDict()
    latest: TestStatusDict = TestStatusDict()
    badges: BadgesStatusDict = BadgesStatusDict()

    class Config:
        extra = Extra.allow


class MetaData(BaseModel):
    """
    Pydantic class to hold the mdakit metadata.
    """
    project_name: str
    authors: List[str]
    maintainers: List[str]
    description: str
    keywords: List[str]
    license: str
    project_home: str
    python_requires: str
    documentation_home: str
    documentation_type: str
    project_org: Optional[str]
    community_home: Optional[str]
    install: Optional[List[str]] = None
    import_name: Optional[str] = None
    src_install: Optional[List[str]] = None
    run_tests: Optional[List[str]] = None
    test_dependencies: Optional[List[str]] = None
    development_status: Optional[str]
    changelog: Optional[str]
    publications: Optional[List[str]]


    # TODO: what about authors, that can also optionally be a URL
    #@validator('project_home', 'documentation_home', 'community_home',
    #           'changelog')
    #def url_exists(cls, v):
    #    if v is not None:
    #        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    #        headers = {'User-Agent': user_agent,}
    #        req = request.Request(v, None, headers)
    #        code = request.urlopen(req).getcode()
    #        if code != 200:
    #            raise ValueError(f"unreachable URL: {v}")


class MDAKit:
    def __init__(self, path):
        self.path = Path(path)
        self._read_metadata(self.path)
        self._read_status(self.path)

    def _read_metadata(self, path):
        """
        Read mdakit metadata yaml file
        """
        metadata = read_yaml(path / "metadata.yaml")

        self.metadata = MetaData(
                project_name=metadata['project_name'],
                authors=metadata['authors'],
                maintainers=metadata['maintainers'],
                description=metadata['description'],
                keywords=metadata['keywords'],
                license=metadata['license'],
                project_home=metadata['project_home'],
                python_requires=metadata['python_requires'],
                documentation_home=metadata['documentation_home'],
                documentation_type=metadata['documentation_type'],
                project_org=metadata.get('project_org', None),
                community_home=metadata.get('community_home', None),
                install=metadata.get('install', None),
                import_name=metadata.get('import_name', None),
                src_install=metadata.get('src_install', None),
                run_tests=metadata.get('run_tests', None),
                test_dependencies=metadata.get('test_dependencies', None),
                development_status=metadata.get('development_status', None),
                changelog=metadata.get('changelog', None),
                publications=metadata.get('publications', None),)

    def _read_status(self, path):
        """
        Read the status file or create one if it's missing
        """
        self.status = Status(path / "status.yaml")

    def gen_badges(self):
        try:
            badges = self._get_class_badges(self.metadata.import_name)
        except:
            badges = BadgesStatusDict()

        try:
            badges.coverage = self._get_codecov_status(
                    self.metadata.project_org,
                    self.metadata.project_name
            )
        except:
            badges.coverage = False

        self.status.data.badges = badges

    @staticmethod
    def _get_class_badges(name: Optional[str]):
        if name is None:
            return BadgesStatusDict()

        # Get all the necessary MDAnalysis classes
        from MDAnalysis.analysis.base import AnalysisBase
        from MDAnalysis.coordinates.base import ProtoReader, WriterBase, ConverterBase
        from MDAnalysis.topology.base import TopologyBase
        from MDAnalysis.transformations.base import TransformationBase

        def get_modules(mod):
            return inspect.getmembers(mod[1], inspect.ismodule)

        def get_submods(mods):
            modules = []
            submods = [get_modules(mod) for mod in mods]
            for mod in submods:
                modules.extend(mod)
            return modules

        mdakit = importlib.import_module(name)

        for mod in inspect.getmembers(sys.modules[name], inspect.ismodule):
            submod = inspect.getmembers(mod[1], inspect.ismodule)
            subsubmods = get_submods(submod)
            allmods.extend(submod)
            allmods.extend(subsubmods)

        mod_classes = [inspect.getmembers(mod[1], inspect.isclass) for mod in allmods]
        classes = []
        for i in mod_classes:
            classes.extend(i)

        badges = BadgesStatusDict()
        badges.converter = any(issubclass(i[1], ConverterBase) for i in classes)
        badges.reader = any(issubclass(i[1], ProtoReader) for i in classes)
        badges.writer = any(issubclass(i[1], WriterBase) for i in classes)
        badges.topology = any(issubclass(i[1], TopologyBase) for i in classes)
        badges.transformation = any(issubclass(i[1], TransformationBase) for i in classes)
        badges.analysis = any(issubclass(i[1], AnalysisBase) for i in classes)

        return badges

    @staticmethod
    def _get_codecov_status(orgname: Optional[str], projname: str):
        # orgname is optional
        if orgname is None:
            return False

        # Assume that codecov token is set
        token = os.environ['CODECOV_TOKEN']
        headers = {"Authorization": f"bearer {token}"}
        endpoint = f"https://codecov.io/api/v2/github/{orgname}/repos/{project_name}/commits"
        response = requests.get(endpoint, headers=headers)
        content = json.loads(response.content)
        coverage = max(commit['totals']['coverage'] for commit in content['results'])

        return coverage > 80

    def get_matching_version(self, max_ver: str = "3.11", min_ver: str = "3.8",
                             version_field: str = "python_requires"):

        version_pin = getattr(self.metadata, version_field)
        if version_pin is None:
            return max_ver

        current_version = version.TargetVersion.from_str(max_ver)
        min_version = version.TargetVersion.from_str(min_ver)
        pin_specifiers =  [specifiers.Specifier(i) for i in version_pin.split(',')]
        compatible_version = False

        while (current_version.to_version() >= min_version.to_version()):
            for spec in pin_specifiers:
                compatible_version = version._operators[spec.operator](
                        current_version.to_string(),
                        spec.version,
                )

            if compatible_version:
                break
            else:
                current_version.minor -= 1

        if not compatible_version:
            raise ValueError("Could not find compatible version which matched "
                             "the python version specs")

        return current_version.to_string()

    def raise_issues(self):
        """
        Raise issues for statuses with > 1 fails
        """
        git = Github(os.environ['GITHUB_TOKEN'])
        repo = git.get_repo('MDAnalysis/MDAKits')
        issues = [issue for issue in repo.get_issues()]

        def _bool_status(arg: bool) -> str:
            return 'passed' if argument else 'fail'

        def _create_issue(run_type: str):
            stat = getattr(self.status.data, run_type)

            # don't raise an issue if not failed at least twice
            if stat.numfails < 1:
                return

            issue_tag = f"[{self.metadata.project_name}-{run_type}]"
            issue_title = f"{issue_tag} Failed CI run"

            # quit if issue already exists
            for issue in issues:
                if issue_tag in issue.title:
                    return

            # generate list of maintainers to tag
            maint = ""
            for m in self.metadata.maintainers:
                maint += f"@{m} "

            issue_body = (
                    f"At least two repeated CI runs for "
                    f"{self.metadata.project_name} have failed.\n"
                    f"Here is the last recorded status of the tests:\n"
                    f"  - installing python: {_bool_status(stat.install_python)}\n"
                    f"  - installing the mdakit: {_bool_status(stat.install_mdakit)}\n"
                    f"  - installing mdanalysis: {_bool_status(stat.install_mdanalysis)}\n"
                    f"  - installing the test dependencies: {_bool_status(stat.install_test_deps)}\n"
                    f"  - running tests: {_bool_status(stat.run_tests)}\n"
                    f"Pinging maintainers: {maint}"
            )

            repo.create_issue(title=issue_title, body=issue_body)

        for run_type in ['latest', 'develop']:
            _create_issue(run_type)

    @staticmethod
    def _get_custom_badge(left, right, colour):
        return f"https://img.shields.io/badge/{left}-{right}-{colour}.svg"

    def gen_ci_badges(self, run_type):
        status = getattr(self.status.data, run_type)

        if ((self.metadata.run_tests is None) or
            (run_type == 'develop' and self.metadata.install is None) or
            (run_type == 'latest' and self.metadata.src_install is None)):
            return self._get_custom_badge(run_type, "unavailable", "inactive")
        elif status.numfails > 1:
            return self._get_custom_badge(run_type, "failed", "red")
        else:
            return self._get_custom_badge(run_type, "passed", "green")

    def gen_code_badges(self):
        badges = []
        
        # coverage
        if self.status.data.badges.coverage:
            badges.append(self._get_custom_badge('coverage', '> 80%', 'ff69b4'))

        if self.status.data.badges.converter:
            badges.append(self._get_custom_badge('type', 'converter', 'blue'))

        if self.status.data.badges.reader:
            badges.append(self._get_custom_badge('type', 'reader', 'blue'))

        if self.status.data.badges.writer:
            badges.append(self._get_custom_badge('type', 'writer', 'blue'))

        if self.status.data.badges.topology:
            badges.append(self._get_custom_badge('type', 'topology', 'blue'))

        if self.status.data.badges.transformation:
            badges.append(self._get_custom_badge('type', 'transformation', 'blue'))

        if self.status.data.badges.analysis:
            badges.append(self._get_custom_badge('type', 'analysis', 'blue'))

        return ' '.join(badges)

    def gen_authors(self, urls):
        if 'https' in self.metadata.authors[0]:
            auths = f"`{self.metadata.project_name} authors`_"
            urls.append(f".. _`{self.metadata.project_name} authors`:\n"
                        f"   {self.metadata.authors[0]}\n\n")
        else:
            auths = ','.join(self.metadata.authors)

        return auths

    def write_mdakit_page(self):
        name = self.metadata.project_name
        urls = []
        authors = self.gen_authors(urls)

        title = ("************************\n"
                 f"{name}\n"
                 "************************\n\n")

        description = (f"| **Description:**\n"
                       f"| *{self.metadata.description}*\n")

        keywords = f"| 🔑 **Keywords:** {', '.join(self.metadata.keywords)}\n"

        authors = f"| 🖋️ **Authors**: {authors}\n"
        project_home = f"| 🏠 **Project home:** {self.metadata.project_home}\n"
        documentation_home = f"| 📖 **Documentation:** {self.metadata.documentation_home}\n"
        license = f"| ⚖️ **License:** {self.metadata.license}\n"

        if self.metadata.development_status is not None:
            development_status = f"| 🚀 **Development status:** {self.metadata.development_status}\n"
        else:
            development_status = ""

        if self.metadata.changelog is not None:
            changelog = f"| 📜 **Changelog:** {self.metadata.changelog}\n"
        else:
            changelog = ""

        if self.metadata.publications is not None:
            publications = f"| 📑 **Publications:**\n"
            for pub in self.metadata.publications:
                publications += f"|    - {pub}\n"
        else:
            publications = ""

        latest_ci = f"| 🧪 **Tests (latest):** |{name}_latest| \n"
        develop_ci = f"| 🧪 **Tests (develop):** |{name}_develop| \n"

        urls.append(f".. |{name}_latest| image:: {self.gen_ci_badges('latest')}\n"
                    f"   :alt: {name} develop CI status\n"
                    f"   :target: https://github.com/MDAnalysis/MDAKits/actions\n\n")

        urls.append(f".. |{name}_develop| image:: {self.gen_ci_badges('develop')}\n"
                    f"   :alt: {name} develop CI status\n"
                    f"   :target: https://github.com/MDAnalysis/MDAKits/actions\n\n")

        if self.gen_code_badges() != '':
            badges = (f"| 📛 **Badges**\n"
                      f" {self.gen_code_badges()}\n")
        else:
            badges = "\n"

        if ((self.metadata.install is not None) or
            (self.metadata.src_install is not None)):
            installation_instructions = (
                "Installation instructions\n"
                "=========================\n\n"
            )

            if self.metadata.install is not None:
                installation_instructions += (
                    f"The latest version of {name} can be "
                    "installed using the following:\n\n"
                    ".. code-block:: bash\n\n"
                )
                for i in self.metadata.install:
                    installation_instructions += (
                            f"    {i}\n"
                    )
            if self.metadata.src_install is not None:
                installation_instructions += (
                    f"The source code of {name} can be "
                    "installed using the following:\n\n"
                    ".. code-block:: bash\n\n"
                )
                for i in self.metadata.src_install:
                    installation_instructions += (
                            f"    {i}\n"
                    )
            installation_instructions += "\n"
        else:
            installation_instructions = None

        with open(f"{name}.rst", "w") as kitf:
            kitf.write(f".. _{name}:\n\n")
            kitf.write(title)
            kitf.write(authors)
            kitf.write(project_home)
            kitf.write(documentation_home)
            kitf.write(license)
            kitf.write(keywords)
            kitf.write(development_status)
            kitf.write(changelog)
            kitf.write(publications)
            kitf.write(latest_ci)
            kitf.write(develop_ci)
            kitf.write(description)
            kitf.write(badges)
            kitf.write("\n\n")

            if installation_instructions is not None:
                kitf.write(installation_instructions)

            for entry in urls:
                kitf.write(entry)

    def write_table_entry(self, f, urls, toctree):
        name = self.metadata.project_name
        keywords = ', '.join(self.metadata.keywords)
        authors = self.gen_authors(urls)
        ci_latest = f"|{name}_latest|"
        ci_develop = f"|{name}_develop|"

        urls.append(f".. |{name}_latest| image:: {self.gen_ci_badges('latest')}\n"
                    f"   :alt: {name} develop CI status\n"
                    f"   :target: https://github.com/MDAnalysis/MDAKits/actions\n\n")

        urls.append(f".. |{name}_develop| image:: {self.gen_ci_badges('develop')}\n"
                    f"   :alt: {name} develop CI status\n"
                    f"   :target: https://github.com/MDAnalysis/MDAKits/actions\n\n")

        f.write(f'    * - :ref:`{name}`\n')
        f.write(f'      - {keywords}\n')
        f.write(f'      - {authors}\n')
        f.write(f'      - {ci_latest} {ci_develop}\n')
        toctree.append(f'   {name}\n')

    def get_install(self, install_type):
        if install_type == "src":
            if self.metadata.src_install is None:
                return ""
            else:
                return ';'.join(self.metadata.src_install)
        else:
            if self.metadata.install is None:
                return ""
            else:
                return ';'.join(self.metadata.install)

    def get_test_deps(self):
        if self.metadata.test_dependencies is None:
            return ""

        return ';'.join(self.metadata.test_dependencies)

    def get_run_tests(self, runtype):
        if self.metadata.run_tests is None:
            return ""

        test_steps = []
        for step in self.metadata.run_tests:
            # special case for cloning the latest tag
            if step == "git clone latest":
                test_steps.append(f'git clone {self.metadata.project_home}.git && cd "$(basename "$_" .git)"')
                if runtype == "latest":
                    test_steps.append("git fetch --tags")
                    test_steps.append("latestTag=$(git describe --tags `git rev-list --tags --max-count=1`)")
                    test_steps.append("git checkout $latestTag")
            else:
                test_steps.append(step)

        return ';'.join(test_steps)
