import numpy  as np
from scipy.special import *

def djn(n,z):
    dj = 0.5*(jn(n-1,z) - jn(n+1,z));
    return dj

def dkn(n,z):
    dk = -0.5*(kn(n-1,z) + kn(n+1,z));
    return dk
    
def findzeros(x,y):
    # Zero finding algorithm.
    # Find the zeros of a function y(x)
      

    # First the simple part: find any zeros in the vector    
    zind = (y==0)    
    
    # Next find position of any sign changes
    signchange = y[0:-2] * y[1:-1]
    scind = np.nonzero(signchange < 0)
    scind = np.transpose(scind) # This step seems necessary to get the final shape correct

    # Now apply linear interpolation to find a more accurate
    # estimate of the position of the zero
    xzsc = x[scind]
    for ll in range(0,max(np.shape(scind))-1):
        xzsc[ll] = x[scind[ll]] - y[scind[ll]] / ( ( y[scind[ll]+1] - y[scind[ll]] ) / (x[scind[ll]+1] - x[scind[ll]]) ) 
        
    # Flatten to a 1D array before returning    
    xzsc = xzsc.flatten()

    # Combine and sort the zero-crossing values
    xz = np.concatenate((xzsc,x[zind]))
    xz = np.sort(xz)
    return xz
        

def SolveHybridModeEVE(V,n,l,nco,ncl):
    # Define a finite range over which to look for solutions
    Us = np.linspace(0,V,10000)
    # Define w parameter    
    Ws = np.sqrt(V**2-Us**2)

    # Avoid division by zero or invalid values in Ws
    eps = np.finfo(float).eps  # Machine epsilon
    Ws[Ws < eps] = eps
    
    # LHS of the eigenvalue equation
    LHS1 = (0.5 * (jn(n-1, Us) - jn(n+1, Us)) / (Us * jn(n, Us) + eps)) - (0.5 * (kn(n-1, Ws) + kn(n+1, Ws)) / (Ws * kn(n, Ws) + eps))
    LHS2 = (0.5 * (jn(n-1, Us) - jn(n+1, Us)) / (Us * jn(n, Us) + eps)) - ((ncl/nco)**2 * 0.5 * (kn(n-1, Ws) + kn(n+1, Ws)) / (Ws * kn(n, Ws) + eps))
    LHS = LHS1 * LHS2

    # RHS of EVE
    RHS = (n**2)*(1.0/(Us**2 + eps) + 1.0/(Ws**2 + eps))*(1.0/(Us**2 + eps) + ((ncl/nco)**2)*(1.0/(Ws**2 + eps)))

    # Solve
    zeroUs = findzeros(Us,LHS-RHS); # Zero finding algorithm


    # Sort and extract the lth solution to give the
    # (n,l)th mode
    if (len(zeroUs)>=l):
        Usol = zeroUs[l-1]
    else:
        Usol = V
        # Check solution, issue a warning if nothing found
        print("WARNING: no solution for this m in chosen range")
              
    return Usol

# HEモードの電場計算
def CalcHEMode(a, nco, ncl, n, l, lam, psi, R, T, propDir):
    k = 2 * np.pi / lam

    # 規格化周波数V
    V = k * a * np.sqrt(nco**2 - ncl**2)

    # 固有値Uを求める
    U = SolveHybridModeEVE(V, n, l, nco, ncl)
    if U is None:
        print(f"Error: No solution found for mode (n={n}, l={l}).")
        return None, None, None

    # 伝播定数β
    beta = np.sqrt(k**2 * nco**2 - (U / a)**2) if propDir == True else - np.sqrt(k**2 * nco**2 - (U / a)**2)
    W = np.sqrt(V**2 - U**2)


    # 電場分布の補正係数
    s = n * (1/(U**2) + 1/(W**2)) / (djn(n,U)/(U * jn(n,U)) + dkn(n,W)/(W * kn(n,W)))

    # 電場分布
    Er = np.where(
        R < a,
        -1j * beta * (a / U) * ((1 - s) / 2 * jn(n-1, U / a * R) - (1 + s) / 2 * jn(n+1, U / a * R)) * np.cos(n * T + psi),
        -1j * beta * (a * jn(n, U)) / (W * kn(n, W)) * ((1 - s) / 2 * kn(n - 1, W / a * R) + (1 + s) / 2 * kn(n + 1, W / a * R)) * np.cos(n * T + psi)
    )

    Et = np.where(
        R < a,
        1j * beta * (a / U) * ((1 - s) / 2 * jn(n-1, U / a * R) + (1 + s) / 2 * jn(n+1, U / a * R)) * np.sin(n * T + psi),
        1j * beta * (a * jn(n, U)) / (W * kn(n, W)) * ((1 - s) / 2 * kn(n - 1, W / a * R) - (1 + s) / 2 * kn(n + 1, W / a * R)) * np.sin(n * T + psi)
    )

    Ez = np.where(
        R < a,
        jn(n, U / a * R) * np.cos(n * T + psi),
        (jn(n, U) / kn(n, W)) * kn(n, W / a * R) * np.cos(n * T + psi)
    )

    Ex = Er * np.cos(T) - Et * np.sin(T)
    Ey = Er * np.sin(T) + Et * np.cos(T)

    return Ex, Ey, Ez


# Example usage:
if __name__ == "__main__":
    a = 200e-9  #fiber radius
    nco = 1.45  # Core refractive index
    ncl = 1.00  # Cladding refractive index
    n = 1    # Mode number
    l = 1    # Order of the mode
    lam = 785e-9 #wavelength
    psi = np.pi/2.0 #phase of quasi-y pol.
    R = a   #radial distance
    alpha = 0.8 * np.pi/2.  #angle <T in the function>
    propDir = 0 #propagation direction: 0 -> plus z-dir, 1 -> minus z-dir

    E = np.array(CalcHEMode(a, nco, ncl, n, l, lam, psi, R, alpha, propDir))
    print(E)