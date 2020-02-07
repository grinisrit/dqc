import torch
import numpy as np
import matplotlib.pyplot as plt
from ddft.hamiltons.hamiltonpw import HamiltonPlaneWave

def setup_hamilton(nx, ndim, boxsize, nfreq=1.0, sin=True):
    dtype = torch.float64
    x = torch.linspace(-boxsize/2.0, boxsize/2.0, nx+1)[:-1].to(dtype)
    rgrids = torch.meshgrid(*[x for i in range(ndim)]) # (nx,nx)
    rgrid = torch.cat([rgridx.unsqueeze(-1) for rgridx in rgrids], dim=-1).view(-1,ndim) # (nr,ndim)

    # construct the space
    space = QSpace(rgrid, [nx for i in range(ndim)])

    # construct the wavefunction as wf = sumj(sin(2*pi*xj))
    if sin:
        wf = torch.sin(rgrid * 2 * np.pi * nfreq).unsqueeze(0) # (1,nr,ndim)
    else:
        wf = torch.cos(rgrid * 2 * np.pi * nfreq).unsqueeze(0) # (1,nr,ndim)
    wf = torch.sum(wf, dim=-1, keepdim=True) # (1,nr,1)

    # assert torch.allclose(space.invtransformsig(wfq, dim=1), wf, atol=1e-5)
    # assert torch.allclose(space.transformsig(space.invtransformsig(wfq, dim=1), dim=1), wfq, atol=1e-5)

    h = HamiltonPlaneWave(rgrid, [nx for i in range(ndim)])
    return wf, h, space


def compare_hamilton_pw_kinetics(nx, ndim, boxsize=4.0, nfreq=1.0, sin=True):
    wf, h, space = setup_hamilton(nx, ndim, boxsize, nfreq=nfreq, sin=sin)
    vext = torch.zeros_like(wf).squeeze(-1)

    kin = h(wf, vext) # (1,nr,1)

    a = wf-2*kin/(2*np.pi*nfreq)**2
    assert torch.allclose(a, torch.zeros_like(a), atol=1e-4)

def compare_hamilton_pw_vext(nx, ndim, boxsize=4.0, nfreq=1.0, sin=True):
    wf, h, space = setup_hamilton(nx, ndim, boxsize, nfreq=nfreq, sin=sin)
    rgrid = space.rgrid # (nr, ndim)
    rgrid_norm = rgrid.norm(dim=-1) # (nr,)
    vext = (rgrid_norm * rgrid_norm * 0.5).unsqueeze(0) # (1,nr)

    hr = h(wf, vext) # (1,nr,1)

    kin = wf*(2*np.pi*nfreq)**2/2.0 # 1/2 * omega^2 * wf
    vext_wf = hr-kin
    vext_wf2 = vext.unsqueeze(-1)*wf
    torch.allclose(vext_wf, vext_wf2, atol=1e-4)

def test_hamilton_pw_kinetics():
    compare_hamilton_pw_kinetics(101, 1)
    compare_hamilton_pw_kinetics(101, 1, nfreq=1.0, sin=False)
    compare_hamilton_pw_kinetics(101, 1, nfreq=10.0, sin=True)
    compare_hamilton_pw_kinetics(101, 1, nfreq=10.0, sin=False)
    compare_hamilton_pw_kinetics(101, 1, nfreq=12.0, sin=False)
    compare_hamilton_pw_kinetics(101, 1, nfreq=12.0, sin=True)

def test_hamilton_pw_kinetics2d():
    compare_hamilton_pw_kinetics(51, 2)

def test_hamilton_pw_kinetics3d():
    compare_hamilton_pw_kinetics(31, 3)

def test_hamilton_pw_vext():
    compare_hamilton_pw_vext(101, 1)
    compare_hamilton_pw_kinetics(101, 1, nfreq=1.0, sin=False)
    compare_hamilton_pw_kinetics(101, 1, nfreq=10.0, sin=True)
    compare_hamilton_pw_kinetics(101, 1, nfreq=10.0, sin=False)
    compare_hamilton_pw_kinetics(101, 1, nfreq=12.0, sin=False)
    compare_hamilton_pw_kinetics(101, 1, nfreq=12.0, sin=True)

def test_hamilton_pw_vext2d():
    compare_hamilton_pw_vext(51, 2)

def test_hamilton_pw_vext3d():
    compare_hamilton_pw_vext(31, 3)
