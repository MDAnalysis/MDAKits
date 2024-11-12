#####################
Improving your MDAKit
#####################

Adding new features
===================
Developing your MDAKit can involve, for example, adding new features, or 
altering existing ones to improve performance or user-friendliness. This may 
come at your own initiative, or the request of a user.

How you develop your kit is up to you! Just remember it's a good idea to  
develop the tests and documentation alongside the new code (and to run the 
existing tests to ensure you aren't causing any unintended changes).


Go beyond the minimal MDAKit Registry requirements
==================================================
The requirements for registering an MDAKit are intentionally minimal to keep 
the entry barrier low. **Going beyond these minimal requirements is highly
recommended**.

This may include (but is not limited to):

- **More tests**: can you get to 100% coverage?!
- **More documentation**: Explain each part of your code. Add examples. Make
  your documentation visually appealing and easy to navigate!
- :ref:`Add a logo <logo>`: Spice up your MDAKit with your very own logo!
- **Use tooling and workflows**: don't rely solely on the MDAKit Registry's CI 
  run - set up your own automated testing and alerts!
- **Community resources**: make it easy for users to report issues, ask 
  questions - or even contribute to your MDAKit themselves!
- **Release on PyPi/conda-forge**: make it easier for users to install your kit! 
- :ref:`Make a journal publication <publishing>`: get recognition for your code!

If applicable, remember to :ref:`update your kit's metadata <update-metadata>` 
so new features are reflected on the Registry.


.. _update-metadata:

Updating the MDAKit's metadata
==============================
As your kit evolves, you may wish to update the information displayed on the
MDAKit's registry - for example, to expand the description, add a publication, 
or update the installation instructions.

If this is the case, simply edit your kit's ``metadata.yaml`` in your fork of 
the ``MDAKits`` repository, then make a new Pull Request (PR). The MDAKits team will then 
review and merge your PR to apply the changes.


.. _publishing:

Publishing your MDAKit!
=======================
Publishing an article in a journal such as `JOSS <https://joss.readthedocs.io/>`_
is a good way to get recogneition for your work and provide a citable source for
users.

`JOSS papers`_ are short, relatively simple, and in meeting the requirements
for registering an MDAKit, you will have already met many of the JOSS submission 
requirements. Once you've built up your kit's documentation and testing, 
consider publication with JOSS or a similar journal!


.. _logo:

Adding a logo for your MDAKit
=============================
A custom logo can add some pizazz to your MDAKit. You are welcome to create an
entirely custom logo, use the default `'empty gear' template`_, 
or modify the template - feel free to place your logo within the gears!

If you used the MDAKits cookiecutter, there is already a placeholder logo in 
your documentation. The `MDAKits cookiecutter documentation`_ has information 
on updating this.

.. note::
   MDAnalysis recommends that kit authors carefully check that any material used 
   in their kit - including logos - is used under appropriate licenses, and do
   not infringe on any copyrights. 
   
   MDAnalysis cannot give any legal advice on these matters; if you are unsure 
   about any legal matters, please consult a lawyer.


.. _`MDAKits cookiecutter documentation`:
   https://cookiecutter-mdakit.readthedocs.io/en/latest/usage.html#documentation-configuration

.. _`JOSS papers`:
   https://joss.readthedocs.io/en/latest/submitting.html#submission-process

.. _`'empty gear' template`:
   https://github.com/MDAnalysis/branding/tree/main/templates/MDAKits

