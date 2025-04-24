from ctypes import *
import numpy as np
import os, sys
import types


def inspect_uparams(self, which_param, value=None):
    """

    This is an internal function that gives/takes the value of the
    interaction parameters. In EDIpack > 3.0.4, these are stored in
    internal matrices, so Uloc, Ust etc. are not up-to-date with them
    after the input is read. To keep compatibility with older versions
    we default to the previous behavior if the function inspect_uparams
    is not found in the c_bindings library

    """

    norb_aux = c_int.in_dll(self.library, "Norb").value

    if which_param == "Uloc":
        parindex = 0
    elif which_param == "Ust":
        parindex = 1
    elif which_param == "Jh":
        parindex = 2
    elif which_param == "Jx":
        parindex = 3
    elif which_param == "Jp":
        parindex = 4

    if value is None:
        ioflag = 1
    else:
        ioflag = 0

    inspect_uparams_wrap = self.library.inspect_uparams
    inspect_uparams_wrap.argtypes = [
        c_int,
        np.ctypeslib.ndpointer(dtype=float, ndim=2, flags="F_CONTIGUOUS"),
        c_int,
        np.ctypeslib.ndpointer(dtype=int, ndim=1, flags="F_CONTIGUOUS"),
    ]
    inspect_uparams_wrap.restype = None

    # Take the old value of the parameters
    parvalue = np.zeros((norb_aux, norb_aux), dtype=float, order="F")
    ierrflag = np.zeros(1, dtype=int, order="F")
    inspect_uparams_wrap(parindex, parvalue, 1, ierrflag)
    if (
        ierrflag[0] == 1
    ):  # If the matrices are not initialized yet, 
        # raise an exception so the calling function 
        # defaults to accessing the input variables
        raise Exception

    if ioflag == 0:  # Take a value
        if parindex == 0:
            if np.isscalar(value):
                parvalue[0, 0] = value
            elif len(value) < norb_aux:
                parvalue[0 : len(value), 0 : len(value)] = np.diag(value)
            else:
                parvalue[:, :] = np.diag(value[0:norb_aux])
        else:
            if np.isscalar(value):
                parvalue = value * (
                    np.ones((norb_aux, norb_aux), dtype=float, order="F")
                    - np.eye(norb_aux, dtype=float, order="F")
                )
            elif np.shape(value) == (norb_aux, norb_aux):
                parvalue = np.array(value, dtype=float, order="F")
            else:
                print(np.shape(value))
                raise ValueError("Shape of parameter matrix != [Norb, Norb]")
        inspect_uparams_wrap(parindex, parvalue, ioflag, ierrflag)
    else:  # Return a value
        value = np.zeros((norb_aux, norb_aux), dtype=float, order="F")
        inspect_uparams_wrap(parindex, value, ioflag, ierrflag)
        if parindex == 0:
            return np.diagonal(value)
        else:
            return value
            
            
            
def reset_umatrix(self):
    """

    This function resets to 0 all the interaction coefficients
    
    """
    
    reset_umatrix_wrap = self.library.reset_umatrix
    reset_umatrix_wrap.argtypes = None
    reset_umatrix_wrap.restype = None
    
    reset_umatrix_wrap()
    
    
def add_twobody_operator(self,orbvector,spinvector,coefficient):
    """

    This function lets the user add an interaction term on-the-fly.
    The input parameters are of the form :code:`[o1,o2,o3,o4]` for the
    orbital indices and :code:`[s1,s2,s3,s4]="u/d"` for the spin indices.
    The order of the indices is consistent with those of the umatrix file
    (see relevant EDIpack2.0 documentation).
    
    :type orbvector: int
    :param orbvector: array of length 4, orbital indices
    
    :type orbvector: str
    :param orbvector: array of length 4, spin indices
    
    :type float: coefficient
    :param orbvector: interaction coefficient
    
    """
    
    add_twobody_operator_wrap = self.library.add_twobody_operator
    add_twobody_operator_wrap.argtypes = [
        c_int,
        c_int,
        c_int,
        c_int,
        c_int,
        c_int,
        c_int,
        c_int,
        c_double
    ]
    add_twobody_operator_wrap.restype = None
    
    mapping = {"u": 1, "d": 2}
    spinvector = [mapping[x] for x in spinvector]
    orbvector = [x+1 for x in orbvector]
    
    add_twobody_operator_wrap(orbvector[0],spinvector[0],orbvector[1],spinvector[1],orbvector[2],spinvector[2],orbvector[3],spinvector[3],coefficient)
