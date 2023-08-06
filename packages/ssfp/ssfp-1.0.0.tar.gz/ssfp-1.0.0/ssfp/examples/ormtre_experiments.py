'''Abstract simulation experiments.'''

from time import perf_counter
from typing import NamedTuple

import numpy as np
import matplotlib.pyplot as plt
from phantominator import shepp_logan

from ssfp import bssfp, planet
from ssfp.ismrm2021 import ormtre

class SimObj(NamedTuple):
    M0: np.ndarray
    T1: np.ndarray
    T2: np.ndarray
    df: np.ndarray
    dfTR: float
    I: np.ndarray
    TR: float
    alpha: float
    pcs: np.ndarray
    mask: np.ndarray
    SNR: float

def simsetup(N: int, TRs: list, alpha: float, npcs: list, sigma: float, avoid_sing: bool, short_df: bool) -> list:
    '''Create simulation scenarios for multiple TR ellipses.'''

    # reproducibility
    np.random.seed(0)

    # Shepp-Logan
    M0, T1, T2 = shepp_logan((N, N, 1), MR=True, zlims=(-.25, 0))
    M0 = np.squeeze(M0)
    T1 = np.squeeze(T1)
    T2 = np.squeeze(T2)

    # Simulate bSSFP acquisition with linear off-resonance
    # for each TR ellipse
    ret = []
    dfTR = min(TRs) # use the lowest TR for generating df maps
    for TR, npcs0 in zip(TRs, npcs):
        pcs = np.linspace(0, 2*np.pi, npcs0, endpoint=False)
        if avoid_sing:
            df, _ = np.meshgrid(
                np.linspace(1/(2*dfTR), 1/dfTR, N),
                np.linspace(1/(2*dfTR), 1/dfTR, N))
        else:
            if short_df:
                df, _ = np.meshgrid(
                    np.linspace(-1/(2*dfTR), 1/(2*dfTR), N),
                    np.linspace(-1/(2*dfTR), 1/(2*dfTR), N))
                    # np.linspace(-1/(1.25*dfTR), 1/(1.25*dfTR), N),
                    # np.linspace(-1/(1.25*dfTR), 1/(1.25*dfTR), N))
                # df /= 2
            else:
                df, _ = np.meshgrid(
                    np.linspace(-1/dfTR, 1/dfTR, N),
                    np.linspace(-1/dfTR, 1/dfTR, N))
        sig = bssfp(
            T1, T2, TR, alpha, field_map=df,
            phase_cyc=pcs, M0=M0, target_pc_axis=-1,
            phi_rf=0)

        # Do T1, T2 mapping for each pixel
        mask = np.abs(M0) > 1e-8

        # Make it noisy
        n = sigma*(np.random.normal(0, 1, sig.shape) +
                   1j*np.random.normal(0, 1, sig.shape))
        if sigma == 0:
            SNR = np.inf
        else:
            SNR = np.sqrt(1/sig.size*np.sum(np.abs(sig)**2))/np.sqrt(1/n.size*np.sum(np.abs(n)**2))
            SNR = 10*np.log10(SNR**2)
        sig += n*mask[..., None]
        ret.append(SimObj(
            M0=M0, T1=T1, T2=T2, df=df, dfTR=dfTR, I=sig, TR=TR, alpha=alpha,
            pcs=pcs, mask=mask, SNR=SNR))

    return ret

def dfexp(N: int, TRs: list, alpha: float, sigma: float, use4=False, t1t2_cmp=True, disp=True, short_df=False):
    simObjs = simsetup(
        N=N, TRs=TRs,
        alpha=alpha, npcs=[4, 4 if use4 else 2],
        sigma=sigma, avoid_sing=t1t2_cmp, short_df=short_df)
    p = simsetup(
        N=N, TRs=[min(TRs)],
        alpha=alpha, npcs=[8 if use4 else 6],
        sigma=sigma, avoid_sing=t1t2_cmp, short_df=short_df)[0]
    s0, s1 = simObjs[0], simObjs[1]

    # look at t1, t2 maps
    if t1t2_cmp and disp:
        _M0est, T1est, T2est, dfest = planet(p.I, alpha=p.alpha, TR=p.TR)

        # construct virtual ellipse and run planet
        phi = ormtre(s0.I, s1.I, s0.mask, s0.TR, s1.TR, rad=True)
        v = np.empty(p.I.shape, dtype=p.I.dtype)
        v[..., :4] = s0.I
        v[..., 4:] = s1.I*np.exp(1j*phi[..., None])
        try:
            _vM0est, vT1est, vT2est, vdfest = planet(v, alpha=s0.alpha, TR=(s0.TR + s1.TR)/2)
        except np.linalg.LinAlgError:
            raise ValueError('COULD NOT DO VIRTUAL ELLIPSE')


        T1mx = 5
        T1mn = 0
        T2mx = 3
        T2mn = -1

        # better contrast by doing this
        s0.T2[~s0.mask] = T2mn
        T2est[~s0.mask] = T2mn
        vT2est[~s0.mask] = T2mn

        nx, ny = 2, 3
        plt.subplot(nx, ny, 1)
        plt.imshow(s0.T1, vmin=T1mn, vmax=T1mx, cmap='gray')
        plt.title('True T1')
        plt.xticks([], []), plt.yticks([], [])

        plt.subplot(nx, ny, 2)
        plt.imshow(T1est, vmin=T1mn, vmax=T1mx, cmap='gray')
        plt.title('PLANET T1')
        plt.ylabel(f'Estimates, SNR={int(s0.SNR)}')
        plt.xticks([], []), plt.yticks([], [])

        plt.subplot(nx, ny, 3)
        plt.imshow(vT1est, vmin=T1mn, vmax=T1mx, cmap='gray')
        plt.title('Virt Ellipse T1')
        plt.xticks([], []), plt.yticks([], [])

        # compute diffs
        planet_diff = np.abs(s0.T1 - T1est)*s0.mask
        virtellipse_diff = np.abs(s0.T1 - vT1est)*s0.mask

        plt.subplot(nx, ny, 5)
        plt.imshow(planet_diff, cmap='gray')
        plt.ylabel('|True - Estimates|')
        plt.xticks([], []), plt.yticks([], [])
        plt.xlabel('mean/var: %.3e/%.3e' % (np.nanmean(planet_diff.flatten()), np.nanvar(planet_diff.flatten())))
        plt.colorbar()

        plt.subplot(nx, ny, 6)
        plt.imshow(virtellipse_diff, cmap='gray')
        plt.xticks([], []), plt.yticks([], [])
        plt.xlabel('mean/var: %.3e/%.3e' % (np.nanmean(virtellipse_diff.flatten()), np.nanvar(virtellipse_diff.flatten())))
        plt.colorbar()

        plt.show()

        nx, ny = 2, 3
        plt.subplot(nx, ny, 1)
        plt.imshow(s0.T2, vmin=T2mn, vmax=T2mx, cmap='gray')
        plt.title('True T2')
        plt.xticks([], []), plt.yticks([], [])

        plt.subplot(nx, ny, 2)
        plt.imshow(T2est, vmin=T2mn, vmax=T2mx, cmap='gray')
        plt.title('PLANET T2')
        plt.ylabel(f'Estimates, SNR={int(s0.SNR)}')
        plt.xticks([], []), plt.yticks([], [])

        plt.subplot(nx, ny, 3)
        plt.imshow(vT2est, vmin=T2mn, vmax=T2mx, cmap='gray')
        plt.title('Virt Ellipse T2')
        plt.xticks([], []), plt.yticks([], [])

        # compute diffs
        planet_diff = np.abs(s0.T2 - T2est)*s0.mask
        virtellipse_diff = np.abs(s0.T2 - vT2est)*s0.mask

        plt.subplot(nx, ny, 5)
        plt.imshow(planet_diff, cmap='gray')
        plt.ylabel('|True - Estimates|')
        plt.xticks([], []), plt.yticks([], [])
        plt.xlabel('mean/var: %.3e/%.3e' % (np.nanmean(planet_diff.flatten()), np.nanvar(planet_diff.flatten())))
        plt.colorbar()

        plt.subplot(nx, ny, 6)
        plt.imshow(virtellipse_diff, cmap='gray')
        plt.xticks([], []), plt.yticks([], [])
        plt.xlabel('mean/var: %.3e/%.3e' % (np.nanmean(virtellipse_diff.flatten()), np.nanvar(virtellipse_diff.flatten())))
        plt.colorbar()

        plt.show()

    elif not t1t2_cmp and disp:
        # look at off-resonance maps

        # do offres estimate using two gs_recon solutions
        theta = ormtre(s0.I, s1.I, s0.mask, s0.TR, s1.TR, rad=False)
        theta[np.abs(theta) > 2e3] = np.nan
        theta = np.nan_to_num(theta)
        # theta[np.abs(theta) > 300] = s0.df[np.abs(theta) > 300]
        # from skimage.restoration import unwrap_phase
        # theta = unwrap_phase(theta)
        # theta = np.unwrap(theta, axis=0)
        # theta *= 1/(s1.TR/s0.TR - 1)/(np.pi*s0.TR)

        # manually unwrap
        # _diff = theta - s0.df*s0.mask
        # theta[_diff > 200] -= 1/p.TR
        # _diff = np.abs(theta - s0.df*s0.mask)
        # theta[_diff > 200] += 1/p.TR
        # # _diff = np.abs(theta*s0.mask - s0.df*s0.mask)

        # do offres estimate using planet
        _M0est, _T1est, _T2est, dfest = planet(p.I, alpha=p.alpha, TR=p.TR)
        # from skimage.restoration import unwrap_phase
        # dfest = unwrap_phase(dfest)
        # dfest = np.unwrap(dfest, axis=0)

        plt.subplot(2, 3, 1)
        plt.imshow(s0.df*s0.mask, cmap='gray')
        plt.title('True Off-Res')
        plt.xticks([], []), plt.yticks([], [])
        plt.colorbar()

        # manually unwrap
        planet_diff = dfest - s0.df*s0.mask
        dfest[planet_diff > 200] -= 1/p.TR
        planet_diff = np.abs(dfest - s0.df*s0.mask)
        dfest[planet_diff > 200] += 1/p.TR
        planet_diff = np.abs(dfest*s0.mask - s0.df*s0.mask)

        plt.subplot(2, 3, 2)
        plt.imshow(dfest, cmap='gray')
        plt.xticks([], []), plt.yticks([], [])
        plt.title(f'PLANET Off-Res ({p.I.shape[-1]} PCs)')
        plt.ylabel(f'Estimates, SNR={int(s0.SNR)}')
        plt.colorbar()

        plt.subplot(2, 3, 3)
        plt.imshow(theta*s0.mask, cmap='gray')
        plt.xticks([], []), plt.yticks([], [])
        plt.title(f'Multi-TR Off-Res ({s0.I.shape[-1]}+{s1.I.shape[-1]} PCs)')
        plt.colorbar()

        mtr_diff = np.abs(theta*s0.mask - s0.df*s0.mask)

        plt.subplot(2, 3, 5)
        plt.imshow(planet_diff, cmap='gray')
        plt.ylabel('|Truth - Estimates|')
        plt.xticks([], []), plt.yticks([], [])
        plt.xlabel('mean/var: %.3e/%.3e' % (np.nanmean(planet_diff.flatten()), np.nanvar(planet_diff.flatten())))
        plt.colorbar()

        plt.subplot(2, 3, 6)
        plt.imshow(mtr_diff, cmap='gray')
        plt.xticks([], []), plt.yticks([], [])
        plt.xlabel('mean/var: %.3e/%.3e' % (np.nanmean(mtr_diff.flatten()), np.nanvar(mtr_diff.flatten())))
        plt.colorbar()

        plt.show()

    # Return error
    if not disp:
        # do offres estimate using two gs_recon solutions
        theta = ormtre(s0.I, s1.I, s0.mask, s0.TR, s1.TR)

        # do offres estimate using planet
        _M0est, T1est, T2est, dfest = planet(p.I, alpha=p.alpha, TR=p.TR)

        # construct virtual ellipse and run planet
        if s1.I.shape[-1] == 4:
            phi = ormtre(s0.I, s1.I, s0.mask, s0.TR, s1.TR, rad=True)
            v = np.empty(p.I.shape, dtype=p.I.dtype)
            v[..., 0::2] = s0.I
            v[..., 1::2] = s1.I*np.exp(1j*phi[..., None])
            _vM0est, vT1est, vT2est, vdfest = planet(v, alpha=s0.alpha, TR=(s0.TR + s1.TR)/2)
        else:
            vT1est = np.zeros(theta.shape)
            vT2est = np.zeros(theta.shape)
            vdfest = np.zeros(theta.shape)

        from skimage.metrics import normalized_root_mse as nrmse
        planetT1err = nrmse(s0.T1[~np.isnan(T1est)], (T1est*s0.mask)[~np.isnan(T1est)])
        planetT2err = nrmse(s0.T2[~np.isnan(T2est)], (T2est*s0.mask)[~np.isnan(T2est)])
        planetdferr = nrmse((s0.df*s0.mask)[~np.isnan(dfest)], (dfest*s0.mask)[~np.isnan(dfest)])
        virtT1err = nrmse(s0.T1[~np.isnan(vT1est)], (vT1est*s0.mask)[~np.isnan(vT1est)])
        virtT2err = nrmse(s0.T2[~np.isnan(vT2est)], (vT2est*s0.mask)[~np.isnan(vT2est)])
        virtdferr = nrmse((s0.df*s0.mask)[~np.isnan(vdfest)], (vdfest*s0.mask)[~np.isnan(vdfest)])
        ormtrerr = nrmse((s0.df*s0.mask)[~np.isnan(theta)], (theta*s0.mask)[~np.isnan(theta)])

        if t1t2_cmp:
            return(
                planetT1err,
                planetT2err,
                virtT1err,
                virtT2err,
            ), s0.SNR
        return(
            planetdferr,
            virtdferr,
            ormtrerr,
        ), s0.SNR


if __name__ == '__main__':
    N = 512
    TR0 = 3e-3
    TRs = [TR0, 1.15*TR0]
    alpha = np.deg2rad(100)  # high flip angle (doesn't have to be if not using PLANET)
    alpha_lo = np.deg2rad(10)

    # T1/T2 maps
    # dfexp(N=N, TRs=TRs, alpha=alpha, sigma=1e-5, use4=True, t1t2_cmp=True, disp=True)
    # dfexp(N=N, TRs=TRs, alpha=alpha, sigma=1e-8, use4=False, t1t2_cmp=True, disp=True)

    # # off-resonance maps
    # dfexp(N=N, TRs=TRs, alpha=alpha, sigma=1e-5, use4=True, t1t2_cmp=False, disp=True)
    # dfexp(N=N, TRs=TRs, alpha=alpha, sigma=1e-5, use4=False, t1t2_cmp=False, disp=True, short_df=True)

    # Do SNR comparisons
    nSNR = 10
    t1t2_err = np.empty((4, nSNR))
    # t1t2_err_lo_alpha = np.empty((4, nSNR))
    df_err = np.empty((3, nSNR))
    df_err_lo_alpha = np.empty((3, nSNR))
    SNR = np.empty(nSNR)
    N = 64
    for ii, sigma in enumerate(np.linspace(1e-10, 1e-5, nSNR)[::-1]):
        print(ii)
        t1t2_err[:, ii], SNR[ii] = dfexp(N=N, TRs=TRs, alpha=alpha, sigma=sigma, use4=True, t1t2_cmp=True, disp=False)
        # t1t2_err_lo_alpha[:, ii], SNR[ii] = dfexp(N=N, TRs=TRs, alpha=alpha_lo, sigma=sigma, use4=True, t1t2_cmp=True, disp=False)
        df_err[:, ii], SNR[ii] = dfexp(N=N, TRs=TRs, alpha=alpha, sigma=sigma, use4=True, t1t2_cmp=False, disp=False, short_df=True)
        df_err_lo_alpha[:, ii], SNR[ii] = dfexp(N=N, TRs=TRs, alpha=alpha_lo, sigma=sigma, use4=True, t1t2_cmp=False, disp=False, short_df=True)
    print(SNR)

    alpha_lo = int(np.rad2deg(alpha_lo))
    alpha = int(np.rad2deg(alpha))
    nx, ny = 3, 1
    plt.subplot(nx, ny, 1)
    plt.plot(t1t2_err[0, :], 'k:', label=f'PLANET (FA={alpha}$^o$)', linewidth=1.5)
    plt.plot(t1t2_err[2, :], 'k--', label=f'Virt Ellipse (FA={alpha}$^o$)', linewidth=1.5)
    # plt.plot(t1t2_err_lo_alpha[0, :], 'k:', label=f'PLANET (FA={alpha_lo})')
    # plt.plot(t1t2_err_lo_alpha[2, :], 'k--', label=f'Virt Ellipse (FA={alpha_lo})')
    plt.xticks([], [])
    plt.legend()
    plt.ylabel(f'T1 NRMSE')

    plt.subplot(nx, ny, 2)
    plt.plot(t1t2_err[1, :], 'k:', label=f'PLANET (FA={alpha}$^o$)', linewidth=1.5)
    plt.plot(t1t2_err[3, :], 'k--', label=f'Virt Ellipse (FA={alpha}$^o$)', linewidth=1.5)
    # plt.plot(t1t2_err_lo_alpha[1, :], 'k:', label='PLANET (lo)')
    # plt.plot(t1t2_err_lo_alpha[3, :], 'k--', label='Virt Ellipse (lo)')
    plt.xticks([], [])
    plt.legend()
    plt.ylabel(f'T2 NRMSE')

    plt.subplot(nx, ny, 3)
    plt.plot(df_err[0, :], 'k:', label=f'PLANET (FA={alpha}$^o$)', linewidth=1.5)
    plt.plot(df_err[2, :], 'r-', label=f'Multi-TR (FA={alpha}$^o$)', linewidth=1.5)
    plt.plot(df_err_lo_alpha[0, :], 'k-.', label=f'PLANET (FA={alpha_lo}$^o$)', linewidth=1.5)
    plt.plot(df_err_lo_alpha[2, :], 'r--', label=f'Multi-TR (FA={alpha_lo}$^o$)', linewidth=1.5)
    plt.ylabel(f'$\Delta$f NRMSE')
    plt.xticks(np.arange(nSNR), SNR.round())
    plt.xlabel('SNR')
    plt.legend()

    # plt.subplot(nx, ny, 4)
    # plt.plot(df_err[0, :], 'k-', label='PLANET')
    # plt.plot(df_err[2, :], 'k:', label='Multi-TR')
    # plt.ylabel(f'$\Delta$f NRMSE (FA={int(np.rad2deg(alpha_lo))}$^o$)')
    # plt.xticks(np.arange(nSNR), SNR.round())
    # plt.legend()
    # plt.xlabel('SNR')

    plt.show()
