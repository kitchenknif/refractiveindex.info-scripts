# -*- coding: utf-8 -*-

# Original data: Chernova et al. 2017, https://doi.org/10.1364/OME.7.003844

# Kramers-Kroning Integration https://doi.org/10.1366/0003702884430380

# Version history
# 2025-02-19 first version (Pavel Dmitriev)
# 2025-02-27 simplify output (Misha Polyanskiy)
#

import numpy as np
import matplotlib.pyplot as plt
def generate_epsilon(num_points=10000, min_ev=0.01, max_ev=30.):
    auxfuncs = __import__("Chernova 2017 - Aux funcs")


    # Model parameters
    E = [3.91, 4.19, 4.76, 5.03, 6.05, 6.28, 6.4, 8.3, 9.47]
    Amplitude = [1.16, 4.39, 2.32, 5.58, 2.53, 0.4, 1.37, 0.09, 4.32]
    FWHM = [0.23, 0.53, 0.42, 1.33, 1.99, 0.27, 0.48, 0.21, 3.39]

    UV_E = 15.8
    UV_Amplitude = 222

    eps_inf = 1

    # Simulate range
    eV = np.linspace(min_ev, max_ev, num_points, True)

    epsilon_1_UV = [UV_Amplitude / (UV_E ** 2 - e ** 2) for e in eV]

    eps_1 = np.add(eps_inf, epsilon_1_UV)
    eps_2 = np.zeros(eV.shape)

    for i in range(len(E)):
        eps_1_osc, eps_2_osc = auxfuncs.gaussian(eV, E[i], Amplitude[i], FWHM[i])

        eps_1 += eps_1_osc
        eps_2 += eps_2_osc

    epsilon = eps_1 + 1j * eps_2

    return eV, epsilon


if __name__ == "__main__":

    eV, epsilon = generate_epsilon()

    n = (epsilon ** .5).real
    k = (epsilon ** .5).imag

    #
    # Interpolate to data range
    #
    # Model range
    fit_points = 100
    fit_eV = np.linspace(0.74, 8.8, fit_points, True)

    n_interp = np.interp(fit_eV, eV, n)
    k_interp = np.interp(fit_eV, eV, k)

    wl_um = np.divide(1.23984193, fit_eV)

    # ============================   DATA OUTPUT   =================================
    file = open('out.txt', 'w')
    for i in range(fit_points - 1, -1, -1):
        file.write('\n        {:.4e} {:.4e} {:.4e}'.format(wl_um[i], n_interp[i], k_interp[i]))
    file.close()

    # ===============================   PLOT   =====================================
    # plot n vs eV
    plt.figure(1)
    plt.plot(fit_eV, n_interp)
    plt.xlabel('Photon energy (eV)')
    plt.ylabel('n')

    # plot n vs eV
    plt.figure(2)
    plt.plot(fit_eV, k_interp)
    plt.xlabel('Photon energy (eV)')
    plt.ylabel('k')

    # plot n,k vs μm
    plt.figure(3)
    plt.plot(wl_um, n_interp, label="n")
    plt.plot(wl_um, k_interp, label="k")
    plt.xlabel('Wavelength (μm)')
    plt.ylabel('n, k')
    plt.legend(bbox_to_anchor=(0, 1.02, 1, 0), loc=3, ncol=2, borderaxespad=0)

    plt.show()