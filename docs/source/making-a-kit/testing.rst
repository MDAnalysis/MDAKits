*******
Testing
*******

We also require that minimal regression tests are present.
These tests are not just useful for when you make changes to your code,
but also when any package dependencies (e.g. MDAnalysis, NumPy, and 
Python) change. Additionally, tests inform the users of your packages 
that the code performs at least the way you say it should and give 
them confidence that it can be used.

Basic tests can be written with a variety of packages, such as the 
`pytest package <https://docs.pytest.org/en/7.4.x/>`_ (the default 
choice for MDAnalysis organization projects) or the 
`unittest package <https://docs.python.org/3/library/unittest.html#module-unittest>`_.
Further improvements to your testing procedure may include automatically 
running the tests on pushing to your remote repositories, often referred 
to as continuous integration (CI). CI can be set up using repository 
pipeline tools, such as `GitHub Actions <https://github.com/features/actions>`_.

When submitting an MDAKit to the registry, include the instructions for 
running the tests in the required ``metadata.yaml`` file (see a full example 
in the `registration <registration_>`_ section below).
Assuming that your tests are in a ``test/`` directory at the top level of 
your repository, you could define your test commands as:

.. code-block:: yaml

	run_tests:
	  - git clone latest
	  - pytest -v tests/

This makes a clone of your repository based on your latest 
`release tag on GitHub <https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository>`_ 
and navigates into the repository root. Note that this is not a true 
:program:`git` command, but is instead specific to the MDAKits registry 
workflow and depends on the ``project_home`` field in the ``metadata.yaml`` 
file (see :ref:`specification`).
The :program:`pytest` command then runs the tests found inside the ``tests/`` directory.
If your tests are elsewhere, change this path appropriately.

Dependencies that are only required for testing are indicated in the 
``test_dependencies`` object. Suppose your package uses :program:`pytest` 
and used the `MDAnalysisTests <https://github.com/MDAnalysis/mdanalysis/wiki/UnitTests>`_ 
for sample data. This is reflected in your MDAKit metadata with:

.. code-block:: yaml

	test_dependencies:
	  - mamba install pytest MDAnalysis

