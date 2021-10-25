# FQ_MBHB.py
# implementation of a simple cosmological model based on f(Q) geometry using MBHBs


# imports
from scipy.integrate import quad
from math import log, pi
import numpy as np


# define the natural logarithm of the likelihood
def ln_likelihood(θ, redshifts, distances, errors):
    N = len(redshifts)
    h, Ωm, M = θ

    sum = 0
    for i in range(0, N):
        # eletromagnetic light distance
        # c/H0 = 2.9979/h Gpc
        dLem = (1+redshifts[i]) * (2.9979/h) * quad(lambda Z: 1/(Ωm*(1+Z)**3 + (1-Ωm))**0.5, 0, redshifts[i])[0]

        # correction
        # M in units of H0
        correction = ( (2*6**0.5 + M) / (2*6**0.5 + M/(Ωm*(1+redshifts[i])**3 + (1-Ωm))**0.5))**0.5

        # gravitational wave light distance
        dLgw = correction * dLem

        sum += -log(errors[i]) - (distances[i] - dLgw)**2 / (2*errors[i]**2)

    return -N*log(2*pi)/2 + sum


# define the natural logarithm of the priors
def ln_prior(θ):
    h, Ωm, M = θ

    # flat priors
    if -4.5 < M < 10 and 0.2 < h < 1.2 and 0 < Ωm < 1:
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
    ndim = 3

    # initial values for each walker
    init = [0.7, 0.3, 2.0331] + (0.3, 0.3, 4) * np.random.uniform(0, 1, (nwalkers, ndim))

    # auxiliary names list
    names = ["h", "Ω_m", "M"]

    # labels for each variable
    labels = ["h", "Ω_m", "M"]

    # markers to show in the corner plot
    markers = {"h":0.7, "Ω_m":0.3, "M":0}

    return ndim, init, names, labels, markers
