=====================================
  The MDAnalysis Toolkits Registry
=====================================

|numfocus| |powered_by_MDA|


Contents
========

This repository contains the source code for the `MDAKits registry`_.

The registry hosts a list of MDAKits which it then both documents and
continually validate. For more details about the MDAKit registry, please see
the `MDAKit paper`_ in the section *The MDAKit registry*.

For detailed documentation and tutorials about MDAKits see the MDAKits site
https://mdakits.mdanalysis.org/


Creating a new MDAKit
=====================

The minimum specification for an MDAKit is defined in the `MDAKit
paper`_ under *The MDAKit framework*. To developers in creating best
practices adhering projects, a `cookiecutter`_ has been made
available.


Adding a new MDAKit
===================

Adding a new MDAKit involves making a PR against
this repository and adding a new `metadata`_ file within it's own
respective directory under `mdakits`.

*The registry is currently in development, the way by which new MDAKits are
added may change over time. If you have any concerns or questions about the
process, please reach out by raising an issue!*


License
=======

All written documentation materials are provided under a CC-BY-4.0-SA license, whilst codes (CI, utilities, etc...)
are licensed under ther terms of the MIT license. Please see the `LICENSE`_ for more details.

Acknowledgements
================

The development of this repository is supported by a grant from the Chan Zuckerberg Initiative under an EOSS4 award.

References
==========

1. Irfan Alibay, Lily Wang, Fiona Naughton, Ian Kenney, Jonathan Barnoud,
   Richard J Gowers, and Oliver Beckstein. **MDAKits: A framework for
   FAIR-compliant molecular simulation analysis.** In Meghann Agarwal, Chris
   Calloway, and Dillon Niederhut, editors, *Proceedings of the 22nd Python in
   Science Conference (SCIPY 2023)*, pages 76-84, Austin, TX, 2023. doi:
   `10.25080/gerudo-f2bc6f59-00a`_.

.. _`MDAKits registry`: https://mdakits.mdanalysis.org/mdakits.html
   
.. _`metadata`: mdakits/template/metadata.yaml

.. _`MDAKit paper`: https://doi.org/10.25080/gerudo-f2bc6f59-00a

.. _`10.25080/gerudo-f2bc6f59-00a`: https://doi.org/10.25080/gerudo-f2bc6f59-00a

.. _`cookiecutter`: https://github.com/MDAnalysis/cookiecutter-mdakit

.. _`LICENSE`: LICENSE

.. |numfocus| image:: https://img.shields.io/badge/powered%20by-NumFOCUS-orange.svg?style=flat&colorA=E1523D&colorB=007D8A
   :alt: Powered by NumFOCUS
   :target: https://www.numfocus.org/


.. |powered_by_MDA| image:: https://img.shields.io/badge/Powered%20by-MDAnalysis-orange.svg?logoWidth=15&logo=data:image/x-icon;base64,AAABAAEAEBAAAAEAIAAoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJD+XwCY/fEAkf3uAJf97wGT/a+HfHaoiIWE7n9/f+6Hh4fvgICAjwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACT/yYAlP//AJ///wCg//8JjvOchXly1oaGhv+Ghob/j4+P/39/f3IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJH8aQCY/8wAkv2kfY+elJ6al/yVlZX7iIiI8H9/f7h/f38UAAAAAAAAAAAAAAAAAAAAAAAAAAB/f38egYF/noqAebF8gYaagnx3oFpUUtZpaWr/WFhY8zo6OmT///8BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgICAn46Ojv+Hh4b/jouJ/4iGhfcAAADnAAAA/wAAAP8AAADIAAAAAwCj/zIAnf2VAJD/PAAAAAAAAAAAAAAAAICAgNGHh4f/gICA/4SEhP+Xl5f/AwMD/wAAAP8AAAD/AAAA/wAAAB8Aov9/ALr//wCS/Z0AAAAAAAAAAAAAAACBgYGOjo6O/4mJif+Pj4//iYmJ/wAAAOAAAAD+AAAA/wAAAP8AAABhAP7+FgCi/38Axf4fAAAAAAAAAAAAAAAAiIiID4GBgYKCgoKogoB+fYSEgZhgYGDZXl5e/m9vb/9ISEjpEBAQxw8AAFQAAAAAAAAANQAAADcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjo6Mb5iYmP+cnJz/jY2N95CQkO4pKSn/AAAA7gAAAP0AAAD7AAAAhgAAAAEAAAAAAAAAAACL/gsAkv2uAJX/QQAAAAB9fX3egoKC/4CAgP+NjY3/c3Nz+wAAAP8AAAD/AAAA/wAAAPUAAAAcAAAAAAAAAAAAnP4NAJL9rgCR/0YAAAAAfX19w4ODg/98fHz/i4uL/4qKivwAAAD/AAAA/wAAAP8AAAD1AAAAGwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALGxsVyqqqr/mpqa/6mpqf9KSUn/AAAA5QAAAPkAAAD5AAAAhQAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADkUFBSuZ2dn/3V1df8uLi7bAAAATgBGfyQAAAA2AAAAMwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB0AAADoAAAA/wAAAP8AAAD/AAAAWgC3/2AAnv3eAJ/+dgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9AAAA/wAAAP8AAAD/AAAA/wAKDzEAnP3WAKn//wCS/OgAf/8MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIQAAANwAAADtAAAA7QAAAMAAABUMAJn9gwCe/e0Aj/2LAP//AQAAAAAAAAAA
   :alt: Powered by MDAnalysis
   :target: https://www.mdanalysis.org
