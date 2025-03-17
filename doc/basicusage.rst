Basic usage
==============

The `edipy2` python module detects by default the presence of the Fortran libraries via `pkg-config`. The `EDIpack2.0` library provides an environment module and a `.pc` file which is readable by `pkg-config`. It is by default located in the :code:`~/.pkgconfig.d` directory. The environment variable :code:`PKG_CONFIG_PATH` to include the location of the `.pc` file. If no `.pc` file can be detected, the python module will try, as a backup , to load the library from a custom path that can be provided by setting the environment variable :code:`EDIPACK_PATH` to the folder containing the fortran libraries. If none of the previous attempts succeeds, the module will not not load correctly. 

The `edipy2` module consists mainly of a class called :code:`global_env`. The global variables and the functions of the EDIpack2 library that are exposed to the user are methods of this class. The class needs to be imported at the beginning of the script, along with other useful modules. Numpy is necessary, while mpi4py is strongly recommended.

.. code-block:: python

    import numpy as np
    import scipy as sp
    from edipy2 import global_env as ed
    import mpi4py
    from mpi4py import MPI
    import os,sys

The `EDIpack2.0 <https://www.github.com/EDIpack/EDIpack2.0/>`_ library offers, as an independent module, an interface for real-space DMFT functions (see relevant `documentation <https://edipack.github.io/EDIpack2.0/>`_). `EDIpy2.0` is in principle capable of solving real-space DMFT problems, provided the :code:`edipack2ineq2py.so` library is correctly installed in the system. If this library cannot be found, the python module will disable the real-space DMFT functions, and invoking them will result in a :code:`RuntimeError`. The user can check the availability of the real-space DMFT interface by printing the value of :code:`edipy2.global_env.has_ineq`.

An example driver is provided in the :code:`tests` folder of the `EDIpy2.0` repository. The basic steps to follow to run a single loop of DMFT-ED with edipy2 are the following:

Read the input file

.. code-block:: python

    ed.read_input("inputED.conf")
    
This will read an input file or generate a template one if no such file is found. The template will have the :code:`used.` prefix, which will need to be removed. An `example <https://raw.githubusercontent.com/edipack/EDIpack2.0/refs/heads/master/test/python/inputED.conf>`_ of input file with a brief description of the relevant global variables is provided in the EDIpack2 repo.
    
Set the local Hamiltonian

.. code-block:: python

    ed.set_hloc(hloc=Hloc)
    
If  :f:var:`bath_type`  is :code:`REPLICA` or :code:`GENERAL`, the replica matrix has to be initialized via

.. code-block:: python

    ed.set_hreplica(hvec, lambdavec)
    ed.set_general(hvec, lambdavec)
    
where :code:`hvec` and :code:`lambdavec` are arrays of the proper size (see function documentation).

The solver needs to be initialized via 

.. code-block:: python

    bath = ed.init_solver()
    
Optionally, such as when real-space DMFT is used, the bath can be already allocated as an array, the dimension of which has to be given by the output of :code:`Nb` = :func:`ed.get_bath_dimension` for single-impurity DMFT and :code:`[Nlat,Nb]` for real-space DMFT, where :code:`Nlat` is the number of inequivalent impurities

The impurity problem is then solved via 

.. code-block:: python

    ed.solve(bath)
    
The self-energy needs to be retrieved in order to calculate the local lattice Green's function, via

.. code-block:: python

    Sigma = ed.get_sigma(axis="m")
    
The local Green's function calculation is left to the user, as well as that of the Weiss field or the Delta function, to be fitted by the new bath.
This latter step happens via 

.. code-block:: python

    bath = ed.chi2_fitgf(Delta,bath,ispin=0,iorb=0)
    
(check the function documentation for more details), but alternatively a fitting routine of the user's choice can be employed.
Convergence can be checked via

.. code-block:: python

    err,converged=ed.check_convergence(Delta[0,0,0,0,:],ed.dmft_error,1,ed.Nloop)
    
and, finally, the solution environment can be cleaned up via

.. code-block:: python

    ed.finalize_solver()
    
some or all of the steps above can be inserted in the DMFT convergence loop.
