# FQ_GW_SNIa_GW.py
# implementation of a simple cosmological model based on f(Q) geometry using two sources of GW and SNIa


# imports
from scipy.integrate import quad
from math import log, pi
import numpy as np


# define the natural logarithm of the likelihood
def ln_likelihood(theta, redshifts, distances, errors, candleredshifts, candlemagnitudes, candleerrors, bnsredshifts, bnsdistances, bnserrors):
    h, Omega_m, M = theta
    sum = 0

    # likelihood for the first source of GW
    N = len(redshifts)
    for i in range(0, N):
        # eletromagnetic luminosity distance
        # c/H0 = 2.9979/h Gpc
        dLem = (1+redshifts[i]) * (2.9979/h) * quad(lambda Z: 1/(Omega_m*(1+Z)**3 + (1-Omega_m))**0.5, 0, redshifts[i])[0]

        # correction
        # M in units of H0
        correction = ( (2*6**0.5 + M) / (2*6**0.5 + M/(Omega_m*(1+redshifts[i])**3 + (1-Omega_m))**0.5))**0.5

        # gravitational wave luminosity distance
        dLgw = correction * dLem

        sum += -log(errors[i]) - (1/2) * ( (distances[i] - dLgw) / errors[i] )**2

    sum += -(N/2)*log(2*pi)

    # likelihood for the SNIa
    N = len(candleredshifts)
    A = 0
    B = 0
    C = 0
    for i in range(0, N):
        # H0 independent luminosity distance
        DL = (1+candleredshifts[i]) * quad(lambda Z: 1/(Omega_m*(1+Z)**3 + (1-Omega_m))**0.5, 0, candleredshifts[i])[0]

        # compute Δ(zᵢ)
        Δ = candlemagnitudes[i] - 5*log(DL, 10)

        # perform the summation
        A += (Δ/candleerrors[i])**2
        B += Δ/candleerrors[i]**2
        C += 1/candleerrors[i]**2

    sum += -A + B**2/C

    # likelihood for the second source of GW
    N = len(bnsredshifts)
    for i in range(0, N):
        # eletromagnetic luminosity distance
        # c/H0 = 2.9979/h Gpc
        dLem = (1+bnsredshifts[i]) * (2.9979/h) * quad(lambda Z: 1/(Omega_m*(1+Z)**3 + (1-Omega_m))**0.5, 0, bnsredshifts[i])[0]

        # correction
        # M in units of H0
        correction = ( (2*6**0.5 + M) / (2*6**0.5 + M/(Omega_m*(1+bnsredshifts[i])**3 + (1-Omega_m))**0.5))**0.5

        # gravitational wave luminosity distance
        dLgw = correction * dLem

        sum += -log(bnserrors[i]) - (1/2) * ( (bnsdistances[i] - dLgw) / bnserrors[i] )**2

    sum += -(N/2)*log(2*pi)

    return sum


# define the natural logarithm of the priors
def ln_prior(theta):
    h, Omega_m, M = theta

    # flat priors
    if 0.2 < h < 1.2 and 0 < Omega_m < 1 and −4.89897948556635619639 < M < 10:
        return 0.0

    return -np.inf


# define the probability using the prior and likelihood
def ln_probability(theta, redshifts, distances, errors, candlemagnitudes, candleredshifts, candleerrors, bnsredshifts, bnsdistances, bnserrors):
    prior = ln_prior(theta)
    if not np.isfinite(prior):
        return -np.inf
    return prior + ln_likelihood(theta, redshifts, distances, errors, candlemagnitudes, candleredshifts, candleerrors, bnsredshifts, bnsdistances, bnserrors)
