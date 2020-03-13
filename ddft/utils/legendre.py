import torch

def legint(coeffs, dim=-1, zeroat="left"):
    # Integrate the coefficients of Legendre polynomial one time
    # The resulting integral always have coeffs[0] == 0.
    # coeffs: (..., nr)

    c = coeffs.transpose(dim, -1)
    n = c.shape[-1]
    j21 = 1 + 2 * torch.arange(n).to(coeffs.dtype).to(coeffs.device)

    if zeroat == "left":
        m0 = 1.0
        mfinal = 1.0
    elif zeroat == "right":
        m0 = -1.0
        mfinal = -1.0
    else:
        m0 = 0.0

    dmid = c[..., :-2] / j21[:-2] - c[..., 2:] / j21[2:]
    dr = c[..., -2:] / j21[-2:]
    dl = -c[..., 1:2] / 3.0 + m0 * c[..., :1]

    res = mfinal * torch.cat((dl, dmid, dr), dim=-1).transpose(dim, -1)
    return res

def legval(x, order):
    if order == 0:
        return x*0 + 1
    elif order == 1:
        return x
    elif order == 2:
        return 1.5*x**2 - 0.5
    elif order == 3:
        return 2.5*x**3 - 1.5*x
    elif order == 4:
        return 4.375*x**4 - 3.75*x**2 + 0.375
    elif order == 5:
        return 7.875*x**5 - 8.75*x**3 + 1.875*x
    elif order == 6:
        return (231*x**6 - 315*x**4 + 105*x**2 - 5) / 16
    elif order == 7:
        return (429*x**7 - 693*x**5 + 315*x**3 - 35*x) / 16
    elif order == 8:
        return (6435*x**8 - 12012*x**6 + 6930*x**4 - 1260*x**2 + 35) / 128
    else:
        raise RuntimeError("The legendre polynomial order %d has not been implemented" % order)

def legvander(x, order, orderfirst=False):
    # x: (..., nx)
    # order: int

    assert order >= 0, "Order must be a non-negative integer"

    # (order+1, *xshape)
    yall = []
    yall.append(x.unsqueeze(0)*0+1)
    if order > 0:
        yall.append(x.unsqueeze(0))
        for i in range(2, order+1):
            yall.append(yall[i-1] * x * ((2.0*i-1.0)/i) - yall[i-2] * ((i-1.0)/i))

    y = torch.cat(yall, dim=0)
    if not orderfirst:
        # (*xshape, order+1)
        return y.transpose(0,-1)
    else:
        return y

def assoclegval(cost, l, m):
    sint = torch.sqrt(1-cost*cost)
    assert m <= l, "m must not be greater than l"
    assert l >= 0 and m >= 0, "l and m must be non-negative"
    if l == 0:
        return torch.ones_like(cost).to(cost.device)
    elif l == 1:
        if m == 0:
            return cost
        elif m == 1:
            return -sint
    elif l == 2:
        if m == 0:
            return 1.5 * cost*cost - 0.5
        elif m == 1:
            return -3*cost*sint
        elif m == 2:
            return 3*sint*sint
    elif l == 3:
        if m == 0:
            return 2.5*cost**3 - 1.5*cost
        elif m == 1:
            return (-7.5*cost**2 + 1.5) * sint
        elif m == 2:
            return 15 * cost * sint*sint
        elif m == 3:
            return -15 * sint**3
    elif l == 4:
        if m == 0:
            return (35*cost**4 - 30*cost**2 + 3) / 8.0
        elif m == 1:
            return -2.5*(7*cost**3 - 3*cost) * sint
        elif m == 2:
            return 7.5*(7*cost**2 - 1)*sint**2
        elif m == 3:
            return -105*cost*sint**3
        elif m == 4:
            return 105*sint**4
    elif l == 5:
        if m == 0:
            return (63*cost**4 - 70*cost**2 + 15) * cost/8
        elif m == 1:
            return (21*cost**4 - 14*cost**2 + 1) * sint * 15/8.0
        elif m == 2:
            return (1-cost**2) * (3*cost**2 - 1) * cost * 105./2.
        elif m == 3:
            return (9*cost**2 - 1) * sint**3 * 105./2
        elif m == 4:
            return 945 * cost * sint**4
        elif m == 5:
            return 945 * sint**4
    elif l == 6:
        if m == 0:
            return (231*cost**6 - 315*cost**4 + 105*cost**2 - 5) / 16
        elif m == 1:
            return (33*cost**4 - 30*cost**2 + 5) * sint * cost * 21/8.0
        elif m == 2:
            return (33*cost**4 - 18*cost**2 + 1) * sint**2 * 105/8.0
        elif m == 3:
            return (11*cost**2 - 3) * cost * sint**3 * 315/2.0
        elif m == 4:
            return (11*cost**2 - 1) * sint**4 * 945/2.0
        elif m == 5:
            return 10395 * cost * sint**5
        elif m == 6:
            return 10395 * sint**6
    elif l == 7:
        if m == 0:
            return (429*cost**6 - 693*cost**4 + 315*cost**2 - 35) * cost / 16
        elif m == 1:
            return (429*cost**6 - 495*cost**4 + 135*cost**2 - 5) * sint * 7/16.
        elif m == 2:
            return (143*cost**4 - 110*cost**2 + 15) * cost * sint**2 * 63/8.
        elif m == 3:
            return (143*cost**4 - 66*cost**2 + 3) * sint**3 * 315./8
        elif m == 4:
            return (13*cost**2 - 3) * cost * sint**4 * 3465/2.
        elif m == 5:
            return (13*cost**2 - 1) * sint**5 * 10395/2.
        elif m == 6:
            return 135135 * cost * sint**6
        elif m == 7:
            return 135135 * sint**7
    elif l == 8:
        if m == 0:
            return (6435*cost**8 - 12012*cost**6 + 6930*cost**4 - 1260*cost**2 + 35) / 128
        elif m == 1:
            return (715*cost**6 - 1001*cost**4 + 385*cost**2 - 35) * cost * sint * 9/16.
        elif m == 2:
            return (143*cost**6 - 143*cost**4 + 33*cost**2 - 1) * sint**2 * 315/16.
        elif m == 3:
            return (39*cost**4 - 26*cost**2 + 3) * cost * sint**3 * 3465/8.
        elif m == 4:
            return (65*cost**4 - 26*cost**2 + 1) * sint**4 * 10395/8.
        elif m == 5:
            return (5*cost**2 - 1) * cost * sint**5 * 135135/2.
        elif m == 6:
            return (15*cost**2 - 1) * sint**6 * 135135/2.
        elif m == 7:
            return 2027025 * cost * sint**7
        elif m == 8:
            return 2027025 * sint**8
    else:
        raise RuntimeError("The associated legendre polynomial order %d has not been implemented" % l)

if __name__ == "__main__":
    coeffs = torch.tensor([1., 2., 3.])
    print(legint(coeffs)) # (dc, 0.4, 0.6667, 0.6000)
