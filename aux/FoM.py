#!/usr/bin/env python3

## FoM.py
# creates a figure of merit, for a given set of outputs
# this is done by computing the median of the area for each parameter in the 2 sigma region

import matplotlib.pyplot as plt
from statistics import median
import argparse

parser = argparse.ArgumentParser(description = "Compute the FoM")
parser.add_argument("-n", "--names", type=str, help="String with a Python like list with the names for each parameter, e.g.: \"['a', 'b']\". Must match the names present in the 'CIs.tex' file.", required=True)
parser.add_argument("-i", "--input", nargs="*", help="Input folder(s) with the same parameter space.", required=True)
parser.add_argument("-p", "--plot", nargs="*", help="Given two parameter names to be plotted in a 2D scatter plot.")
parser.add_argument("-a", "--annotate", type=str, help="Annotations for each input to show on plot.")
args = parser.parse_args()
names = eval(args.names)
input = args.input
plot = args.plot
annotate = eval(args.annotate) if args.annotate else None

d = {}
for name in names:
    d[name] = []

for folder in input:
    file = open(f"{folder}/CIs.tex", "r")
    content = file.read()
    header, sigma1, sigma2, = content.split("\n\n")

    sigma1 = sigma1.split("\n")[3:-2]
    sigma2 = sigma2.split("\n")[3:-3]

    for i in range(len(names)):
        if "\pm" in sigma2[i]:
            value, sigma = sigma2[i].replace(" ", "").replace("$", " ").replace("\pm", " ").split(" ")[3:5]
            value = float(value)
            sigma = float(sigma)
            area = round(2*sigma, 3)
        else:
            value, sigmalow, sigmahigh = sigma2[i].replace(" ", "").replace("$", " ").replace("^{+", " ").replace("}_{-", " ").replace("}", "").split(" ")[3:6]
            value = float(value)
            sigmalow = float(sigmalow)
            sigmahigh = float(sigmahigh)
            area = round(sigmalow + sigmahigh, 3)

        d[names[i]].append(area)

    file.close()

for i in range(len(names)):
    print(f"list of areas of {names[i]}: {d[names[i]]}")

    med = median(d[names[i]])
    medfolder = d[names[i]].index(med)
    print(f"median: {input[medfolder]}")

    mini = min(d[names[i]])
    minifolder = d[names[i]].index(mini)
    print(f"best: {input[minifolder]}")

    maxi = max(d[names[i]])
    maxifolder = d[names[i]].index(maxi)
    print(f"worst: {input[maxifolder]}")

    print()

if plot:
    plt.scatter(d[plot[0]], d[plot[1]], zorder=3.5)
    plt.xlabel(f"$\sigma_" + plot[0] + "$")
    plt.ylabel(f"$\sigma_" + plot[1] + "$")
    plt.grid(alpha=0.5, zorder=0.5)

    if annotate:
        for i, txt in enumerate(annotate):
            plt.annotate(txt, (d[plot[0]][i], d[plot[1]][i]))

    plt.show()
