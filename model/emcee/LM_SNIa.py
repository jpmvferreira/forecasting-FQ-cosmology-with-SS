# LM_SNIa.py
# ΛCDM model to be contrained using SNIa


# imports
from scipy.integrate import quad
from math import log
import numpy as np


# define the natural logarithm of the likelihood
def ln_likelihood(θ, redshifts, magnitudes, errors):
    Ωm = θ

    N = len(redshifts)
    A = 0
    B = 0
    C = 0

    for i in range(0, N):
        # H0 independent luminosity distance
        DL = (1+redshifts[i]) * quad(lambda Z: 1/(Ωm*(1+Z)**3 + (1-Ωm))**0.5, 0, redshifts[i])[0]

        # compute Δ(zᵢ)
        Δ = magnitudes[i] - 5*log(DL, 10)

        # perform the summation
        A += (Δ/errors[i])**2
        B += Δ/errors[i]**2
        C += 1/errors[i]**2

    return -A + B**2/C


# define the natural logarithm of the priors
def ln_prior(θ):
    Ωm = θ

    # flat priors
    if 0 < Ωm < 1:
        return 0.0

    return -np.inf


# define the probability using the prior and likelihood
def ln_probability(θ, redshifts, magnitudes, errors):
    prior = ln_prior(θ)
    if not np.isfinite(prior):
        return -np.inf
    return prior + ln_likelihood(θ, redshifts, magnitudes, errors)


# initialize this model and provide all relevant parameters
def initialize(nwalkers):
    # number of free parameters
    ndim = 1

    # initial values for each walker
    init = [0.284] + (0.1, ) * np.random.uniform(-1, 1, (nwalkers, ndim))

    # auxiliary names list
    names = ["Ω_m"]

    # labels for each variable
    labels = ["Ω_m"]

    # markers to show in the corner plot
    markers = {"Ω_m":0.284}

    return ndim, init, names, labels, markers
