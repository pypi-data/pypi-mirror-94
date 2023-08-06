'''Make some error plots like PLANET has.'''

import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

from ssfp import bssfp, planet
from ssfp.ismrm2021 import ormtre

if __name__ == '__main__':
    T1, T2 = .830, .08
    df = 10

    npcs = 10
    N = 64
    M = 100
    TRs = np.linspace(1e-3, 50e-3, N)
    alphas = np.linspace(0, np.deg2rad(90), N+1)[1:]
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)

    # sig = np.empty((N, N, npcs), dtype='complex')
    T1est = np.empty((N, N, M))
    T2est = np.empty((N, N, M))
    dfest = np.empty((N, N, M))
    sigma = 1e-5
    for ii in trange(N):
        for jj in range(N):
            sig = bssfp(
                np.ones(M)*T1, T2, TRs[ii], alphas[jj], field_map=df,
                phase_cyc=pcs, M0=1, target_pc_axis=-1)
            sig += sigma*(np.random.normal(0, 1, size=(M, npcs)) + 1j*np.random.normal(0, 1, size=(M, npcs)))
            _Meff, T1est[ii, jj, :], T2est[ii, jj, :], dfest[ii, jj, :] = planet(
                np.atleast_2d(sig), alphas[jj], TRs[ii])

    T1err = np.mean((T1est - T1)/T1, axis=-1)
    T2err = np.mean((T2est - T2)/T2, axis=-1)
    dferr = np.mean((dfest - df)/df, axis=-1)

    nx, ny = 1, 3
    plt.subplot(nx, ny, 1)
    plt.imshow(T1err)
    plt.colorbar()
    # plt.xticks(np.arange(N), alphas)

    plt.subplot(nx, ny, 2)
    plt.imshow(T2err)
    plt.colorbar()
    # plt.xticks(np.arange(N), alphas)

    plt.subplot(nx, ny, 3)
    plt.imshow(np.nan_to_num(dferr))
    plt.colorbar()
    # plt.xticks(np.arange(N), alphas)

    plt.show()
