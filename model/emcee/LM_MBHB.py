# LM_MBHB.py
# ΛCDM model to be contrained using MBHBs


# imports
from scipy.integrate import quad
from math import log, pi
import numpy as np


# define the natural logarithm of the likelihood
def ln_likelihood(θ, redshifts, distances, errors):
    N = len(redshifts)
    h, Ωm = θ

    sum = 0
    for i in range(0, N):
        # c/H0 = 2.9979/h Gpc
        dL = (1+redshifts[i]) * (2.9979/h) * quad(lambda Z: 1/(Ωm*(1+Z)**3 + (1-Ωm))**(1/2), 0, redshifts[i])[0]
        sum += -log(errors[i]) - (distances[i] - dL)**2 / (2*errors[i]**2)

    return -N*log(2*pi)/2 + sum


# define the natural logarithm of the priors
def ln_prior(θ):
    h, Ωm = θ

    # flat priors
    if 0.2 < h < 1.2 and 0 < Ωm < 1:
        return 0.0

    return -np.inf


# define the probability using the prior and likelihood
def ln_probability(θ, redshifts, distances, errors):
    prior = ln_prior(θ)
    if not np.isfinite(prior):
        return -np.inf
    return prior + ln_likelihood(θ, redshifts, distances, errors)


# initialize this model and provide all relevant parameters
def initialize(nwalkers):
    # number of free parameters
    ndim = 2

    # initial values for each walker
    init = [0.7, 0.3] + (0.1, 0.1) * np.random.uniform(-1, 1, (nwalkers, ndim))

    # auxiliary names list
    names = ["h", "Ω_m"]

    # labels for each variable
    labels = ["h", "Ω_m"]

    # markers to show in the corner plot
    markers = {"h":0.7, "Ω_m":0.3}

    return ndim, init, names, labels, markers
