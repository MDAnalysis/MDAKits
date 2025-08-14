###################################
Packaging, deployments and releases
###################################

Packaging
=========
What is is?
-----------
- Group everything your code needs so it's easy for users to grab + install
    the code, dependencies, license
- Important terms: 'source install', dependencies (+pinning), 'package distribution platforms'
   'package manager', (deployment, versioning, releases - expanded below)
- Highlight: a git repository vs. a repository of packages
- Relevant: dependencies - support windows

Why is it important?
--------------------
- specifying versions, installing these automatically ('resolve dependencies')

How is it done?
---------------
- Python package: __init__.py
    Installable: pyproject.toml/(setup.py)
- PyPI + conda-forge
   (basic overview how/links to the relevant pages)
Link to relevant cookiecutter bits


Licensing
=========
*take from existing license page*

What is it?
-----------
- legal statement about who owns + who can use the code/how

Why is it important?
--------------------

How is it done?
---------------
- LICENSE file, link to licenses


Deployments and releases
========================
What is it?
-----------
- A particular 'state' of a software package + making it available
- Important terms: version number+semantic versioning, release notes

More details:
- What goes in release notes; CHANGELOG
- Not making 'breaking changes' straight away + notifying of upcoming changes 
- when to make releases - stable release vs. nightly builds

Why is it important?
--------------------

How is it done?
---------------
- versioningit/versioneer
- e.g. using git tags + releasing w/ github
    link to relevant sections of cookiecutter; MDA userguide
- Publishing new versions to PyPI/conda-forge; automatic pipelines
Links to relevant cookiecutter bits
