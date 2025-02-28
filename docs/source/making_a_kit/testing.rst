.. _testing: 

*******
Testing
*******

The MDAKit Registry requires that **minimal regression tests are present**.
These tests are not just useful for when you make changes to your code, but
also when any package dependencies (e.g. MDAnalysis, NumPy, and Python) change.
Additionally, tests inform the users of your packages that the code performs at
least the way you say it should and give them confidence that it can be used.

Basic tests can be written with a variety of packages, such as 
`pytest <https://docs.pytest.org/en/7.4.x/>`_ (the default choice for MDAnalysis
organization projects) or
`unittest <https://docs.python.org/3/library/unittest.html#module-unittest>`_.

Further improvements to your testing procedure may include automatically running
the tests on pushing to your remote repositories, often referred to as 
**continuous integration (CI)**. CI can be set up using repository pipeline 
tools, such as `GitHub Actions <https://github.com/features/actions>`_.

When submitting an MDAKit to the registry, you'll include the instructions for 
running the tests in the required ``metadata.yaml`` file under ``run_tests`` - 
see the :ref:`metadata.yaml documentation <specifying-tests>` for more.
