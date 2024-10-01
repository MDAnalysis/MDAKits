.. _registration:

*****************************
Part 7: Registering an MDAKit
*****************************

*For a video demonstration of this section,* 
`click here  <https://www.youtube.com/watch?v=viCPUHkgSxg&t=287s>`_.

The MDAKit registration is the same regardless of the creation process 
for the kit. Here, we continue our guided example by showing the 
registration process for our example ``rmsfkit``. When registering 
your own kit, be sure to read the general information on the registration 
process is found in the :ref:<add_mdakit> section. 

In order to submit your MDAKit to the registry, you will need to create 
a pull request on GitHub against the MDAnalysis/MDAKits repository.

First create a fork of the MDAnalysis/MDAKits repository on GitHub, then
clone the fork to your machine, navigate into ``MDAKits/mdakits/``, 
and make an empty directory with your MDAKit name:

.. code-block:: bash

	git clone git@github.com:yourusername/MDAKits
	cd MDAKits/mdakits
	mkdir rmsfkit/
	cd rmsfkit

Now add a ``metadata.yaml`` for your MDAKit in this directory. See
:ref:`specification` for more details on this file.  
The contents of ``metadata.yaml`` for ``rmsfkit`` are:

.. code-block:: yaml

	project_name: rmsfkit
	authors:
	  - https://github.com/yourusername/rmsfkit/blob/main/AUTHORS.md
	maintainers:
	  - yourusername
	description:
	    An analysis module for calculating the root-mean-square fluctuation of atoms in molecular dynamics simulations.
	keywords:
	  - rms
	  - rmsf
	license: GPL-2.0-or-later
	project_home: https://github.com/yourusername/rmsfkit
	documentation_home: https://rmsfkit.readthedocs.io/en/latest/
        documentation_type: API
        src_install:
          - git clone https://github.com/yourusername/rmsfkit.git
          - cd rmsfkit/
          - pip install .

	## Optional entries
	python_requires: ">=3.9"
	mdanalysis_requires: ">=2.0.0"
	run_tests:
	  - pytest --pyargs rmsfkit.tests
	development_status: Beta

Commit and push this to your fork:

.. code-block:: bash

        git add metadata.yaml
        git commit -m "Adding rmsfkit"
        git put origin main

Refresh the forked repository page in your browser. Under "Contribute", 
open a Pull Request. Add a title with the name of the kit and add a quick 
description. Click "Create pull request" and wait for the tests to pass.

Once this is done, you can add a comment along the lines of 
"@MDAnalysis/mdakits-reviewers, ready for review". The reviewers will get 
back you you with any change requests before merging it in as a kit.

At this point there are no additional steps for registering your kit!
However, your responsibility for your new MDAKit does not end here.
Once your kit is on the {weekly CI run, also keep an eye on other things, continue to improve/develop}. 
Read the information on the :ref:`maintaining` page.

.. image:: img/rmsftutorial/submitting.gif
        :alt: Process for submitting a kit to the registy


