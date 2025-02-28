********************
Part 3: Adding tests
********************

*See our* `YouTube tutorial <https://www.youtube.com/watch?v=viCPUHkgSxg&t=72s>`_
*for a video demonstration of this section.*

The cookiecutter set up the framework for tests in ``<package_name>/tests``. 
Here we demonstrate the process for adding tests, running them locally, and
preparing them for automatic running (continuous integration).

Adding the tests
----------------

#. For our ``rmsfkit`` example, we once again take directly from the 
   existing code in the MDAnalysis package. We take the 
   `RMSF testing class <https://github.com/MDAnalysis/mdanalysis/blob/develop/testsuite/MDAnalysisTests/analysis/test_rms.py>`_ 
   and update the contents of ``rmsfkit/tests/test_rmsfkit.py`` as follows:

   .. code-block:: python

	"""
	Unit and regression test for the rmsfkit package.
	
	The TestRMSF class was taken from the MDAnalysis rms tests file and
	the relevant modules were switched.
	"""
	
	# Import package, test suite, and other packages as needed
	from MDAnalysisTests.datafiles import GRO, XTC, rmsfArray
	import MDAnalysis as mda
	
	from numpy.testing import assert_equal, assert_almost_equal
	import numpy as np
	import os
	import pytest
	
	import rmsfkit
	import sys
	
	def test_rmsfkit_imported():
	    """Sample test, will always pass so long as import statement worked"""
	    assert "rmsfkit" in sys.modules
	
	
	class TestRMSF(object):
	    @pytest.fixture()
	    def universe(self):
	        return mda.Universe(GRO, XTC)
	
	    def test_rmsf(self, universe):
	        rmsfs = rmsfkit.RMSF(universe.select_atoms('name CA'))
	        rmsfs.run()
	        test_rmsfs = np.load(rmsfArray)
	
	        assert_almost_equal(rmsfs.results.rmsf, test_rmsfs, 5,
	                            err_msg="error: rmsf profile should match test "
	                            "values")
	
	    def test_rmsf_single_frame(self, universe):
	        rmsfs = rmsfkit.RMSF(universe.select_atoms('name CA')).run(start=5, stop=6)
	
	        assert_almost_equal(rmsfs.results.rmsf, 0, 5,
	                            err_msg="error: rmsfs should all be zero")
	
	    def test_rmsf_identical_frames(self, universe, tmpdir):
	
	        outfile = os.path.join(str(tmpdir), 'rmsf.xtc')
	
	        # write a dummy trajectory of all the same frame
	        with mda.Writer(outfile, universe.atoms.n_atoms) as W:
	            for _ in range(universe.trajectory.n_frames):
	                W.write(universe)
	
	        universe = mda.Universe(GRO, outfile)
	        rmsfs = rmsfkit.RMSF(universe.select_atoms('name CA'))
	        rmsfs.run()
	        assert_almost_equal(rmsfs.results.rmsf, 0, 5,
	                            err_msg="error: rmsfs should all be 0")


#. *Adding a test dependency:* Since these tests use files from the 
   ``MDAnalysisTests`` package, we need to add this as a dependency. We do this
   in two configuration files:

   - In ``devtools/conda-envs/test_env.yaml``, in the ``dependencies:`` section:

     .. code-block:: yaml
     
        dependencies:
        # Base depends
        - python
        - pip

        # MDAnalysis
        - MDAnalysis

        # Testing
        - pytest
        - pytest-cov
        - pytest-xdist
        - codecov
        - MDAnalysisTests # <-- add this! 

   - In ``pyproject.toml``, under ``[project.optional-dependencies]``:

     .. code-block:: toml

	[project.optional-dependencies]
	test = [
	    "pytest>=6.0",
	    "pytest-xdist>=2.5",
	    "pytest-cov>=3.0",
	    "MDAnalysisTests>=2.0.0", # <-- add this!
	]


Running the tests
-----------------

#. Before running the tests, you need an environment with the necessary 
   packages installed. Following the instructions from the generated 
   ``README.md``, you can create a testing environment using ``mamba`` 
   (preferred) or ``conda``; e.g. for ``rmsfkit``:

   .. code-block:: bash

        $ mamba create -n rmsfkit
        $ mamba env update --name rmsfkit --file devtools/conda-envs/test_env.yaml
        $ mamba activate rmsfkit


#. Then install the MDAKit package in *editable mode*:

   .. code-block:: bash

        $ pip install -e .


#. Tests can now be run locally using:

   .. code-block:: bash

	$ pytest rmsfkit/tests

   This should pass without errors, though with some potential warnings. 

Steps 1-2 only need to be performed once. Thereafter, tests can be run at any 
point with ``pytest rmsfkit/tests`` (though you may need to reactivate the 
environment, ``mamba activate rmsfkit``).


Preparing for CI
----------------

Local tests passing is only half of testing. Ideally, tests should also pass 
through **continuous integration services**. The cookiecutter generates the 
necessary GitHub workflow files ``.github/workflows/gh-ci.yaml`` to do this on
GitHub.

#. Since our tests for ``rmsfkit`` use the ``MDAnalysisTests`` package, we again
   need to make a change to ``.github/workflows/gh-ci.yaml``. In the *Install 
   MDAnalysis version* job we change the ``install-tests`` flag to ``true``:

  .. code-block:: yaml

	- name: Install MDAnalysis version
	  uses: MDAnalysis/install-mdanalysis@main
	  with:
		version: ${{ matrix.mdanalysis-version }}
		install-tests: true  # <-- this needs to be true! 
		installer:  mamba 
		shell: bash  -l {0} 

In the next part, we will demonstrate uploading the MDAKit to a GitHub 
repository in order to run the pre-built continuous integration provided by the
cookiecutter. 


Progress: MDAKit requirements
-----------------------------

#. **✓ Uses MDAnalysis**
#. **✓ Open source + OSI license**
#. *Versioned + on a version-controlled repository*
#. **✓ Designated authors and maintainers**
#. *(At least) minimal documentation*
#. **✓(At least) minimal regression tests** - these are ready and (hopefully)
   passing! CI should be finalised in the next step by pushing to GitHub.
#. **✓ Installable as a standard package**
#. **✓ (Recommended) community information available**
#. *(Recommended) on a package distribution platform*

