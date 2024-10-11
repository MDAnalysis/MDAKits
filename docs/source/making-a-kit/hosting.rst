.. _hosting:

***********************************************
Hosting code in a version controlled repository
***********************************************

The MDAKits registry makes heavy use of the GitHub actions infrastructure. Thus,
registration of a kit **requires** that all code maintainers also have a GitHub 
account for communication purposes.

For this reason, if your code is not already hosted in an accessible version 
controlled repository, hosting on `GitHub <https://github.com>`_ is 
*recommended*, although other services such as 
`Bitbucket <https://bitbucket.org/>`_, `GitLab <https://gitlab.com>`_, or self 
hosting are possible.

The registry **does not require** that your code be available through packaging
repositories such as the Python Package Index (`PyPi <https://pypi.org/>`_) or
`conda-forge <https://conda-forge.org/>`_, although having your code available
through these services is highly encouraged. 

However, your code **does** need to be installable from source. You'll specify 
the commands for this in the ``scr_install`` field of your ``metadata.yaml`` 
file (see the :ref:`metadata.yaml documentation <specification>`). This will 
then be made available to users on your MDAKit's page on the
:ref:`Registry <mdakits>`.
