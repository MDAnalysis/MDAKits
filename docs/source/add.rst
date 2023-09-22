********************************
Adding an MDAKit to the Registry
********************************

Do you have an MDAKit? Consider adding it to the `MDAKit registry`_!


.. note::   
   The `MDAKit registry`_ is still in its initial stages. We expect that the way in
   which MDAKits are added, and the type of information required, may change
   over time. Please reach out via the `issue tracker`_ if you have any
   questions.

Registering an MDAKit requires you to create a single file with metadata
(called ``metadata.yaml``). You add this file to the `MDAnalysis/mdakits
repository`_ on GitHub.

Process
=======

Add a MDAKit by following these steps:

#. Create a fork the MDAKit repository https://github.com/MDAnalysis/mdakits.
#. Make a new branch (choose any name, but "add-my-awesome-mdakit" is a good
   one).
#. Add a new folder under ``mdakits`` with the name of your MDAKit.
#. Add a metadata YAML file with your MDAKit's details; copy the template from
   `mdakits/template/metadata.yaml`_ and modify it. See the comments in the
   file and the :ref:`notes below<template>` for more explanations.
#. Create a Pull Request (PR) from your branch against the *main*
   branch of the `MDAnalysis/mdakits repository`_. Add a title with
   the name of the kit (e.g. "register MyAwesomeTool") and add a short
   description.

   A number of tests should automatically start to run.
#. Wait for the tests to pass (i.e., all results should be green and
   pass).

   * If there are problems at this stage (tests don't pass and you don't
     know where to start fixing the problem), add a comment to your PR
     with the text

        *@MDAnalysis/mdakits-reviewers please help with tests.*

     in order to notify the MDAnalysis team that you need assistance
     with fixing your submission.
   * If the tests passed, add a comment to your PR with the text

        *@MDAnalysis/mdakits-reviewers, ready for review.*

#. Someone from the MDAnalysis team will *review* your Pull Request for
   fulfilling the :ref:`requirements for an MDAKit<requirements>` and for any
   technical issues.

   They may ask for modifications so please *check your PR regularly*
   or `enable GitHub notifications`_. Part of the registration process
   is to engage in a conversation with the MDAnalysis team. The PR
   cannot be merged until all relevant questions have been addressed.
#. When your PR passes review, it will be merged and your MDAKit is registered.
#. Remember: **You remain responsible for maintaining your code**. The
   registry (and MDAnalysis) continuously test your code but the
   MDAnalysis team cannot fix it for you.

   .. Note:: 

      The registry will alert you via GitHub issues when your tests
      start failing with newer versions of MDAnalysis or other
      dependencies. In this case **please fix your code and make a new
      release of your code**.  

      
Specification of the ``metadata.yaml`` file
===========================================

The ``metadata.yaml`` file is in `YAML format`_.

The file contains required and optional entries.

**Required entries**
   Any variable in the *Required entries* section **must** be
   provided. If missing or empty, the MDAKit cannot be registered.

**Optional entries**
   Any variable in the *Optional entries* section **may** be left
   empty or be left out. However, it is recommended to provide as much
   information as possible.


.. Note::    

   For now, the :ref:`template file<template>` serves as the primary
   specification for the MDAKits registry ``metadata.yaml`` file.  The
   MDAKits registry specification will likely be updated in the future
   and some of the optional entries may become required.


      
.. _template:

Template ``metadata.yaml`` file
===============================

The following is the template metadata file
`mdakits/template/metadata.yaml`_. Please see the *comments in the template*
for an explanation of all possible items. Replace values with content
appropriate for your MDAKit.

.. Note::

   The template uses the strings ``GH_HOST_ACCOUNT``,  ``MYPROJECT``, and
   ``MYPACKAGE`` to indicate that you should be filling in *your* details.

   
``GH_ACCOUNT``
   The GitHub account where the source code repository is held; typically your
   username or the organization that you're part of.

``MYPROJECT``
   The name of your project. This is the name of your repository. In the template we
   also use it as the PyPi/conda package name.
   
``MYPACKAGE``
   The name of the Python package. It describes how you import it in Python
   code, i.e. it is used in ``import MYPACKAGE``.

The file is in `YAML format`_ so please look at the latest
specifications to learn more about how to write correct YAML
files. Typically you should be able to get started by modifying the
template. Note that YAML is a file format where indentation matters so
make sure that your editor uses spaces and not TAB for indentation as
this can lead to incorrect YAML. Lines starting with hash marks ``#``
are comments. You can add your own comments and modify the existing
ones as needed.

The comments in the template file indicate two sections. The first
one contains all **required entries**, the second one all **optional
entries**.


.. code-block:: yaml

   # TEMPLATE MDAKit file
   # ====================
   #
   #------------------------------------------------------------
   # Required entries
   #------------------------------------------------------------
   ## str: name of the project (the respository name)
   project_name: MYPROJECT
   
   ## List(str): a link to the authors file (preferred) or a list of authors 
   authors:
     - https://github.com/GH_HOST_ACCOUNT/MYPROJECT/blob/main/AUTHORS
       
   ## List(str): a list of maintainers
   maintainers:
     - NAME1
     - OPTIONAL_NAME2
     - OPTIONAL_NAME3
       
   ## str: a free form description of the mdakit
   description:
       (REPLACE WITH A SHORT DESCRIPTION OF WHAT YOUR MDAKit DOES.)
       
   ## List(str): a list of keywords which describe the mdakit
   keywords:
     - KEYWORD1
     - KEYWORD2
       
   ## str: the license the mdakit falls under
   license: GPL-2.0-or-later
   
   ## str: the link to the project's code
   project_home: https://github.com/GH_HOST_ACCOUNT/MYPROJECT/
   
   ## str: the link to the project's documentation
   documentation_home: https://MYPROJECT.readthedocs.io
   
   ## str: the type of documentation available [UserGuide, API, README]
   documentation_type: UserGuide + API

   #------------------------------------------------------------
   # Optional entries
   #------------------------------------------------------------   
   ## List(str): a list of commands to use when installing the latest
   ## release of the code. Note: only one installation method can currently
   ## be defined. We suggest using mamba where possible (e.g.
   ##   mamba -c conda-forge install MYPROJECT
   ## for a conda package installation).
   ## Here we use a simple PyPi installation:
   install:
     - pip install MYPROJECT
       
   ## List(str): a list of commands to use when installing the mdakit from its
   ## source code.
   src_install:
     - pip install git+https://github.com/GH_HOST_ACCOUNT/MYPROJECT@main
       
   ## str: the package name used to import the mdakit
   import_name: MYPACKAGE
   
   ## str: a specification for the range of Python versions supported by this MDAKit
   python_requires: ">=3.9"
   
   ## str: a specification for the range of MDAnalysis versions supported by this MDAKit
   mdanalysis_requires: ">=2.0.0"
   
   ## List(str): a list of commands to use when attempting to run the MDAKit's tests
   ## If you package your tests inside your package then you can typically use the 
   ##     pytest --pyargs MYPACKAGE
   ## command as shown below. 
   ## Otherwise you need to include commands to make the tests available. 
   ## For example, if the tests are in the repository at the top level under `./tests`:
   ## First use `git clone latest` to either clone the top commit for "development code" checks or check out
   ## the latest tag for "latest release" checks. Then then run pytest:
   ##    - git clone latest
   ##    - pytest -v ./tests
   ## Feel free to ask for advice on your pull request!
   run_tests:
     - pytest --pyargs MYPACKAGE
       
   ## List(str): a list of commands to use to install the necessary dependencies required
   ## to run the MDAKit's tests.
   ## The default below _might_ be sufficient or you might not even need MDAnalysisTests:
   ## make sure that it is appropriate for how you run tests.
   test_dependencies:
     - mamba install pytest MDAnalysisTests
       
   ## str: the organisation name the MDAKit falls under
   project_org: GH_HOST_ACCOUNT
   
   ## str: the development status of the MDAKit
   ## See https://pypi.org/classifiers/ for development status classifiers.
   development_status: Production/Stable
   
   ## List(str) a list of publications to cite when using the MDAKit
   ## Links to scientific publications or stable URLs (typically of the form
   ## https://doi.org/<DOI> or to a preprint server)
   publications:
     - URL1
     - URL2
       
   ## str: a link to the MDAKit's community (mailing list, github discussions, etc...)
   community_home: URL
   
   ## str: a link to the MDAKit's changelog
   changelog: https://github.com/MYNAME/MYPROJECT/blob/main/CHANGELOG.md


.. _`issue tracker`:
   https://github.com/MDAnalysis/MDAKits/issues

.. _`MDAnalysis/mdakits repository`:
   https://github.com/MDAnalysis/mdakits
   
.. _`MDAKit registry`: https://mdakits.mdanalysis.org/mdakits.html

.. _`enable GitHub notifications`:
   https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github/setting-up-notifications/configuring-notifications

.. _`mdakits/template/metadata.yaml`:
   https://github.com/MDAnalysis/MDAKits/blob/main/mdakits/template/metadata.yaml

.. _YAML format: https://yaml.org/   
