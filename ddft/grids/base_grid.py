from abc import abstractmethod, abstractproperty
import torch

class BaseGrid(object):

    @abstractmethod
    def get_dvolume(self):
        """
        Obtain the torch.tensor containing the dV elements for the integration.

        Returns
        -------
        * dV: torch.tensor (nr,)
            The dV elements for the integration
        """
        pass

    @abstractmethod
    def solve_poisson(self, f):
        """
        Solve Poisson's equation del^2 v = f, where f is a torch.tensor with
        shape (nbatch, nr) and v is also similar.
        The solve-Poisson's operator must be written in a way that it is
        a symmetric transformation when multiplied by get_dvolume().

        Arguments
        ---------
        * f: torch.tensor (nbatch, nr)
            Input tensor

        Results
        -------
        * v: torch.tensor (nbatch, nr)
            The tensor that fulfills del^2 v = f. Please note that v can be
            non-unique due to ill-conditioned operator del^2.
        """
        pass

    @abstractproperty
    def rgrid(self):
        """
        Returns (nr, ndim) torch.tensor which represents the spatial position
        of the grid.
        """
        pass

    @abstractproperty
    def boxshape(self):
        """
        Returns the shape of the signal in the real spatial dimension.
        prod(boxshape) == rgrid.shape[0]
        """
        pass

    def integralbox(self, p, dim=-1):
        """
        Performing the integral over the spatial grid of the signal `p` where
        the signal in spatial grid is located at the dimension `dim`.

        Arguments
        ---------
        * p: torch.tensor (..., nr, ...)
            The tensor to be integrated over the spatial grid.
        * dim: int
            The dimension where it should be integrated.
        """
        integrand = p.transpose(dim,-1) * self.get_dvolume()
        res = torch.sum(integrand, dim=-1)
        return res.transpose(dim,-1)

    def mmintegralbox(self, p1, p2):
        """
        Perform the equivalent of matrix multiplication but replacing the sum
        with integral sum.

        Arguments
        ---------
        * p1: torch.tensor (..., n1, nr)
        * p2: torch.tensor (..., nr, n2)
            The integrands of the matrix multiplication integration.

        Returns
        -------
        * mm: torch.tensor (..., n1, n2)
            The result of matrix multiplication integration.
        """
        pleft = p1 * self.get_dvolume()
        return torch.matmul(pleft, p2)

    def interpolate(self, f, rq):
        """
        Interpolate the function f to any point rq.

        Arguments
        ---------
        * f: torch.tensor (nbatch, nr)
            The function to be interpolated.
        * rq: torch.tensor (nrq, ndim)
            The position where the interpolated value is queried.

        Returns
        -------
        * fq: torch.tensor (nbatch, nrq)
            The interpolated function at the given queried position.
        """
        raise RuntimeError("Unimplemented interpolate function for class %s" % \
                           (self.__class__.__name__))

class Base3DGrid(BaseGrid):
    @abstractproperty
    def rgrid_in_xyz(self):
        """
        Returns the rgrid in Cartesian coordinate.
        """
        pass

class BaseRadialGrid(BaseGrid):
    @abstractmethod
    def antiderivative(self, intgn, dim=-1, zeroat="left"):
        """
        Perform an integration along the specified dimension.
        """
        pass

class BaseRadialAngularGrid(Base3DGrid):
    @abstractproperty
    def radial_grid(self):
        """
        Returns the radial grid associated with the parent grid.
        """
        pass

class BaseMultiAtomsGrid(Base3DGrid):
    @abstractproperty
    def atom_grid(self):
        """
        Returns the grid for individual atom.
        """
        pass

    @abstractmethod
    def get_atom_weights(self):
        """
        Returns the weights associated with the integration grid per atom.
        Shape: (natoms, nr//natoms)
        """
        pass
