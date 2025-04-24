from ctypes import *
import numpy as np
import os, sys
import types
          
            
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
