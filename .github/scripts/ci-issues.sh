#!/usr/bin/env bash
# Raise issues for mdakits with failing CI runs and close them once fixed.
# Reads the status.yaml files written by utils/handle-status.py.
# Requires: gh (with GH_TOKEN set), jq, yq
set -euo pipefail

maindir="${1:-mdakits}"

open_issues=$(gh issue list --state open --limit 1000 --json number,title)

bool_status() {
    [[ "$1" == "true" ]] && echo "passed" || echo "fail"
}

for kitdir in "$maindir"/*/; do
    # template isn't a real kit; kits without a status file haven't run yet
    [[ "$(basename "$kitdir")" == "template" ]] && continue
    [[ -f "$kitdir/status.yaml" ]] || continue

    name=$(yq '.project_name' "$kitdir/metadata.yaml")

    for run_type in latest develop; do
        tag="[${name}-${run_type}]"
        numfails=$(yq ".${run_type}.numfails // 0" "$kitdir/status.yaml")

        issue=$(jq -r --arg tag "$tag" \
            'first(.[] | select(.title | contains($tag)) | .number) // empty' \
            <<< "$open_issues")

        if [[ -n "$issue" ]]; then
            # clear issues if resolved
            if (( numfails == 0 )); then
                gh issue close "$issue" --comment "CI for ${name} (${run_type}) is passing again."
            fi
            continue
        fi

        if (( numfails < 1 )); then
            continue
        fi

        status() {
            bool_status "$(yq ".${run_type}.$1" "$kitdir/status.yaml")"
        }
        maint=$(yq '.maintainers | map("@" + .) | join(" ")' "$kitdir/metadata.yaml")

        gh issue create --title "${tag} Failed CI run" --body-file - <<EOF
At least two repeated CI runs for ${name} have failed.
Here is the last recorded status of the tests:
  - installing python: $(status install_python)
  - installing the mdakit: $(status install_mdakit)
  - installing mdanalysis: $(status install_mdanalysis)
  - installing the test dependencies: $(status install_test_deps)
  - running tests: $(status run_tests)
Pinging maintainers: ${maint}

---
**How to resolve this:**

- **Check the \`metadata.yaml\`**: Ensure your kit's \`metadata.yaml\` is up-to-date.
- **Check why the pipeline is failing**: Look at the CI logs to find the exact point of failure. See the [documentation on finding the CI error](https://mdakits.mdanalysis.org/maintaining_a_kit/keep-healthy.html#why-did-ci-fail).
- **Pipeline details**: For an in-depth explanation of how the MDAKits Registry CI works, please see [the documentation here](https://mdakits.mdanalysis.org/maintaining_a_kit/keep-healthy.html#mdakitsci).
EOF
    done
done
