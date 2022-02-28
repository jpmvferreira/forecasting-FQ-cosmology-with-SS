# imports
import matplotlib.pyplot as plt
import gwcatalog as gwc
import numpy as np
import scipy

# Hubble function without the Hubble constant
def E(z):
    Ωm = 0.284
    return (Ωm*(1+z)**3 + 1-Ωm)**0.5

# Hubble function
def H(z):
    # Hubble constant
    h = 0.7
    H0 = 299792458*h/(2.9979*3.085678*10**25)

    # matter density
    Ωm = 0.284

    return H0*E(z)


# standard luminosity distance
def dL(z, H):
    c = 9.715611890800001e-18  # speed of light [Gpc/s]
    return (1+z) * c * scipy.integrate.quad(lambda Z: 1/H(Z), 0, z)[0]

# luminosity distance for gravitational waves
def dLgw(z, H, E, M):
    return ((2*6**0.5 + M)/(2*6**0.5 + M/E(z)))**0.5*dL(z, H)

# equations to compute the minimum and maximum value for M
def fmin(M, z, dL, σ):
    return (2*6**0.5 + M)/(2*6**0.5 + M/E(z)) - (1 - σ/dL)**2

def fmax(M, z, dL, σ):
    return (2*6**0.5 + M)/(2*6**0.5 + M/E(z)) - (1 + σ/dL)**2

# LISA
redshifts = [i/100 for i in range(10, 901)]
redshifts, distances, errors = gwc.LISA(population="No Delay", redshifts=redshifts, ideal=True)
events = [0.57]
label = "LISA"

# ET
# redshifts = [i/100 for i in range(7, 201)]
# redshifts, distances, errors = gwc.ET(redshifts=redshifts, ideal=True)
# events = [0.93]
# label = "ET"

# LIGO (diverges! do not use!)
# redshifts = [i/100 for i in range(1, 20)]
# redshifts, distances, errors = gwc.LIGO(redshifts=redshifts, ideal=True)
# events = [0.01, 0.2]
# label = "LIGO"

# numerically solve to obtain the maximum and minimum value of M for each event
deltas = []
M_mins = []
M_maxs = []
for i in range(0, len(redshifts)):
    z_star = redshifts[i]

    M_min = scipy.optimize.fsolve(fmin, 0, args=(z_star, distances[i], errors[i]))[0]
    M_max = scipy.optimize.fsolve(fmax, 0, args=(z_star, distances[i], errors[i]))[0]

    M_mins.append(M_min)
    M_maxs.append(M_max)

    delta = M_max - M_min
    deltas.append(delta)

# print the results
mini = min(deltas)
print(f"min(ΔM(z)) = {mini}")
for i in range(0, len(deltas)):
    if np.isclose(deltas[i], mini):
        redshiftmini = redshifts[i]
        print(f"at z = {redshiftmini}")
        break

# plot ΔM vs z
plt.scatter(redshifts, deltas, marker=".", zorder=3.4, label=label)
plt.scatter(redshiftmini, mini, marker="x", color="red", zorder=3.5, label=f"z = {redshiftmini}, ΔM = {round(mini, 2)}")
plt.legend()
plt.grid(alpha=0.5)
plt.xlabel("z")
plt.ylabel("ΔM")
plt.show()
plt.close()

# plot luminosity distance curves for the desired events
for i in [int((z-redshifts[0])*100) for z in events]:
    markers, caps, bars = plt.errorbar(redshifts[i], distances[i], yerr=errors[i], fmt=".", markersize=7.5, color="#006FED", ecolor="#006FED", elinewidth=1, capsize=2, zorder=3.5)
    [bar.set_alpha(0.75) for bar in bars]
    [cap.set_alpha(0.75) for cap in caps]

    line = np.linspace(0, 9, 1000)  # LISA
    plt.xlim([-0.45, 9.45])         # .
    plt.ylim([-4.5, 115])           # .

    # line = np.linspace(0, 2, 1000)  # ET
    # plt.xlim([-0.045, 2.045])       # .
    # plt.ylim([-0.45, 20.5])         # .

    # line = np.linspace(0, 0.2, 1000)  # LIGO
    # plt.xlim([-0.005, 0.205])         # .
    # plt.ylim([-0.005, 0.2])           # .

    dLline = [dL(j, H) for j in line]
    dLgwmax = [dLgw(j, H, E, M_maxs[i]) for j in line]
    dLgwmin = [dLgw(j, H, E, M_mins[i]) for j in line]

    plt.grid()
    plt.xlabel("z")
    plt.ylabel("$d_L(z)$")
    plt.plot(line, dLline, label="$d_L(z)$", color="black", zorder=2.5, alpha=0.75)
    plt.plot(line, dLgwmax, label="$D^{(max)}_L(z)$", color="red", zorder=2.5, alpha=0.50)
    plt.plot(line, dLgwmin, label="$D^{(min)}_L(z)$", color="red", zorder=2.5, alpha=0.50)
    plt.legend()
    plt.show()
    plt.close()
