.. _guided-example:

*********************************************
Guided Example: Building an RMSF analysis Kit
*********************************************

In this section, we provide a guided example for creating an MDAKit
using the `MDAKit cookiecutter <https://cookiecutter-mdakit.readthedocs.io>`_.
A `video walk-through <https://www.youtube.com/watch?v=viCPUHkgSxg>`_ 
of this tutorial is available on YouTube.

We will create a kit for RMSF analysis, replicating the functionality 
of the `RMSF analysis class <https://docs.mdanalysis.org/stable/documentation_pages/analysis/rms.html#MDAnalysis.analysis.rms.RMSF>`_ 
in the core library.

First, let's refresh ourselves on the :ref:`requirements <requirements>` 
for a 'registerable' kit. In brief:

**MDAKit requirements**

#. Uses MDAnalysis
#. Open source + OSI license
#. Versioned + on a version-controlled repository
#. Designated authors and maintainers
#. (At least) minimal documentation
#. (At least) minimal regression tests
#. Installable as a standard package
#. (Recommended) community information available
#. (Recommended) available on a package distribution platform


Below are the steps we'll go through to create our MDAKit. We'll check
back in after each part to see how we're progressing through these
requirements!

.. toctree::
   :maxdepth: 1
   :caption: Steps for creating an MDAKit from the cookiecutter

   guided-example/use-cookiecutter
   guided-example/add-code
   guided-example/add-tests
   guided-example/to-github
   guided-example/add-docs
   guided-example/make-release
   guided-example/registering

