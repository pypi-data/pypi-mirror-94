'''Run PLANET on water phantom.'''

import pathlib

import numpy as np
import matplotlib.pyplot as plt

from ssfp import gs_recon, planet, robustcc
from ssfp.ismrm2021 import ormtre

def mc_planet(data, alpha, TR):
    nx, ny, nc, _npcs = data.shape[:]
    T1est = np.zeros((nx, ny))
    T2est = np.zeros((nx, ny))
    dfest = np.zeros((nx, ny))
    for jj in range(nc):
        _, T1, T2, df = planet(data[..., jj, :], alpha=alpha, TR=TR, pc_axis=-1)
        T1est += T1
        T2est += T2
        dfest += df
    T1est /= nc
    T2est /= nc
    dfest /= nc
    return T1est, T2est, dfest

def plt_trio(T1est, T2est, dfest, TR, ii=0):
    plt.subplot(2, 3, 3*ii+1)
    plt.imshow(T1est, vmin=0, vmax=.1)
    plt.xticks([], []), plt.yticks([], [])
    plt.title('PLANET T1')
    plt.ylabel(f'TR={TR}')

    plt.subplot(2, 3, 3*ii+2)
    plt.imshow(T2est, vmin=0, vmax=.1)
    plt.xticks([], []), plt.yticks([], [])
    plt.title('PLANET T2')

    plt.subplot(2, 3, 3*ii+3)
    plt.imshow(dfest, vmin=-1/TR0, vmax=1/TR0)
    plt.xticks([], []), plt.yticks([], [])
    plt.title('PLANET $\Delta$f')


if __name__ == '__main__':

    if not pathlib.Path('data/tr6.npy').exists():
        # load data
        data0 = np.load('data/set1_tr6_te3.npy')
        data1 = np.load('data/set1_tr12_te6.npy')
        # dims: (nx, ny, coils, avgs, npcs)
        # collapse average axis
        data0 = np.mean(data0, axis=3)
        data1 = np.mean(data1, axis=3)

        # trim oversampling
        trim = data0.shape[0]//4
        data0 = data0[trim:-trim, ...]
        data1 = data1[trim:-trim, ...]
        nx, ny, nc, npcs = data0.shape[:]
        print(data0.shape)

        # only 8 phase-cycles on each
        data0 = data0[..., ::2]
        data1 = data1[..., ::2]

        np.save('data/tr6.npy', data0)
        np.save('data/tr12.npy', data1)
    else:
        data0 = np.load('data/tr6.npy')
        data1 = np.load('data/tr12.npy')
    TR0, TR1 = 6e-3, 12e-3
    alpha = np.deg2rad(70)
    nx, ny, nc, npcs = data0.shape[:]

    # # try planet
    # for ii, (data, TR) in enumerate(zip((data0, data1), (TR0, TR1))):
    #     T1est, T2est, dfest = mc_planet(data, alpha, TR)
    #     plt_trio(T1est, T2est, dfest, TR=TR, ii=ii)
    # plt.show()

    # Try virtual ellipse
    mask = None
    virt = np.empty((nx, ny, nc, npcs), dtype=data0.dtype)
    vTR = (TR0+TR1)/2
    for ii in range(nc):
        phi = ormtre(data0[..., ii, ::2], data1[..., ii, 1::2], mask, TR0, TR1, rad=True)
        virt[..., ii, 0::2] = data0[..., ii, 0::2]
        virt[..., ii, 1::2] = data1[..., ii, 1::2]*np.exp(1j*phi[..., None])
    T1est, T2est, dfest = mc_planet(virt, alpha, vTR)
    # plt_trio(T1est, T2est, dfest, TR=vTR)
    # plt.show()

    mask = None
    dfest_ormtre = np.zeros((nx, ny))
    for ii in range(nc):
        df = ormtre(data0[..., ii, 0::2], data1[..., ii, 1::2], mask, TR0=TR0, TR1=TR1)
        dfest_ormtre += df
    dfest_ormtre /= nc

    plt.subplot(1, 2, 1)
    plt.imshow(dfest)
    plt.title('PLANET $\Delta$f (8 phase-cycles)')
    plt.xticks([], []), plt.yticks([], [])

    plt.subplot(1, 2, 2)
    plt.imshow(dfest_ormtre)
    plt.title('Multi-TR $\Delta$f (4+4 phase-cycles)')
    plt.xticks([], []), plt.yticks([], [])

    plt.show()

    # dfest = np.zeros((nx, ny))
    # for ii in range(nc):
    #     df = ormtre(data0[..., ii, 0::2], data1[..., ii, ::4], mask, TR0=TR0, TR1=TR1)
    #     dfest += df
    # dfest += df
    # plt.imshow(dfest)
    # plt.show()
