from __future__ import print_function
import scipy.sparse as sps
import numpy as np
# from dolfin import dx, grad, inner


def linearzd_quadterm(H, linv, retparts=False, hlstr=None,
                      lone_only=False, ltwo_only=False):
    """ compute the matrices `L1`, `L2` that represent the linearized convection

    `H(v, v) ~ L1*v + L2*v - H(linv, linv)`


    Parameters:
    ---
    H : (nv, nv*nv) sparse array
        the tensor (as a matrix) that evaluates the convection term
    linv : (nv, 1) numpy array
        the stat at which the linearization is about
    retparts: Boolean, optional
        whether to return the `L1` or `L2` separately, \
        defaults to `False`, i.e. `L1+L2` is returned
    hlstr : str, optional
        name of location from where to load or where to store the \
        the wanted data, if `None` nothing is loaded or stored, \
        defaults to `None`

    """
    try:
        import dolfin_navier_scipy.data_output_utils as dou
        if hlstr is None:
            raise IOError()
        if retparts or lone_only or ltwo_only:
            H1L = dou.load_spa(hlstr + '_H1L.mtx')
            if lone_only:
                return H1L
            H2L = dou.load_spa(hlstr + '_H2L.mtx')
            if ltwo_only:
                return H2L
            print('loaded `hlmat`')
            return H1L, H2L
        else:
            HL = dou.load_spa(hlstr + '.mtx')
            print('loaded `hlmat`')
            return HL

    except IOError:
        print('assembling hlmat ...')

    nv = linv.size
    try:
        speye = sps.eye(nv)
    except TypeError:  # for earlier scipys
        speye = sps.eye(nv, nv)

    if retparts or ltwo_only or lone_only:
        if lone_only:
            H1L = H * (sps.kron(speye, linv))
            return H1L
        if ltwo_only:
            H2L = H * (sps.kron(linv, speye))
            return H2L
        H1L = H * (sps.kron(speye, linv))
        H2L = H * (sps.kron(linv, speye))
        return H1L, H2L
    else:
        HL = H * (sps.kron(speye, linv) + sps.kron(linv, speye))
        return HL


def eva_quadterm(H, v):
    ''' function to evaluate `H*kron(v, v)` without forming `kron(v, v)`

    Parameters:
    ---
    H : (nv, nv*nv) sparse array
        the tensor (as a matrix) that evaluates the convection term

    '''

    NV = v.size
    hvv = np.zeros((NV, 1))
    for k, vi in enumerate(v):
        hviv = H[:, k*NV:(k+1)*NV]*(vi[0]*v)
        hvv = hvv + hviv
    return np.array(hvv)
