import numpy as np
import matplotlib.pyplot as plt
from ssfp import bssfp, gs_recon, planet
from ellipsinator import rotate_points
import seaborn

### Parameters ############################################################
TR1 = 3e-3
mult = 1.15  # TR2 = mult*TR1 -- harmonic TR
T1, T2 = 2, 1
alpha = np.deg2rad(100)  # high flip angle
# df = 1/(2.23234345*TR1)  # off-resonance -- what we're trying to estimate
df = 1/(.25*TR1)
###########################################################################

assert mult > 1, "TR2 should be greater than TR1"
TR2 = mult*TR1
M0 = 100

# A bunch of PCs to draw outline of ellipses
pcs = np.linspace(0, 2*np.pi, 5000, endpoint=False)
pcs = np.concatenate((pcs, [pcs[0]]))

# 4 PCs to find the linearized geometric solution
npcs = 4
pcs = np.concatenate((np.linspace(0, 2*np.pi, npcs, endpoint=False), pcs))

# Show ellipses formed using small flip angle -- shapes don't match!
alpha_small = np.deg2rad(3)
sig1_small_alpha = bssfp(
    T1, T2, TR1, alpha_small, 0, phase_cyc=pcs, M0=M0,
    delta_cs=0, phi_rf=0, phi_edd=0, phi_drift=0)
sig2_small_alpha = bssfp(
    T1, T2, TR2, alpha_small, 0, phase_cyc=pcs, M0=M0,
    delta_cs=0, phi_rf=0, phi_edd=0, phi_drift=0)

# ellipses with large flip angle match! not perfect, but really close
alpha_large = np.deg2rad(100)
sig1_large_alpha = bssfp(
    T1, T2, TR1, alpha_large, 0, phase_cyc=pcs, M0=M0,
    delta_cs=0, phi_rf=0, phi_edd=0, phi_drift=0)
sig2_large_alpha = bssfp(
    T1, T2, TR2, alpha_large, 0, phase_cyc=pcs, M0=M0,
    delta_cs=0, phi_rf=0, phi_edd=0, phi_drift=0)

plt.subplot(1, 2, 1)
plt.plot(sig1_small_alpha[npcs:].real, sig1_small_alpha[npcs:].imag, 'k--', label='TR1', linewidth=2)
plt.plot(sig2_small_alpha[npcs:].real, sig2_small_alpha[npcs:].imag, 'k:', label='TR2', linewidth=2)
plt.title(f'Small FA ({int(np.rad2deg(alpha_small))}$^\circ$)')
plt.xticks([], []), plt.yticks([], [])
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(sig1_large_alpha[npcs:].real, sig1_large_alpha[npcs:].imag, 'k--', label='TR1', linewidth=2)
plt.plot(sig2_large_alpha[npcs:].real, sig2_large_alpha[npcs:].imag, 'r:', label='TR2', linewidth=2)
plt.title(f'Large FA ({int(np.rad2deg(alpha_large))}$^\circ$)')
plt.xticks([], []), plt.yticks([], [])
plt.legend()

plt.show()

# Simulate the acquisitions using large flip angle -- shapes match!
sig1 = bssfp(
    T1, T2, TR1, alpha, df, phase_cyc=pcs, M0=M0,
    delta_cs=0, phi_rf=0, phi_edd=0, phi_drift=0)
sig2 = bssfp(
    T1, T2, TR2, alpha, df, phase_cyc=pcs, M0=M0,
    delta_cs=0, phi_rf=0, phi_edd=0, phi_drift=0)

# # Look at the ellipses
# plt.plot(sig1[npcs:].real, sig1[npcs:].imag, 'k--', label='TR1', linewidth=2)
# plt.plot(sig2[npcs:].real, sig2[npcs:].imag, 'r:', label='TR2', linewidth=2)
# plt.axis('square')
# plt.legend()

# # Look at the ellipses and 4 phase-cycles on each
# plt.plot(sig1[npcs:].real, sig1[npcs:].imag, 'k--', label='TR1', linewidth=2)
# plt.plot(sig2[npcs:].real, sig2[npcs:].imag, 'r:', label='TR2', linewidth=2)
# plt.plot(sig1[:npcs].real, sig1[:npcs].imag, 'r*', label='PCs TR1', linewidth=3)
# plt.plot(sig2[:npcs].real, sig2[:npcs].imag, 'k*', label='PCs TR2', linewidth=3)

# for ii in range(npcs):
#     plt.annotate(str(ii*90), (sig1.real[ii], sig1.imag[ii]))
#     plt.annotate(str(ii*90) + "'", (sig2.real[ii], sig2.imag[ii]))

# # Find geometric centers of both ellipses
ctr1 = gs_recon(sig1[:npcs], second_pass=False)
ctr2 = gs_recon(sig2[:npcs], second_pass=False)
# plt.plot(ctr1.real, ctr1.imag, 'ko', label='GS1', linewidth=3)
# plt.plot(ctr2.real, ctr2.imag, 'ro', label='GS2', linewidth=3)

# plt.axis('square')
# # plt.grid()
# plt.legend()
# plt.xticks([], []), plt.yticks([], [])
# seaborn.despine(ax=plt.gca(), offset=0)
# plt.show()

# If we had 4 phase-cycles on both ellipse, we simply rotate points back
phi = np.angle(ctr1*np.conj(ctr2))[0]
x, y = rotate_points(sig2[:npcs].real, sig2[:npcs].imag, phi)
if mult < 1:
    fac = -1/2
else:
    fac = 1
print('est off-res:', 1/(mult - 1)*phi/(fac*np.pi*TR1), 'true off-res:', df)

plt.plot(sig1[npcs:].real, sig1[npcs:].imag, 'k:', label='TR1', linewidth=2)
plt.plot(sig1[:npcs].real, sig1[:npcs].imag, 'r*', label='PCs TR1', linewidth=3)
for ii in range(npcs):
    plt.annotate(str(ii*90), (sig1.real[ii], sig1.imag[ii]))
    plt.annotate(str(ii*90), (x[ii], y[ii]))
plt.plot(x, y, 'kx', label='Rotated TR2 PCs', linewidth=3)
plt.axis('square')
plt.legend()
plt.xticks([], []), plt.yticks([], [])
plt.show()


assert False

# Take 4 points on the original ellipse and a single 180
# degree phase-cycle pair from the harmonic ellipse.
# Find the geometric center of the first ellipse and then
# and then rotate the line segment formed from the harmonic
# ellipse's phase-cycle pair back about the origin (always
# about origin?) until it intersects the geometric center
# of the original ellipse
plt.plot(sig1[npcs:].real, sig1[npcs:].imag, 'k--', label='TR1', linewidth=2)
plt.plot(sig2[npcs:].real, sig2[npcs:].imag, 'r:', label='TR2', linewidth=2)
pts = sig2[[0, 2]]
plt.plot(pts.real, pts.imag, 'k:.', linewidth=2)

# Do it the stupid way
def check(theta_, pts_, ctr_, tol=1e-1):
    xp, yp = rotate_points(pts_.real, pts_.imag, theta_)
    A = yp[0] - yp[1]
    B = xp[1] - xp[0]
    C = xp[0]*yp[1] - xp[1]*yp[0]
    in_seg = ctr_.real > np.min(xp) and ctr_.real < np.max(xp) and ctr_.imag > np.min(yp) and ctr_.imag < np.max(yp)
    return np.abs(A*ctr_.real + B*ctr_.imag + C) < tol and in_seg

theta = 0
while not check(theta, pts, ctr1) and theta < 2*np.pi:
    theta += 0.0001
print('est off-res:', 1/(mult - 1)*theta/(np.pi*TR1), 'true off-res:', df)
xp, yp = rotate_points(pts.real, pts.imag, theta)
plt.plot(xp, yp, 'k:.', linewidth=2)

plt.plot(ctr1.real, ctr1.imag, 'ko', label='GS1', linewidth=3)
plt.plot(ctr2.real, ctr2.imag, 'ro', label='GS2', linewidth=3)
plt.axis('square')
plt.legend()
plt.xticks([], []), plt.yticks([], [])
seaborn.despine(ax=plt.gca(), offset=0)
plt.show()

# Do PLANET using 4 + 2 phase-cycles
I = np.concatenate((x[:2] + 1j*y[:2], sig1[:npcs]))  # virtual ellipse
_Meff, T1est, T2est = planet(I[None, None, :], alpha=alpha, TR=TR1)
print('True T1:', T1, 'est T1:', T1est[0][0])
print('True T2:', T2, 'est T2:', T2est[0][0])
