*************************
Part 4: Pushing to GitHub
*************************

*For a video demonstration of this section,* 
`click here  <https://www.youtube.com/watch?v=viCPUHkgSxg&t=114s>`_.

We need to upload our code to GitHub in order to finalise the continuous
integration set up in the previous step, and to fullfil the requirement 
that the Kit be hosted on a version-controlled repository.

During the cookie generation process, the target GitHub repository, 
``rmsfkit``, was identified and inserted into the workflows 
configuration, as well as into the ``README.md`` file. 

#. We add this repository as a remote to the local git repository:

   .. code-block:: bash

	$ git remote add origin git@github.com:myusername/rmsfkit

   (substituting ``myusername`` for your GitHub username). Make sure 
   that this repository exists on GitHub and is *empty*. 
   
#. Then, we push the local code to GitHub:

   .. code-block:: bash

	$ git push origin main

The ``rmsfkit`` repository on GitHub will now be up-to-date the local 
repository we have been working on. We can navigate to *Actions* 
on GitHub to see the status of our tests. If all was done 
correctly in the previous sections, these will all pass!


Progress: MDAKit requirements
-----------------------------

#. **✓ Uses MDAnalysis**
#. **✓ Open source + OSI license**
#. **✓ Versioned + on a version-controlled repository** -- our code is
   now on GitHub!
#. **✓ Designated authors and maintainers**
#. *(At least) minimal documentation*
#. **✓ (At least) minimal regression tests** -- CI should be up and
   running, and the tests added in the last step all passing!
#. **✓ Installable as a standard package**
#. **✓ (Recommended) community information available**
#. *(Recommended) on a package distribution platform*

