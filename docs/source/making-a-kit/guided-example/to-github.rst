*************************
Part 4: Pushing to GitHub
*************************

*For a video demonstration of this section,* 
`click here  <https://www.youtube.com/watch?v=viCPUHkgSxg&t=114s>`_.

We need to upload our code to GitHub in order to finalise the continuous
integration set up in the previous step, and to fullfil the requirement 
that the Kit be hosted on a version-controlled repository.

During the cookie generation process, the target GitHub repository was 
identified and inserted into the workflows configuration, as well as 
into the ``README.md`` file. 

Add this repository as a remote to your local git repository:

.. code-block:: bash

	$ git remote add origin git@github.com:myusername/rmsfkit

(substituting ``myusername`` for your GitHub username). Make sure that this repository exists on GitHub and is *empty*. Then, push the local code to GitHub:

.. code-block:: bash

	$ git push origin main

Open the repository in GitHub and navigate to actions. Here you can 
see the status of the tests. If all was done correctly in the previous 
sections, these tests will pass!

**Progress: MDAKit requirements**

#. **✓ Uses MDAnalysis**
#. **✓ Open source + OSI license**
#. **✓ Versioned + on a version-controlled repository**
#. **✓ Designated authors and maintainers**
#. *(At least) minimal documentation*
#. **✓(At least) minimal regression tests**
#. **✓ Installable as a standard package**
#. **✓ (Recommended) community information available**
#. *(Recommended) on a package distribution platform*

