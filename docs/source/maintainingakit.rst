.. _maintaining:

*********************
Maintaining an MDAKit
*********************

.. note::   
   This section is still under construction. If you have topics you would
   like to see covered here, please get in touch via 
   `MDAnalysis Github Discussions`_.

Successfully registering an MDAKit is not the end of the journey! Like a pet, a
software package still requires input to keep it healthy and thriving. 
This includes both expanding and adding new features and ensuring the MDAKit 
continues to run as intended. **While not required for an MDAKit to remain in
the registry, such activities are highly encouraged**.

There are a variety of reasons a kit may behave unexpectedly after being 
submitted to the registry. Apart from actively developing the kit, changes in 
kit dependencies, or even Python itself, can introduce/deprecate new/old 
functionality. 

As part of the MDAKit Registry, your kits' tests (as specified in 
``metadata.yaml``) are automatically rerun each week, so that you (and potential 
users) have assurance that your code still works as intended, or are notified
when it does not. 

**However, the ultimate responsibility for maintaining your MDAKit remains with
you.**

The sections below provide some information to keep in mind for maintaining your
MDAKit after registration.

.. toctree::
   :maxdepth: 2

   maintaining-a-kit/keep-healthy
   maintaining-a-kit/improving


.. _`MDAnalysis GitHub Discussions`:
   https://github.com/MDAnalysis/mdanalysis/discussions


Want to go even further beyond your MDAKit? You can also help us out by 
:ref:`reviewing other MDAKits <reviewers-guide>`! 
