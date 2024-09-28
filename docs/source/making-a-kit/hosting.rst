***********************************************
Hosting code in a version controlled repository
***********************************************

Since the MDAKits registry makes heavy use of the GitHub actions 
infrastructure, registration of a kit requires that all code maintainers
also have a GitHub account for communication purposes.
For this reason, if your code is not already hosted in an accessible 
version controlled repository, hosting on `GitHub <https://github.com>`_ 
is recommended, although other services such as 
`Bitbucket <https://bitbucket.org/>`_, `GitLab <https://gitlab.com>`_, 
or self hosting is possible.

The registry does not require that your code be available through 
packaging repositories such as the Python Package Index or conda-forge, 
although having your code available through these services is highly 
encouraged.

After registration, users can find the installation instructions for the 
source code on your MDAKit page, which is specified in the 
``src_install`` field in the ``metadata.yaml`` file (see :ref:`specification`).

