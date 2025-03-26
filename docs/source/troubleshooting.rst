=================
 Troubleshooting
=================

Although we are trying to make :ref:`creating a MDAKit <makingakit>`
straightforward, things can still go wrong. This page collects recipes
and notes on how to fix problems with MDAKits.

If you have a problem and you can't find an answer here or in the
other documentation on this site, please get in touch via `MDAnalysis GitHub
Discussions`_.

.. _`MDAnalysis GitHub Discussions`:
   https://github.com/MDAnalysis/mdanalysis/discussions

Failures during MDAKit registration PR
======================================


generate_matrix step fails
--------------------------

When you submit your MDAKit registration PR, the continuous integration tests will run. 
Check if there are any failures. If the **generate_matrix** step fails with an 
error similar to the following (the commit hashes will differ):: 

  Base commit: a1be0b27fe3828dbbb389d0ce01e0e9f1a986134
  Head commit: ae10b54c38a2f68e3ac7769321b4b5c8f265655c
  Error: The head commit for this pull_request event is not ahead of the base commit. Please submit an issue on this action's GitHub repo.

then you need to update the main branch of the registry and merge it into your
registration branch.

For example, if your branch is named *register-mykit* then you could do the following.

1. `Sync fork`_ in your GitHub view of your forked MDAKits repository. This pulls in any
   changes that have accrued in the main branch since you submitted your PR.
2. Merge these changes into your branch by pulling these changes and merging::

     git switch main
     git pull
     git switch register-mykit    # change to your branch name
     git merge main
     git push

This should update the PR and make the checks run again.

.. _`Sync fork`:
   https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork
