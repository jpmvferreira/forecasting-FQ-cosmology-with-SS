# FQ_MBHB_SNIa_BNS.py
# implementation of a simple cosmological model based on f(Q) geometry using MBHBs and SNIa


# imports
from scipy.integrate import quad
from math import log, pi
import numpy as np


# define the natural logarithm of the likelihood
def ln_likelihood(θ, redshifts, distances, errors, candleredshifts, candlemagnitudes, candleerrors):
    h, Ωm, M = θ
    sum = 0

    # likelihood for the MBHB
    N = len(redshifts)
    for i in range(0, N):
        # eletromagnetic luminosity distance
        # c/H0 = 2.9979/h Gpc
        dLem = (1+redshifts[i]) * (2.9979/h) * quad(lambda Z: 1/(Ωm*(1+Z)**3 + (1-Ωm))**0.5, 0, redshifts[i])[0]

        # correction
        # M in units of H0
        correction = ( (2*6**0.5 + M) / (2*6**0.5 + M/(Ωm*(1+redshifts[i])**3 + (1-Ωm))**0.5))**0.5

        # gravitational wave luminosity distance
        dLgw = correction * dLem

        sum += -log(errors[i]) - (1/2) * ( (distances[i] - dLgw) / errors[i] )**2

    sum += -(N/2)*log(2*pi)

    # likelihood for the SNe
    N = len(candleredshifts)
    A = 0
    B = 0
    C = 0
    for i in range(0, N):
        # H0 independent luminosity distance
        DL = (1+candleredshifts[i]) * quad(lambda Z: 1/(Ωm*(1+Z)**3 + (1-Ωm))**0.5, 0, candleredshifts[i])[0]

        # compute Δ(zᵢ)
        Δ = candlemagnitudes[i] - 5*log(DL, 10)

        # perform the summation
        A += (Δ/candleerrors[i])**2
        B += Δ/candleerrors[i]**2
        C += 1/candleerrors[i]**2

    sum += -A + B**2/C

    return sum


# define the natural logarithm of the priors
def ln_prior(θ):
    h, Ωm, M = θ

    # flat priors
    if 0.2 < h < 1.2 and 0 < Ωm < 1 and -4.5 < M < 10:
        return 0.0

    return -np.inf


# define the probability using the prior and likelihood
def ln_probability(θ, redshifts, distances, errors, candlemagnitudes, candleredshifts, candleerrors):
    prior = ln_prior(θ)
    if not np.isfinite(prior):
        return -np.inf
    return prior + ln_likelihood(θ, redshifts, distances, errors, candlemagnitudes, candleredshifts, candleerrors)


# initialize this model and provide all relevant parameters
def initialize(nwalkers):
    # number of free parameters
    ndim = 3

    # initial values for each walker
    init = [0.7, 0.284, 0] + (0.1, 0.1, 4) * np.random.uniform(-1, 1, (nwalkers, ndim))

    # auxiliary names list
    names = ["h", "Ω_m", "M"]

    # labels for each variable
    labels = ["h", "Ω_m", "M"]

    # markers to show in the corner plot
    markers = {"h":0.7, "Ω_m":0.284, "M":0}

    return ndim, init, names, labels, markers
