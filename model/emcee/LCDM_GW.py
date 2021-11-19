# LCDM_GW.py
# implementation of ΛCDM using GW data


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
        dL = (1+redshifts[i]) * (2.9979/h) * quad(lambda Z: 1/(Ωm*(1+Z)**3 + (1-Ωm))**0.5, 0, redshifts[i])[0]
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
