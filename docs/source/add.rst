********************************
Adding an MDAKit to the Registry
********************************

Do you have an MDAKit? Consider adding it to the `MDAKit registry`_!


.. note::   
   The `MDAKit registry`_ is still in its infancy, we expect that the way in
   which MDAKits are added, and the type of information required, may change
   over time. Please reach out via the `issue tracker`_ if you have any
   questions.

Registering an MDAKit requires you to create a single file with metadata
(called ``metadata.yaml``). You add this file to the `MDAnalysis/mdakits
repository`_ on GitHub.

Process
=======

Add a MDAKit by following these steps:

1. Create a fork the MDAKit repository https://github.com/MDAnalysis/mdakits.
2. Make a new branch (choose any name, but "add-my-awesome-mdakit" is a good
   one).
3. Add a new folder under ``mdakits`` with the name of your MDAKit.
4. Add a metadata YAML file with your MDAKit's details; copy the template from
   `mdakits/template/metadata.yaml`_ and modify it. See the comments in the
   file and the :ref:`notes below<template>` for more explanations.
5. Open a Pull Request (PR) against the *main* branch of the
   `MDAnalysis/mdakits repository`_.
6. Someone from the MDAnalysis team will *review* your Pull Request for
   fulfilling the :ref:`requirements for an MDAKit<requirements>` and for any
   technical issues. They may ask for modifications so please *check your PR
   regularly* or `enable GitHub notifications`_. Part of the registration
   process is to engage in a conversation with the MDAnalysis team so please be
   responsive.
7. When your PR passes review, it will be merged and your MDAKit is registered.



.. _template:

Template ``metadata.yaml`` file
===============================

The following is the template metadata file
`mdakits/template/metadata.yaml`_. Please see the *comments in the template*
for an explanation of all possible items. You may delete or rewrite any
comments. Replace values with content appropriate for your MDAKit.

.. Note::

   The template uses the strings ``GH_HOST_ACCOUNT``,  ``MYPROJECT``, and
   ``MYPACKAGE`` to indicate that you should be filling in *your* details.

   
``GH_ACCOUNT``
   The GitHub account where he source code repository is held, typically your
   username or the organization that you're part off.

``MYPROJECT``
   The name of your project. This is name of your repository. In the template we
   assume that this is also the PyPi/conda package name but you can make them
   different.
   
``MYPACKAGE``
   The name of the Python package, it describes is how you import it in Python
   code.


   

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
   ## Here we use the simple PyPi installation:
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
   ##     pytest --pyargs MYPACKAGE.tests
   ## command as shown below. 
   ## Otherwise you need to include commands to make the tests available. 
   ## For example, if the tests are in the repository at the top level under `./tests`:
   ## First use `git clone latest` to either clone the top commit for "develop" runs or check out
   ## the latest tag for "latest release" checks. Then then run pytest:
   ##    - git clone latest
   ##    - pytest -v ./tests
   ## Feel free to ask for advice on your pull request!
   run_tests:
     - pytest --pyargs MYPACKAGE.tests
       
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
   development_status: Productions/Stable
   
   ## List(str) a list of publications to cite when using the MDAKit
   ## Links to scientific publications or stable URLs (typically of the form
   ## https://doi.org/<DOI> or to a preprint server)
   publications:
     - URL1
     - URL2
       
   ## str: a link to the MDAKit's community (mailing list, github discussions, etc...)
   community_home: URL
   
   ## str: a link to the MDAKit's changelog
   changelog: https://github.com/MYNAME/MYPROJECT/blob/main/CHANGES


.. _`issue tracker`:
   https://github.com/MDAnalysis/MDAKits/issues

.. _`MDAnalysis/mdakits repository`:
   https://github.com/MDAnalysis/mdakits
   
.. _`MDAKit registry`: https://mdakits.mdanalysis.org/mdakits.html

.. _`enable GitHub notifications`:
   https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github/setting-up-notifications/configuring-notifications

.. _`mdakits/template/metadata.yaml`:
   https://github.com/MDAnalysis/MDAKits/blob/main/mdakits/template/metadata.yaml
