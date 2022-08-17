import os
import argparse
import json
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
from typing import List
from github import Github


git = Github(os.environ['GITHUB_TOKEN'])


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


class Status:
    def __init__(self, jobtype: str, jsonfile: str, yamlfile: str):
        self.jobtype = jobtype
        # read the numfailures from the yaml
        self.numfails = self._numfails_from_yaml(jobtype, yamlfile)

        # read inputs from json
        self._read_from_json(jsonfile)

    @staticmethod
    def _numfails_from_yaml(jobtype: str, yamlfile: str) -> int:
        try:
            with open(yamlfile) as f:
                prev_status = yaml.load(f, Loader=SafeLoader)
            return prev_status[jobtype]['numfails']
        except FileNotFoundError:
            return 0

    def _read_from_json(self, jsonfile: str) -> None:
        with open(jsonfile) as f:
            status_dict = json.load(f)

        curr_job_fail = False

        for key, item in status_dict.items():
            item = True if item == "success" else False

            if item is False:
                curr_job_fail = True

            setattr(self, 'key', item)

        if curr_job_fail:
            self.numfails += 1

    def to_dict(self):
        return {self.jobtype: {
            'numfails': self.numfails,
            'install_python': self.install_python,
            'install_mdakit': self.install_mdakit,
            'install_mda': self.install_mda,
            'install_test_deps': self.install_test_deps,
            'run_tests': self.run_tests, }}


def get_mdakit_list(maindir: str, excludedirs: List[str]) -> List[str]:
    path = Path(f"./{maindir}")
    mdakits = []
    for entry in path.iterdir():
        if entry.is_dir():
            var = str(entry.relative_to(f"./{maindir}"))
            if var not in excludedirs:
                mdakits.append(var)
    return mdakits


def handle_mdakit(maindir: str, jsondir: str,
                  mdakit: str, jobtypes: List[str]):
    # get the status of the recent CI build
    statuses = []
    for job in jobtypes:
        jsonfile = (f"{jsondir}/cron-statuses-{mdakit}-"
                    f"{job}/{mdakit}-{job}-statuses.json")
        yamlfile = f"{maindir}/{mdakit}/status.yaml"
        statuses.append(Status(job, jsonfile, yamlfile))

    # scan through statuses and raise an issue if necessary
    for status in statuses:
        if status.numfails > 1:
            raise_issue(mdakit, status)

    # write the issues out
    write_mdakit_status(maindir, mdakit, statuses)


def raise_issue(maindir: str, mdakit: str, status):
    """Raise an issue for a failed status if an issue doesn't already exist.
    """
    issue_tag = f"[{mdakit}-{status.jobtype}]"
    repo = git.get_repo('MDAnalysis/MDAKits')
    issues = [issue for issue in repo.get_issues()]

    for issue in issues:
        if issue_tag in issue.title:
            return

    # Get maintainers
    with open(f'{maindir}/{mdakit}/metadata.yaml') as f:
        metadata = yaml.load(f, Loader=SafeLoader)

    maintainers = mdatadata['maintainers']

    issue_title = f"{issue_tag} Failed CI run"

    # write issue body
    def bool_status(argument: bool) -> str:
        return 'passed' if argument else 'fail'

    issue_body = (f"At least two repeated CI runs for {mdakit} have failed.\n "
                  "Here is last recorded status of the tests:\n"
                  f"  - installing python: {bool_status(status.install_python)}\n"
                  f"  - installing the mdakit: {bool_status(status.install_mdakit)}\n"
                  f"  - installing the test dependencies: {bool_status(status.install_test_deps)}\n"
                  f"  - running tests: {bool_status(status.run_tests)}\n"
                  f"Pinging maintainers: {' '.join(maintainers)}")

    # raise issue - TODO use labels
    repo.create_issue(title=issue_title, body=issue_body)


def write_mdakit_status(maindir: str, mdakit: str, statuses):
    # combine the two dictionaries and write out a yaml file
    outfile = f"{maindir}/{mdakit}/status.yaml"

    fullstatus = {}

    for status in statuses:
        fullstatus.update(status.to_dict())

    with open(outfile, 'w') as f:
        yaml.dump(fullstatus, f, default_flow_style=False)


if __name__ == "__main__":
    args = parser.parse_args()

    mdakits = get_mdakit_list(args.maindir, args.excludesubdirs)

    for mdakit in mdakits:
        handle_mdakit(args.maindir, args.statusdir,
                      mdakit, ['develop', 'latest'])
