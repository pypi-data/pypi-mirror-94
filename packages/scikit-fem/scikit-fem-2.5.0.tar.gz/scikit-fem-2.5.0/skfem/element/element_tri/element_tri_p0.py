import numpy as np

from ..element_h1 import ElementH1
from ...mesh.mesh2d import MeshTri


class ElementTriP0(ElementH1):

    interior_dofs = 1
    dim = 2
    maxdeg = 0
    dofnames = ['u']
    doflocs = np.array([[.5, .5]])
    mesh_type = MeshTri

    def lbasis(self, X, i):
        if i == 0:
            return 1. + 0. * X[0], 0. * X
        else:
            self._index_error()
