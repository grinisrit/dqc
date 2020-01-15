import torch
from ddft.utils.misc import set_default_option

"""
This file contains methods to obtain eigenpairs of a linear transformation
    which is a subclass of ddft.modules.base_linear.BaseLinearModule
"""

def davidson(A, neig, params, **options):
    """
    Iterative methods to obtain the `neig` lowest eigenvalues and eigenvectors.
    This function is written so that the backpropagation can be done.

    Arguments
    ---------
    * A: BaseLinearModule instance
        The linear module object on which the eigenpairs are constructed.
    * neig: int
        The number of eigenpairs to be retrieved.
    * params: list of differentiable torch.tensor
        List of differentiable torch.tensor to be put to A.forward(x,*params).
        Each of params must have shape of (nbatch,...)
    * **options:
        Iterative algorithm options.

    Returns
    -------
    * eigvals: torch.tensor (nbatch, neig)
    * eigvecs: torch.tensor (nbatch, na, neig)
        The `neig` smallest eigenpairs
    """
    config = set_default_option({
        "max_niter": 10*neig,
        "nguess": neig+1,
        "min_eps": 1e-6,
    }, options)

    # get some of the options
    nguess = config["nguess"]
    max_niter = config["max_niter"]
    min_eps = config["min_eps"]

    # get the shape of the transformation
    na, nc = A.shape
    nbatch = params[0].shape[0]
    p = list(A.parameters())[0]
    dtype = p.dtype
    device = p.device
    if na != nc:
        raise TypeError("The linear transformation of davidson method must be a square matrix")

    # set up the initial guess
    V = torch.eye(na, nguess).unsqueeze(0).repeat(nbatch, 1, 1).to(dtype).to(device) # (nbatch,na,nguess)
    dA = A.diag(*params) # (nbatch, na)

    prev_eigvals = None
    stop_reason = "max_niter"
    for m in range(nguess, max_niter, nguess):
        VT = V.transpose(-2, -1)
        AV = A(V, *params) # (nbatch, na, nguess)
        T = torch.bmm(VT, AV) # (nbatch, nguess, nguess)

        # eigvals are sorted from the lowest
        # eval: (nbatch, nguess), evec: (nbatch, nguess, nguess)
        eigvalT, eigvecT = torch.symeig(T, eigenvectors=True)
        eigvecA = torch.bmm(V, eigvecT) # (nbatch, na, nguess)

        # check the convergence
        if prev_eigvals is not None:
            dev = (eigvalT[:,:neig].data - prev_eigvals).abs().max()
            if dev < min_eps:
                stop_reason = "min_eps"
                break

        # calculate the parameters for the next iteration
        prev_eigvals = eigvalT[:,:neig].data

        nj = eigvalT.shape[1]
        ritz_list = []
        for i in range(nj):
            f = 1. / (dA - eigvalT[:,i:i+1]) # (nbatch, na)
            AVphi = A(eigvecA[:,:,i], *params) # (nbatch, na)
            lmbdaVphi = eigvalT[:,i:i+1] * eigvecA[:,:,i] # (nbatch, na)
            r = f * (AVphi - lmbdaVphi) # (nbatch, na)
            ritz_list.append(r.unsqueeze(-1))

        # add the ritz vectors to the guess vectors
        ritz = torch.cat(ritz_list, dim=-1)
        ritz = ritz / ritz.norm(dim=1, keepdim=True) # (nbatch, na, nguess)
        Va = torch.cat((V, ritz), dim=-1)
        if Va.shape[-1] > na:
            Va = Va[:,:,-na:]

        # orthogonalize the new columns of V
        Q, R = torch.qr(Va) # V: (nbatch, na, nguess), R: (nbatch, nguess, nguess)
        V = Q

    eigvals = eigvalT[:,:neig]
    eigvecs = eigvecA[:,:,:neig]
    return eigvals, eigvecs