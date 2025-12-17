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
    """
    Class to handle status information for a given MDAKit
    """
    def __init__(self, path):
        """
        Reads in and stores the status.yaml file information for an MDAKit.


        Parameters
        ----------
        path : pathlib.Path
            Path to the status yaml file.


        Note
        ----
        * Should there be no status.yaml file, a blank set of information will
          be generated.
        """
        if path.is_file():
            status = read_yaml(path)
            develop = TestStatusDict(**status['develop'])
            latest = TestStatusDict(**status['latest'])
            badges = BadgesStatusDict(**status['badges'])
            self.data = StatusData(develop=develop, latest=latest, badges=badges)
        else:
            self.data = StatusData()

    def write_status(self, basepath):
        """
        Write out a status.yaml based on the current contents of the
        Status class.


        Parameters
        ----------
        basepath : pathlib.Path
            Location where to write a status.yaml file.
        """
        outfile = basepath / "status.yaml"
        with open(outfile, 'w') as f:
            yaml.dump(self.data.dict(), f, default_flow_style=False)


class TestStatusDict(BaseModel):
    """
    Pydantic class to hold test status results
    """
    install_python: bool = True
    install_mdakit: bool = True
    install_mdanalysis: bool = True
    install_test_deps: bool = True
    run_tests: bool = True
    numfails: int = 0


class BadgesStatusDict(BaseModel):
    """
    Pydantic class to hold badge status results
    """
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
    run_tests: Union[List[str], Dict[List[str]], None] = None
    test_dependencies: Union[List[str], Dict[List[str]], None] = None
    development_status: Optional[str]
    changelog: Optional[str]
    publications: Optional[List[str]]


    # TODO LIST:
    #   * what about authors, that can also optionally be a URL
    #   * validate github handles for maintainers
    #   * validate github repositories
    #   * validate publications
    @validator('project_home', 'documentation_home', 'community_home',
               'changelog')
    def url_exists(cls, v):
        if v is not None:
            try:
                response = requests.get(v)
            except requests.ConnectionError as e:
                raise ValueError(f"unreachable URL: {v}")

    @validator('run_tests', 'test_dependencies')
    def optional_dictionaries(cls, v):
        if isinstance(v, dict):
            for entry in ['latest', 'develop']:
                assert entry in v.keys(), f"{entry} not key in {v}"


class MDAKit:
    def __init__(self, path):
        """
        Create the MDAKit object. Feed in the metadata and status YAML files.


        Parameters
        ---------
        path : str
            A path to the mdakit directory location
        """
        self.path = Path(path)
        self._read_metadata(self.path)
        self._read_status(self.path)

    def _read_metadata(self, path):
        """
        Read mdakit metadata yaml file.


        Parameters
        ----------
        path : pathlib.Path
            A path to the MDAKit directory entry.
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
        Read the status file or fill in an empty Status ojbect if missing.


        Parameters
        ----------
        path : pathlib.Path
            A path to the MDAKit directory entry.
        """
        self.status = Status(path / "status.yaml")

    def gen_badges(self):
        """
        Generate badges for the MDAKit.

        Currently this will:
          * Try to work out the MDAnalysis base classes being used by the code.
            * Needs to have `import_name` defined in the metadata yaml file.
          * Read in the current codecov status for the project.
            * Needs to have `project_org` and `project_name` defined in the
              yaml file.

        TODO:
        -----
        * For mysterious reasons this is currently broken and needs fixing.
        """
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
        """
        Uses `inspect` to check (up to 3 layers down), if there are any objects
        in the MDAKit that subclasses one of the following MDAnalysis base
        classes:
          * AnalysisBase
          * ProtoReader
          * WriterBase
          * ConverterBase
          * TopologyBase
          * TransformationBase
        """
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
        """
        Uses the codecov API to fetch coverage data for the MDAKit.
        """
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
        """
        Find a version that matches both the input range (defined by `max_ver`
        and `min_ver`) and the range version for the `version_field` entry in
        the MDAKit metadata.
        """

        version_pin = getattr(self.metadata, version_field)
        if version_pin is None:
            return max_ver

        current_version = version.TargetVersion.from_str(max_ver)
        min_version = version.TargetVersion.from_str(min_ver)
        pin_specifiers =  [specifiers.Specifier(i) for i in version_pin.split(',')]
        compatible_version = False

        while (current_version.to_version() >= min_version.to_version()):
            for spec in pin_specifiers:
                # Fetch the pin version string and convert it for comparison
                pin_ver = version.TargetVersion.from_str(spec.version)
                compatible_version = version._operators[spec.operator](
                        current_version.to_version(),
                        pin_ver.to_version(),
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
        Raise issues in MDAKit repository for statuses with > 1 fails.
        """
        git = Github(os.environ['GITHUB_TOKEN'])
        repo = git.get_repo('MDAnalysis/MDAKits')
        issues = [issue for issue in repo.get_issues()]

        def _bool_status(arg: bool) -> str:
            return 'passed' if arg else 'fail'

        def _create_issue(run_type: str):
            stat = getattr(self.status.data, run_type)

            issue_tag = f"[{self.metadata.project_name}-{run_type}]"
            issue_title = f"{issue_tag} Failed CI run"

            # quit if issue already exists
            for issue in issues:
                if issue_tag in issue.title:
                    # clear issues if resolved
                    if stat.numfails == 0:
                        issue.edit(state="closed")
                    return

            # if numfails < 1 and you've not done so yet return
            if stat.numfails < 1:
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
        """
        Private method to create a custom badge using img.shields.io

        Parameters
        ----------
        left : str
          Text to be stored on the left side of the badge
        right : str
          Text to be stored on the right side of the badge
        color : str
          img.shields.io compatible color for the badge status
        """
        return f"https://img.shields.io/badge/{left}-{right}-{colour}.svg"

    def gen_ci_badges(self, run_type):
        """
        Create a badge for the CI outcomes of a particular run type.

        Parameters
        ----------
        run_type : str
          Either `latest` or `develop`, indicates the run type for which a
          badge should be created.


        Returns
        -------
        str
          Link to a custom img.shields.io badge for the status of the CI run.
        """
        status = getattr(self.status.data, run_type)

        if ((self.metadata.run_tests is None) or
            (run_type == 'develop' and self.metadata.src_install is None) or
            (run_type == 'latest' and self.metadata.install is None)):
            return self._get_custom_badge(run_type, "unavailable", "inactive")
        elif status.numfails > 1:
            return self._get_custom_badge(run_type, "failed", "red")
        else:
            return self._get_custom_badge(run_type, "passed", "green")

    def gen_code_badges(self):
        """
        Generate achivement badges for the MDAKit based on the badge data
        currently stored under `self.data.badges`.
        """
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
        """
        Create an authors entry for the MDAKit docs.


        Parameters
        ----------
        urls : List[str]
          A list of url entries so that sphinx knows how to link things
          correctly.
        """
        if 'https' in self.metadata.authors[0]:
            auths = f"`{self.metadata.project_name} authors`_"
            urls.append(f".. _`{self.metadata.project_name} authors`:\n"
                        f"   {self.metadata.authors[0]}\n\n")
        else:
            auths = ', '.join(self.metadata.authors)

        return auths

    def write_mdakit_page(self):
        """
        Write a ReST docs entry for the MDAKit giving a summary of current
        status.
        """
        name = self.metadata.project_name
        urls = []
        authors = self.gen_authors(urls)

        title = ("************************************************\n"
                 f"{name}\n"
                 "************************************************\n\n")

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
                publications += f"|    * {pub}\n"
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
                    f"\nThe source code of {name} can be "
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
        """
        Write out a table entry for the MDAKits searchable summary table.
        """
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
        """
        Get shell appropriate install instructions for the MDAKit.


        Parameters
        ----------
        install_type : str
          If `src` will pass back source installation instructions, otherwise
          will pass back the standard installation instructions.

        Returns
        -------
        str
          Shell executable string of installation instructions.
        """
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

    def get_test_deps(self, runtype=None):
        """
        Get a list of test dependency install instructions.


        Parameters
        ----------
        runtype : Optional[str]
          Either `latest` or `develop`, if `self.metadata.test_dependencies`
          is a dictionary, will attempt to read list from the corresponding
          key.


        Returns
        -------
        str :
          Semi-colon separated list of install instructions which can be
          executed from shell.
        """
        if self.metadata.test_dependencies is None:
            return ""

        if isinstance(self.metadata.test_dependencies, dict):
            return ';'.join(self.metadata.test_dependencies[run_type])
        else:
            return ';'.join(self.metadata.test_dependencies)

    def get_run_tests(self, runtype=None):
        """
        Get a list of test dependency install instructions.


        Parameters
        ----------
        runtype : Optional[str]
          Either `latest` or `develop`, if `self.metadata.run_tests`
          is a dictionary, will attempt to read list from the corresponding
          key.


        Returns
        -------
        str :
          Semi-colon separated list of test run instructions which can be
          executed from shell.

        """
        if self.metadata.run_tests is None:
            return ""

        if ((runtype == "latest" and self.metadata.install is None) or
            (runtype == "develop" and self.metadata.src_install is None)):
            return ""

        if isinstance(self.metadata.run_tests, dict):
            run_tests = self.metadata.run_tests[runtype]
        else:
            run_tests = self.metadata.run_tests

        test_steps = []
        for step in run_tests:
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
