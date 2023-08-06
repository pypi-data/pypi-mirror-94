from typing import Type, Dict

import numpy as np
from numpy import ndarray

from ..mesh import Mesh, MeshType


class MeshLine(Mesh):
    """One-dimensional mesh."""

    refdom: str = "line"
    brefdom: str = "point"
    meshio_type: str = "line"
    name: str = "One-dimensional"

    p = np.zeros((1, 0), dtype=np.float64)
    t = np.zeros((2, 0), dtype=np.int64)
    t2f = np.zeros((1, 0), dtype=np.int64)
    f2t = np.zeros((2, 0), dtype=np.int64)

    def __init__(self,
                 p: ndarray = None,
                 t: ndarray = None,
                 boundaries: Dict[str, ndarray] = None,
                 subdomains: Dict[str, ndarray] = None,
                 validate: bool = True):
        """Initialize one-dimensional mesh.

        If no parameters are given, initializes a mesh with the nodes 0 and 1.

        Parameters
        ----------
        p
            The nodes of the mesh.
        t
            Optional element connectivity. By default, this is constructed
            using the assumption that `p` is sorted.
        subdomains
            Named subsets of elements.
        boundaries
            Named subsets of boundary facets.
        validate
            If ``True``, perform mesh validity checks.

        """
        if p is None:
            p = np.array([[0., 1.]], dtype=np.float_)
        if p is not None and len(p.shape) == 1:
            p = np.array([p])
        self.p = p
        self.boundaries = boundaries
        self.subdomains = subdomains

        self.facets = self._facets()
        self.t = np.vstack([self.facets[0, :-1],
                            self.facets[0, 1:]]) if t is None else t
        super(MeshLine, self).__init__()
        self._build_mappings()

        if validate:
            self._validate()

    def _facets(self):
        return np.arange(self.p.shape[1])[None, :]

    @classmethod
    def init_refdom(cls: Type[MeshType]) -> MeshType:
        """Initialise a mesh consisting of the reference interval [0,1]."""
        return cls()

    def _build_mappings(self):
        """Build t2f and f2t"""

        self.t2f = self.t
        # build f2t
        e_tmp = self.t2f.flatten()
        t_tmp = np.tile(np.arange(self.t.shape[1]), 2)

        e_first, ix_first = np.unique(e_tmp, return_index=True)
        e_last, ix_last = np.unique(e_tmp[::-1], return_index=True)
        ix_last = e_tmp.shape[0] - ix_last - 1

        self.f2t = np.zeros((2, self.facets.shape[1]), dtype=np.int64)
        self.f2t[0, e_first] = t_tmp[ix_first]
        self.f2t[1, e_last] = t_tmp[ix_last]

        # second row to zero if repeated (i.e., on boundary)
        self.f2t[1, np.nonzero(self.f2t[0, :] == self.f2t[1, :])[0]] = -1

    def _adaptive_refine(self, marked):
        """Perform an adaptive refine which splits each marked element into
        two."""

        t = self.t
        p = self.p

        mid = range(len(marked)) + np.max(t) + 1

        nonmarked = np.setdiff1d(np.arange(t.shape[1]), marked)

        newp = np.hstack((p, p[:, t[:, marked]].mean(1)))
        newt = np.vstack((t[0, marked], mid))
        newt = np.hstack((t[:, nonmarked],
                          newt,
                          np.vstack((mid, t[1, marked]))))

        # update fields
        self.p = newp
        self.t = newt
        self.facets = self._facets()

        self._build_mappings()

    def nodes_satisfying(self, test):
        """Return nodes that satisfy some condition.

        Parameters
        ----------
        test : lambda function (1 param)
            Evaluates to 1 or ``True`` for nodes belonging
            to the output set.

        """
        return np.nonzero(test(self.p[0, :]))[0]

    def _uniform_refine(self):
        """Perform a single mesh refine that halves 'h'."""
        # rename variables
        p = self.p

        # new vertices and elements
        newp = np.hstack((p, p[:, self.t].mean(axis=1)))
        newt = np.empty((self.t.shape[0], 2 * self.t.shape[1]),
                        dtype=self.t.dtype)
        newt[0, ::2] = self.t[0]
        newt[0, 1::2] = p.shape[1] + np.arange(self.t.shape[1])
        newt[1, ::2] = newt[0, 1::2]
        newt[1, 1::2] = self.t[1]
        # update fields
        self.p = newp
        self.facets = np.hstack(
            [self.facets,
             self.facets.shape[1] + np.arange(self.t.shape[1])[None, :]])
        self.t = newt
        self._build_mappings()

    def boundary_nodes(self):
        """Find the boundary nodes of the mesh."""
        _, counts = np.unique(self.t.flatten(), return_counts=True)
        return np.nonzero(counts == 1)[0]

    def interior_nodes(self):
        """Find the interior nodes of the mesh."""
        _, counts = np.unique(self.t.flatten(), return_counts=True)
        return np.nonzero(counts == 2)[0]

    def __mul__(self, other):
        """Tensor product mesh."""
        from .mesh2d.mesh_quad import MeshQuad
        return MeshQuad.init_tensor(self.p[0], other.p[0])

    def param(self):
        return np.max(np.abs(self.p[0, self.t[1, :]]
                             - self.p[0, self.t[0, :]]))

    def _mapping(self):
        from skfem.mapping import MappingAffine
        return MappingAffine(self)

    def element_finder(self, mapping=None):
        ix = np.argsort(self.p)

        def finder(x):
            maxix = (x == np.max(self.p))
            x[maxix] = x[maxix] - 1e-10  # special case in np.digitize
            return np.argmax(np.digitize(x, self.p[0, ix[0]])[:, None]
                             == self.t[0], axis=1)

        return finder

    @staticmethod
    def strip_extra_coordinates(p: ndarray) -> ndarray:
        return p[:, :1]
