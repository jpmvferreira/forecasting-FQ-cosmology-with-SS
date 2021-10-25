# LM_MBHB_SNIa.py
# ΛCDM model to be contrained using MBHBs and SNIa


# imports
from scipy.integrate import quad
from math import log, pi
import numpy as np


# define the natural logarithm of the likelihood
def ln_likelihood(θ, redshifts, distances, errors, candleredshifts, candlemagnitudes, candleerrors):
    h, Ωm = θ
    sum = 0

    # likelihood for the MBHBs
    N = len(redshifts)
    for i in range(0, N):
        # c/H0 = 2.9979/h Gpc
        dL = (1+redshifts[i]) * (2.9979/h) * quad(lambda Z: 1/(Ωm*(1+Z)**3 + (1-Ωm))**(1/2), 0, redshifts[i])[0]
        sum += -log(errors[i]) - (distances[i] - dL)**2 / (2*errors[i]**2)

    sum += -N*log(2*pi)/2 + sum

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
    h, Ωm = θ

    # flat priors
    if 0.2 < h < 1.2 and 0 < Ωm < 1:
        return 0.0

    return -np.inf


# define the probability using the prior and likelihood
def ln_probability(θ, redshifts, distances, errors, candleredshifts, candlemagnitudes, candleerrors):
    prior = ln_prior(θ)
    if not np.isfinite(prior):
        return -np.inf
    return prior + ln_likelihood(θ, redshifts, distances, errors, candleredshifts, candlemagnitudes, candleerrors)


# initialize this model and provide all relevant parameters
def initialize(nwalkers):
    # number of free parameters
    ndim = 2

    # initial values for each walker
    init = [0.7, 0.284] + (0.1, 0.1) * np.random.uniform(-1, 1, (nwalkers, ndim))

    # auxiliary names list
    names = ["h", "Ω_m"]

    # labels for each variable
    labels = ["h", "Ω_m"]

    # markers to show in the corner plot
    markers = {"h":0.7, "Ω_m":0.284}

    return ndim, init, names, labels, markers
