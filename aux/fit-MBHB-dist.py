import numpy as np
from math import floor
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import beta

def pdf(x, a, b, c):
    return [c * ((i/9)**(a-1)) * ((1-(i/9))**(b-1)) for i in x]

def f(z, pop):
    if z < 0.1 or z >= 9:
        return 0
    return pop[floor(z)]

colors = ["red", "blue", "green"]
labels = ["Pop III", "Delay", "No Delay"]

xdata = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5]

pop3 = [2.012, 7.002, 8.169, 5.412, 3.300, 1.590, 0.624, 0.141, 0.000]
N = sum(pop3)
print(f"N for Pop III (5 years): {N}")
pop3 = [i/N for i in pop3]

delay = [0.926, 4.085, 5.976, 5.131, 4.769, 2.656, 1.710, 0.644, 0.362]
N = sum(delay)
print(f"N for Delay (5 years): {N}")
delay = [i/N for i in delay]

nodelay = [3.682, 10.28, 9.316, 7.646, 4.909, 2.817, 1.187, 0.362, 0.161]
N = sum(nodelay)
print(f"N for No Delay (5 years): {N}")
nodelay = [i/N for i in nodelay]

i = 0
for pop in (pop3, delay, nodelay):
    popt, pcov = curve_fit(pdf, xdata, pop)

    line = np.linspace(0, 9, 1000).tolist()

    events = [f(i, pop) for i in line]
    plt.plot(line, events, color=colors[i], alpha=0.5)

    popt[0] = round(popt[0], 2)
    popt[1] = round(popt[1], 2)
    popt[2] = round(popt[2], 2)
    dist = pdf(line, popt[0], popt[1], popt[2])
    popt[2] = round(popt[2]/np.trapz(dist, x=line), 2)
    dist = pdf(line, popt[0], popt[1], popt[2])
    plt.plot(line, dist, color="dark"+colors[i], label=labels[i])
    print(f"{labels[i]}: a = {popt[0]}, b = {popt[1]},c = {popt[2]}")
    print(f"area for {labels[i]}: {np.trapz(dist, x=line)}")

    i += 1

plt.ylabel("f(z)", {"fontsize": 14})
plt.xlabel("z", {"fontsize": 14})
plt.legend()
plt.grid(alpha=0.5, zorder=0.5)
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
plt.show()
