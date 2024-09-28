***************************************************
Part 2: Adding code to the newly created repository
***************************************************

*For a video demonstration of this section,* 
`click here  <https://www.youtube.com/watch?v=viCPUHkgSxg&t=48s>`_.

Now that we have a shell for our MDAKit, we can begin to add our code
to the ``rmsfkit/`` directory.

In this example, we are recreating the exist MDAnalysis RMSD analysis,
so we will simply copy and paste the analysis class into 
``rmsfkit/rmsfkit.py``.The in-code documentation (which has been trimmed 
here for brevity) is written in 
`reStructuredText syntax <https://docutils.sourceforge.io/rst.html>`_
syntax for building with Sphinx later. 

The contents of the file should now resemble the following code block:

.. code-block:: python

	"""
	rmsfkit.py
	A package to perform RMSF analysis on molecular dynamics data.
	
	All code and documentation, both of which are trimmed for the sake of brevity,
	are taken from the MDAnalysis Python package. Used under GPLv2+.
	"""
	
	from MDAnalysis.analysis.base import AnalysisBase
	import numpy as np
	
	class RMSF(AnalysisBase):
	    r"""Calculate RMSF of given atoms across a trajectory.
	
	    Note
	    ----
	    No RMSD-superposition is performed; it is assumed that the user is
	    providing a trajectory where the protein of interest has been structurally
	    aligned to a reference structure. The protein also has to be whole because
	    periodic boundaries are not taken into account.
	
	    Run the analysis with :meth:`RMSF.run`, which stores the results in the
	    array :attr:`RMSF.results.rmsf`.
	
	    """
	    def __init__(self, atomgroup, **kwargs):
	        r"""Parameters
	        ----------
	        atomgroup : AtomGroup
	            Atoms for which RMSF is calculated
	        verbose : bool (optional)
	             Show detailed progress of the calculation if set to ``True``; the
	             default is ``False``.
	
	        Raises
	        ------
	        ValueError
	             raised if negative values are calculated, which indicates that a
	             numerical overflow or underflow occurred
	
	        Notes
	        -----
	        The root mean square fluctuation of an atom :math:`i` is computed as the
	        time average
	
	        .. math::
	
	          \rho_i = \sqrt{\left\langle (\mathbf{x}_i - \langle\mathbf{x}_i\rangle)^2 \right\rangle}
	
	        No mass weighting is performed. 
	        
	        This method implements an algorithm for computing sums of squares while
	        avoiding overflows and underflows :cite:p:`Welford1962`.
	
	        References
	        ----------
	        .. bibliography::
	            :filter: False
	
	            Welford1962
	
	        """
	        super(RMSF, self).__init__(atomgroup.universe.trajectory, **kwargs)
	        self.atomgroup = atomgroup
	
	    def _prepare(self):
	        self.sumsquares = np.zeros((self.atomgroup.n_atoms, 3))
	        self.mean = self.sumsquares.copy()
	
	    def _single_frame(self):
	        k = self._frame_index
	        self.sumsquares += (k / (k+1.0)) * (self.atomgroup.positions - self.mean) ** 2
	        self.mean = (k * self.mean + self.atomgroup.positions) / (k + 1)
	
	    def _conclude(self):
	        k = self._frame_index
	        self.results.rmsf = np.sqrt(self.sumsquares.sum(axis=1) / (k + 1))
	
	        if not (self.results.rmsf >= 0).all():
	            raise ValueError("Some RMSF values negative; overflow " +
	                             "or underflow occurred")


Finally, to make our ``RMSF`` analysis class easier to access, we 
import it in ``__init__.py`` by adding:

.. code-block:: python

	from .rmsfkit import RMSF


**Progress: MDAKit requirements**

#. **✓ Uses MDAnalysis**
#. **✓ Open source + OSI license**
#. *Versioned + on a version-controlled repository*
#. **✓ Designated authors and maintainers**
#. *(At least) minimal documentation*
#. *(At least) minimal regression tests*
#. **✓ Installable as a standard package**
#. **✓ (Recommended) community information available**
#. *(Recommended) on a package distribution platform*

