"""
Sum of diagonal and low rank matrices
"""
from typing import List, Iterable
import numpy as np
from numpy import ndarray
from spmat import utils


class ILMat:
    """
    Identity plus outer product of low rank matrix, I + L @ L.T

    Attributes
    ----------
    lmat : ndarray
        Low rank matrix.
    tmat : ILMat
        Alternative ILMat, construct by transpose of ``lmat``. It is not
        ``None`` when ``lmat`` is a 'fat' matrix.
    dsize : int
        Size of the diagonal.
    lrank : int
        Rank of the low rank matrix.

    Methods
    -------
    dot(x)
        Dot product with vector or matrix.
    invdot(x)
        Inverse dot product with vector or matrix.
    logdet()
        Log determinant of the matrix.
    """

    def __init__(self, lmat: Iterable):
        """
        Parameters
        ----------
        lmat : Iterable

        Raises
        ------
        ValueError
            When ``lmat`` is not a matrix.
        """
        self.lmat = utils.to_numpy(lmat, ndim=(2,))
        self.dsize = self.lmat.shape[0]
        self.lrank = min(self.lmat.shape)

        self._u, s, _ = np.linalg.svd(self.lmat, full_matrices=False)
        self._v = s**2
        self._w = -self._v/(1 + self._v)

    @property
    def mat(self) -> ndarray:
        return np.identity(self.dsize) + (self._u*self._v) @ self._u.T

    @property
    def invmat(self) -> ndarray:
        return np.identity(self.dsize) + (self._u*self._w) @ self._u.T

    def dot(self, x: Iterable) -> ndarray:
        """
        Dot product with vector or matrix

        Parameters
        ----------
        x : Iterable
            Vector or matrix

        Returns
        -------
        ndarray
        """
        x = utils.to_numpy(x, ndim=(1, 2))
        return x + (self._u*self._v) @ (self._u.T @ x)

    def invdot(self, x: Iterable) -> ndarray:
        """
        Inverse dot product with vector or matrix

        Parameters
        ----------
        x : Iterable
            Vector or matrix

        Returns
        -------
        ndarray
        """
        x = utils.to_numpy(x, ndim=(1, 2))
        return x + (self._u*self._w) @ (self._u.T @ x)

    def logdet(self) -> float:
        """
        Log determinant

        Returns
        -------
        float
            Log determinant of the matrix.
        """
        return np.log(1 + self._v).sum()

    def __repr__(self) -> str:
        return f"ILMat(dsize={self.dsize}, lrank={self.lrank})"


class DLMat:
    """
    Diagonal plus outer product of low rank matrix, D + L @ L.T

    Attributes
    ----------
    diag : ndarray
        Diagonal vector.
    lmat : ndarray
        Low rank matrix.
    dsize : int
        Size of the diagonal.
    lrank : int
        Rank of the low rank matrix.
    sdiag : ndarray
        Square root of diagonal vector.
    ilmat : ILMat
        Inner ILMat after strip off the diagonal vector.

    Methods
    -------
    dot(x)
        Dot product with vector or matrix.
    invdot(x)
        Inverse dot product with vector or matrix.
    logdet()
        Log determinant of the matrix.
    """

    def __init__(self, diag: Iterable, lmat: Iterable):
        """
        Parameters
        ----------
        diag : Iterable
            Diagonal vector.
        lmat : Iterable
            Low rank matrix.

        Raises
        ------
        ValueError
            If length of ``diag`` not match with number of rows of ``lmat``.
        ValueError
            If there are non-positive numbers in ``diag``.
        """
        diag = utils.to_numpy(diag, ndim=(1,))
        lmat = utils.to_numpy(lmat, ndim=(2,))
        if diag.size != lmat.shape[0]:
            raise ValueError("`diag` and `lmat` size not match.")
        if any(diag <= 0.0):
            raise ValueError("`diag` must be all positive.")

        self.diag = diag
        self.lmat = lmat

        self.dsize = self.diag.size
        self.lrank = min(self.lmat.shape)

        self.sdiag = np.sqrt(self.diag)
        self.ilmat = ILMat(self.lmat/self.sdiag[:, np.newaxis])

    @property
    def mat(self) -> ndarray:
        return np.diag(self.diag) + self.lmat.dot(self.lmat.T)

    @property
    def invmat(self) -> ndarray:
        return self.ilmat.invmat/(self.sdiag[:, np.newaxis] * self.sdiag)

    def dot(self, x: Iterable) -> ndarray:
        """
        Inverse dot product with vector or matrix

        Parameters
        ----------
        x : Iterable
            Vector or matrix

        Returns
        -------
        ndarray
        """
        x = utils.to_numpy(x, ndim=(1, 2))
        x = (x.T*self.sdiag).T
        x = self.ilmat.dot(x)
        x = (x.T*self.sdiag).T
        return x

    def invdot(self, x: Iterable) -> ndarray:
        """
        Inverse dot product with vector or matrix

        Parameters
        ----------
        x : Iterable
            Vector or matrix

        Returns
        -------
        ndarray
        """
        x = utils.to_numpy(x, ndim=(1, 2))
        x = (x.T/self.sdiag).T
        x = self.ilmat.invdot(x)
        x = (x.T/self.sdiag).T
        return x

    def logdet(self) -> float:
        """
        Log determinant

        Returns
        -------
        float
            Log determinant of the matrix.
        """
        return np.log(self.diag).sum() + self.ilmat.logdet()

    def __repr__(self) -> str:
        return f"DLMat(dsize={self.dsize}, lrank={self.lrank})"


class BDLMat:
    """
    Block diagonal low rank matrix, [... D + L @ L.T ...]

    Attributes
    ----------
    dlmats : List[DLMat]
        List of DLMat.
    num_blocks : int
        Number of blocks.
    dsizes : ndarray
        An array contains ``dsize`` for each block.
    dsize : int
        Overall diagonal size of the matrix.

    Methods
    -------
    dot(x)
        Dot product with vector or matrix.
    invdot(x)
        Inverse dot product with vector or matrix.
    logdet()
        Log determinant of the matrix.
    """

    def __init__(self, dlmats: List[DLMat]):
        self.dlmats = dlmats
        self.num_blocks = len(self.dlmats)
        self.dsizes = np.array([dlmat.dsize for dlmat in self.dlmats])
        self.dsize = self.dsizes.sum()

    @property
    def mat(self) -> ndarray:
        return utils.create_bdiag_mat([dlmat.mat for dlmat in self.dlmats])

    @property
    def invmat(self) -> ndarray:
        return utils.create_bdiag_mat([dlmat.invmat for dlmat in self.dlmats])

    def dot(self, x: Iterable) -> ndarray:
        """
        Inverse dot product with vector or matrix

        Parameters
        ----------
        x : Iterable
            Vector or matrix

        Returns
        -------
        ndarray
        """
        x = utils.to_numpy(x, ndim=(1, 2))
        x = utils.split(x, self.dsizes)
        return np.concatenate([dlmat.dot(x[i])
                               for i, dlmat in enumerate(self.dlmats)], axis=0)

    def invdot(self, x: Iterable) -> ndarray:
        """
        Inverse dot product with vector or matrix

        Parameters
        ----------
        x : Iterable
            Vector or matrix

        Returns
        -------
        ndarray
        """
        x = utils.to_numpy(x, ndim=(1, 2))
        x = utils.split(x, self.dsizes)
        return np.concatenate([dlmat.invdot(x[i])
                               for i, dlmat in enumerate(self.dlmats)], axis=0)

    def logdet(self) -> float:
        """
        Log determinant

        Returns
        -------
        float
            Log determinant of the matrix.
        """
        return sum([dlmat.logdet() for dlmat in self.dlmats])

    def __repr__(self) -> str:
        return f"BDLMat(dsize={self.dsize}, num_blocks={self.num_blocks})"

    @classmethod
    def create_bdlmat(cls,
                      diag: ndarray,
                      lmat: ndarray,
                      dsizes: Iterable[int]) -> "BDLMat":
        diags = utils.split(diag, dsizes)
        lmats = utils.split(lmat, dsizes)
        return cls([DLMat(*args) for args in zip(diags, lmats)])
