*********************************
Step-by-step registration process
*********************************

This page lists the step-by-step process for registering an MDAKit.

For an example, see the registration page for the guided ``rmsfkit`` example.

#. Create a fork of the MDAKit repository 
   https://github.com/MDAnalysis/mdakits.
#. Make a new branch (choose any name, but "add-my-awesome-mdakit" is 
   a good one).
#. Add a new folder under ``mdakits`` with the name of your MDAKit. 
   Please note that this *must* match the name provided under the 
   `project_name` entry of the ``metadata.yaml`` file.
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

