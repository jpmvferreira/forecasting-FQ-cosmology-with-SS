## belgacem.py
# cosmological model from 1805.0873: ΛCDM with Ωm = 0.3087 and H0 = 67.64 km s⁻¹ Mpc⁻¹


# imports
from scipy.integrate import quad


# Hubble function
def H(z):
    # Hubble constant
    H0 = 67.64
    H0 = H0*3.240779289*10**(-20)

    # value for Ωm
    Ωm = 0.3087

    return H0*(Ωm*(1+z)**3 + 1-Ωm)**0.5


# luminosity distance
def dL(z, H):
    c = 9.715611890800001e-18  # speed of light [Gpc/s]
    return (1+z) * c * quad(lambda Z: 1/H(Z), 0, z)[0]


# description
description = "ΛCDM (Ωm = 0.3087, H0 = 67.64 km s⁻¹ Mpc⁻¹)"
