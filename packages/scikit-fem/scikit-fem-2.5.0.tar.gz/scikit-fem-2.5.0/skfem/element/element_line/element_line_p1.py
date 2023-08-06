import numpy as np

from ...mesh.mesh_line import MeshLine
from ..element_h1 import ElementH1


class ElementLineP1(ElementH1):

    nodal_dofs = 1
    dim = 1
    maxdeg = 1
    dofnames = ['u']
    doflocs = np.array([[0.],
                        [1.]])
    mesh_type = MeshLine

    def lbasis(self, X, i):
        x = X[0]

        if i == 0:
            phi = 1 - x
            dphi = np.array([-1 + 0 * x])
        elif i == 1:
            phi = x
            dphi = np.array([1 + 0 * x])
        else:
            self._index_error()

        return phi, dphi
