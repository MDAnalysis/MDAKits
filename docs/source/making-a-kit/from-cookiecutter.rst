************************************************
Building from the cookiecutter: a guided example
************************************************

In this section, we provide a guided example for creating an MDAKit
using the `MDAKit cookiecutter <https://cookiecutter-mdakit.readthedocs.io>`_.
A `video walk-through of this tutorial  <https://www.youtube.com/watch?v=viCPUHkgSxg>`_ 
is available on YouTube.

We will create a kit for RMSF analysis, replicating the functionality 
of the `RMSF analysis class <https://docs.mdanalysis.org/stable/documentation_pages/analysis/rms.html#MDAnalysis.analysis.rms.RMSF>`_ 
in the core library.


**MDAKit requirements**

As a reminder, here are (in brief) the requirements (and recommendations)
that we are aiming to fulfil to make a 'registerable' kit. See the 
requirements in more detail :ref:`here <requirements>` 
We'll check back in at the end of each part to see how we're going!

#. Uses MDAnalysis
#. Open source + OSI license
#. Versioned + on a version-controlled repository
#. Designated authors and maintainers
#. (At least) minimal documentation
#. (At least) minimal regression tests
#. Installable as a standard package
#. (Recommended) community information available
#. (Recommended) on a package distribution platform


.. toctree::
   :maxdepth: 1
   :caption: Steps

   guided-example/use-cookiecutter
   guided-example/add-code
   guided-example/add-tests
   guided-example/to-github
   guided-example/add-docs
   guided-example/make-release

