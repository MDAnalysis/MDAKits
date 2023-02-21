********************************
Adding an MDAKit to the Registry
********************************

Do you have an MDAKit? Consider adding it to the Registry!


.. note::
   The MDAKit registry is still in its infancy, we expect that the
   way in which MDAKits are added, and the type of information required,
   may change over time. Please reach out via the `issue tracker`_ if you
   have any questions.


Adding an MDAKit is a simple process, and follows the following steps:
  * Create a fork the MDAKit repository
  * Make a new branch
  * Add a new folder under ``mdakits`` with the name of your MDAKit
  * Add a metadata YAML file with your MDAKit's details (a template can be found under ``mdakits/template``)


An example ``metadata.yaml`` file
=================================

The following is an example metadata file for propkatraj::

    # Required entries
    ## str: name of the project (the respository name)
    project_name: propkatraj
    ## List(str): a list of authors (or a link to the authors file)
    authors:
      - https://github.com/Becksteinlab/propkatraj/blob/main/AUTHORS
    ## List(str): a list of maintainers
    maintainers:
      - ianmkenney
      - IAlibay
      - orbeckst
    ## str: a free form description of the mdakit
    description:
        pKa estimates for proteins using an ensemble approach
    ## List(str): a list of keywords which describe the mdakit
    keywords:
      - pKa
      - protein
    ## str: the license the mdakit falls under
    license: GPL-2.0-or-later
    ## str: the link to the project's code
    project_home: https://github.com/Becksteinlab/propkatraj/
    ## str: the link to the project's documentation
    documentation_home: https://becksteinlab.github.io/propkatraj/
    ## str: the type of documentation available [UserGuide, API, README]
    documentation_type: UserGuide + API

    # Optional entries
    ## List(str): a list of commands to use when installing the latest
    ## release of the code. Note: only one installation method can currently
    ## be defined. We suggest using conda/mamba where possible.
    install:
      - pip install propkatraj
    ## List(str): a list of commands to use when installing the mdakit from its
    ## source code.
    src_install:
      - pip install git+https://github.com/Becksteinlab/propkatraj@main
    ## str: the package name used to import the mdakit
    import_name: propkatraj
    ## str: a specification for the range of Python versions supported by this MDAKit
    python_requires: ">=3.8"
    ## str: a specification for the range of MDAnalysis versions supported by this MDAKit
    mdanalysis_requires: ">=2.0.0"
    ## List(str): a list of commands to use when attempting to run the MDAKit's tests
    run_tests:
      - pytest --pyargs propkatraj.tests
    ## List(str): a list of commands to use to install the necessary dependencies required
    ## to run the MDAKit's tests
    test_dependencies:
      - mamba install pytest MDAnalysisTests
    ## str: the organisation name the MDAKit falls under
    project_org: Becksteinlab
    ## str: the development status of the MDAKit
    development_status: Mature
    ## List(str) a list of publications to cite when using the MDAKit
    publications:
      - https://zenodo.org/record/7647010
      - https://doi.org/10.1021/ct200133y
      - https://doi.org/10.1085/jgp.201411219
    ## str: a link to the MDAKit's community (mailing list, github discussions, etc...)
    community_home: https://alinktoamailinglist.org
    ## str: a link to the MDAKit's changelog
    changelog: https://alinktoachangelog.org


.. _`issue tracker`:
   https://github.com/MDAnalysis/MDAKits/issues

