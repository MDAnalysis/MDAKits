************************************
Part 1: Using the MDAKit cookicutter
************************************

*For a video demonstration of this section,* 
`click here  <https://www.youtube.com/watch?v=viCPUHkgSxg&t=38s>`_.

The MDAKits cookiecutter (a
`Cookiecutter tool <https://cookiecutter.readthedocs.io/en/stable/>`_)
can be used to rapidly develop a FAIR-compliant MDAKit by generating
placeholder code for documentation, testing and installation. 

More infromation on its usage is can be found in the 
`MDAKit cookiecutter documentation <https://cookiecutter-mdakit.readthedocs.io/en/latest/>`_,
but in short, using the cookiecutter involves running a command line
prompt and then responding to a set of subsequent prompts. You will 
need Python 3.10+ and the 
`Cookiecutter tool <https://cookiecutter.readthedocs.io/en/stable/>`_ installed.

In this example, we use the cookiecutter as follows to generate 
a new MDAKit template ``rmsfkit``. Some prompts are left
blank, accepting the the default option.

.. code-block:: bash

	$ cookiecutter gh:MDAnalysis/cookiecutter-mdakit

	project_name (ProjectName): rmsfkit
	repo_name (rmsfkit): 
	package_name (rmsfkit): 
	description (A short description of the project.): A package to perform RMSF analysis on molecular dynamics data.
	github_username (Your personal GitHub username): myusername
	github_host_account (GitHub account for hosting rmsfkit (e.g. myusername or an organization account). Press Enter to use myusername): 
	author_name (Your name (or your organization/company/team)): Firstname Lastname
	author_email (Your email (or your organization/company/team)): myemail@email-provider.com
	Select dependency_source:
	1 - Prefer conda-forge over the default anaconda channel with pip fallback
	2 - Prefer default anaconda channel with pip fallback
	3 - Dependencies from pip only (no conda)
	Choose from [1/2/3] (1): 
	Select include_ReadTheDocs:
	1 - y
	2 - n
	Choose from [1/2] (1): 
	template_analysis_class (Class name to template (e.g. Rmsfkit ). Press Enter to skip including analysis templates):

This generates a new git repository named ``rmsfkit`` (note, the 
author of the initial commit will match that of the user's global git 
configurations).

Navigating into this directory, we find a number of files and 
subdirectories. The 
`cookiecutter documentation <https://cookiecutter-mdakit.readthedocs.io/en/latest/usage.html>`_
provides more information on these, but those to take note of now 
include:

- ``LICENSE`` -- a text file containing the license information (GLPv2+ by default)
- ``AUTHORS.md`` -- a template text file for listing code authors as each 
  new contribution is made. Auto-populated with your name as the 
  initial project creator.
- ``README.md`` -- a text file containing the project description and other 
  useful information; typically landing page content rendered on GitHub.
- ``pyproject.toml`` - a configuration file with information for 
  packaging (and other tools).
- ``rmsfkit/`` -- template for the python package source code, i.e. 
  where your code (and tests) will live.
- ``CODE_OF_CONDUCT.md`` and ``CONTRIBUTING.md`` -- text files containing
  community guidelines and instructions on reporting issues and contributing
  (once the code is hosted on GitHub).
- ``docs/`` -- folder containing documentation template, instructions
  and build environment documented within.

We'll address other files as they come up in subsequent parts.


** Progress: MDAKit requirementsi**

#. *Uses MDAnalysis* 
#. **✓ Open source + OSI license** -- the default GPLv2 license falls
   under OSI. If you wish to choose another license, you can replace
   the default LICENSE file with another. See :ref:`<licensing>` for more.
#. *Versioned + on a version-controlled repository* -- the cookiecutter has
   set up versioning with git; in a later step, we'll add it to the the
   GitHub repository.
#. **✓ Designated authors and maintainers** -- in the generated AUTHORS.md 
   file, assuming that the maintained and author are the same person. 
   More authors will be added as the project evolves. 
#. *(At least) minimal documentation* -- the generated README.md file 
   provides a form of minimal documentation; however, we will be adding 
   more documentation in a later step. 
#. *(At least) minimal regression tests*
#. **✓ Installable as a standard package** -- through `rmsfkit/` and 
   `pyproject.toml`.
#. **✓ (Recommended) community information available** -- provided with
   CODE_OF_CONDUCT.md and CONTRIBUTING.md. Adjust these files to suit your 
   needs.
#. *(Recommended) on a package distribution platform*
