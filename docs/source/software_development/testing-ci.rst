##################################
Testing and continuous integration
##################################

Testing
=======
What is it?
-----------
- Check that running a piece of code gives an expected result
- Important terms: regression tests/unit tests, 'code coverage'

More detail:
- Things to cover: both 'good' and 'bad' data
  
Why is it important?
--------------------

How is it done?
---------------
- pytest, unittest
  { some particular tips w/ pytest? assert }
- Where do tests 'live'? with the package (MDAKit cookie cutter) vs. separate (MDA)
- Running locally, running automatically -> GitHub actions + CI
- codecov (+ automating)


Continuous integration
======================
What is it?
-----------
- Check that software still works in general (installation, pass tests) as 
  time progresses
- Related: 'upstream dependencies'+ keeping an eye on upcoming changes

Why is it important?
--------------------
- Both changes you make + that happen upstream can affect code in unexpected ways!

How is it done?
---------------
- GitHub actions + scheduling on push, at X time, etc
