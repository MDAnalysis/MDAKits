"""
A script to plot the number of packages registered over time.

You will need the following packages installed:
- PyGithub
- numpy
- pandas
- seaborn
- matplotlib

You will need a GitHub token with access to the repository to run this script.
The token should be stored in the environment variable `GH_TOKEN`.
"""
import argparse
import datetime
import re
import os

import numpy as np
import pandas as pd
from github import Github

import seaborn as sns
import matplotlib.dates as mdates
from matplotlib import pyplot as plt

REPO_NAME = "mdanalysis/MDAKits"
GITHUB_TOKEN = os.environ["GH_TOKEN"]

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--verbose",
    action="store_true",
    help="Print the DataFrame of results",
)

def find_prs_with_file(repo_name, github_token):
    """
    Find all pull requests that added a `metadata.yaml` file to the repository.
    """
    pattern = re.compile(r"metadata\.yaml$")
    
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    
    prs_with_file = []

    # Iterate through all pull requests in the repository
    for pr in repo.get_pulls(state='closed'):
        # Check if the PR was merged
        if pr.merged_at is None:
            continue

        # Check files changed in the PR
        # look for addition of a `metadata.yaml` file
        # so we ignore updates and changes to the metadata
        files = pr.get_files()
        for file in files:
            if file.status == 'added' and re.search(pattern, file.filename):
                # mostly these attributes are for debugging
                prs_with_file.append({
                    'pr_number': pr.number,
                    'pr_title': pr.title,
                    'merged_at': pr.merged_at,
                    'html_url': pr.html_url
                })
                break

    return prs_with_file


def main(
    verbose: bool = False,
):
    """
    Main function to plot the number of packages registered over time.
    """
    results = find_prs_with_file(REPO_NAME, GITHUB_TOKEN)
    df = pd.DataFrame(results)
    df_cumsum = df.sort_values("merged_at")
    df_cumsum["Number of MDAKits"] = np.arange(len(df)) + 1

    if verbose:
        print(df_cumsum)

    _, ax = plt.subplots(figsize=(4, 3))
    ax = sns.lineplot(
        ax=ax,
        data=df_cumsum,
        x="merged_at",
        y="Number of MDAKits"
    )

    ax.set_xlim((
        datetime.date(2023, 1, 1),
        datetime.date(2024, 11, 30)
    ))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
    ax.set_xlabel("Added to registry")
    ax.set_ylabel("Number of MDAKits")
    ax.set_title("MDAKits Registry Growth")
    plt.tight_layout()
    plt.savefig("mdakits-registry-growth.png", dpi=300)
    print("Saved plot to mdakits-registry-growth.png")


if __name__ == "__main__":
    args = parser.parse_args()
    main(verbose=args.verbose)
