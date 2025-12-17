.. _specification:
   
The ``metadata.yaml`` file
==========================

The ``metadata.yaml`` file is a `YAML format`_ file containing important
information about an MDAKit. A template can be found :ref:`below <template>` 
and in the MDAKit repository (`mdakits/template/metadata.yaml`_). For an 
example of a completed ``metadata.yaml``, see the 
:ref:`guided example <example-registration>`.

The file includes both required and optional entries:

- **Required entries**: Any variable in the 'required entries' section **must**
  be provided. If missing or empty, the MDAKit *cannot be registered*.

- **Optional entries**: Any variable in the 'optional entries' section **may** 
  be left empty or be left out. However, it is recommended to provide as much
  information as possible. Some aspects of the registry checks may not work if
  these details are missing.

Please see the comments in the template for an explanation of all possible
items. Some additional notes on specifying how to run tests are also provided 
:ref:`below <specifying-tests>`.

.. Note::    

   For now, the :ref:`template file <template>` serves as the primary  
   specification for the MDAKits registry ``metadata.yaml`` file.  The MDAKits 
   registry specification will likely be updated in the future with new optional
   and required entries. The MDAKits team will assist developers with migrations
   should they become necessary.


.. _template:

Template ``metadata.yaml`` file
-------------------------------

Start from this template (also available at `mdakits/template/metadata.yaml`_) 
when creating a ``metadata.yaml`` for your MDAKit. See the comments for an 
explanation of each item, and replace the values as appropriate for your MDAKit,
noting the sections for *required entries* and *optional entries*.

The template uses the strings ``GH_HOST_ACCOUNT``, ``MYPROJECT``, and 
``MYPACKAGE`` to indicate that you should be filling in **your** details!
   
- ``GH_ACCOUNT``: The GitHub account where the source code repository is held; 
  typically your username or the organization that you're part of.

- ``MYPROJECT``: The name of your project. This is the name of your repository.
  In the template we also use it as the PyPi/conda package name.
   
- ``MYPACKAGE``: The name of the Python package. It describes how you import it 
  in Python code, i.e. it is used in ``import MYPACKAGE``.

**Note on YAML format**: Please look at the `YAML format`_ specifications to 
learn more about how to write correct YAML files. Note that YAML is a file 
format where indentation matters so make sure that your editor uses spaces and 
not TAB for indentation, as this can lead to incorrect YAML. Lines starting 
with hash marks ``#`` are comments. You can add your own comments and modify the
existing ones as needed.

.. literalinclude:: ../../../mdakits/template/metadata.yaml
   :language: yaml
   :lines: 1-2,13-


.. _specifying-tests:

Specifying tests
----------------

The commands for running your MDAKit's tests must be added under the 
``run_tests`` entry. Assuming that your tests are in a ``test/`` directory at
the top level of your repository, you could define your test commands as:

.. code-block:: yaml

	run_tests:
	  - git clone latest
	  - pytest -v tests/

This makes a clone of your repository based on your latest 
`release tag on GitHub <https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository>`_ 
and navigates into the repository root. Note that this is not a true 
:program:`git` command, but is instead specific to the MDAKits registry workflow
and depends on the ``project_home`` field in the ``metadata.yaml`` file.

The :program:`pytest` command then runs the tests found inside the ``tests/`` 
directory. If your tests are elsewhere, change this path appropriately.

Dependencies that are only required for testing are indicated in the 
``test_dependencies`` object. Suppose your package uses :program:`pytest`, and
used the `MDAnalysisTests <https://github.com/MDAnalysis/mdanalysis/wiki/UnitTests>`_ 
for sample data. This is reflected in your MDAKit metadata with:

.. code-block:: yaml

	test_dependencies:
	  - mamba install pytest MDAnalysis


.. _`mdakits/template/metadata.yaml`:
   https://github.com/MDAnalysis/MDAKits/blob/main/mdakits/template/metadata.yaml

.. _YAML format: https://yaml.org/   

