*********************
Maintaining an MDAKit
*********************

* More TBA* 

There are a variety of reasons a kit may behave unexpectedly after 
being submitted to the registry.
Apart from actively developing the kit, changes in kit dependencies, 
or even Python itself, can introduce (deprecate) new (old) functionality.
For this reason, the kits' continuous integration is rerun weekly to 
confirm the kits expected behavior.

In the event that a kit no longer passes its tests, an issue in MDAnalysis/MDAKits is automatically raised while notifying the maintainers indicated in the `metadata.yaml` file.
While the registry developers will be happy to help where possible, ultimately, the maintainers of the MDAKit are responsible for resolving such issues and ensuring that the tests pass.
The issue will automatically close after the next CI run if the tests pass again.
