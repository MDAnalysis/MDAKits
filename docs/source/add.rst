.. _add-mdakit:

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

#. Create a fork of the MDAKit repository https://github.com/MDAnalysis/mdakits.
#. Make a new branch (choose any name, but "add-my-awesome-mdakit" is a good
   one).
#. Add a new folder under ``mdakits`` with the name of your MDAKit. Please note that this *must* match the name provided under the `project_name` entry of the ``metadata.yaml`` file.
#. Add a metadata YAML file with your MDAKit's details; copy the template from
   `mdakits/template/metadata.yaml`_ and modify it. See the comments in the
   file and the :ref:`notes below<template>` for more explanations.
#. Create a Pull Request (PR) from your branch against the *main*
   branch of the `MDAnalysis/mdakits repository`_. Add a title with
   the name of the kit (e.g. "register MyAwesomeTool") and add a short
   description of your MDAKit.

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
   registry will continuously test your code but the
   MDAnalysis team cannot fix it for you.

   .. Note:: 

      The registry will alert you via GitHub issues when your tests
      start failing with newer versions of your code, MDAnalysis, or other
      dependencies. In this case your MDAKit will be displayed as broken in the registry. **It is your responsibility to fix any relevant code in your package and (if necessary) make a new
      release of your code**.  

.. _specification:
   
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
   information as possible. Some aspects of the registry checks may not work if these details are missing.


.. Note::    

   For now, the :ref:`template file<template>` serves as the primary
   specification for the MDAKits registry ``metadata.yaml`` file.  The
   MDAKits registry specification will likely be updated in the future
   with new optional and required entries. The MDAKits team will assist developers with migrations should they become necessary.


      
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

.. literalinclude:: ../../mdakits/template/metadata.yaml
   :language: yaml
   :lines: 1-2,13-

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
