## TO-DO:
# - meter incertezas no m e no b

from scipy.stats import linregress
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import os

l = [["FQ_LISA-12_SNIa-binned", "FQ_LISA-10_SNIa-binned", "FQ_LISA-9_SNIa-binned"],
    ["FQ_ET-4_SNIa-binned"],
    ["FQ_LISA-12_SNIa-binned_LIGO-2", "FQ_LISA-12_SNIa-binned_LIGO-1", "FQ_LISA-12_SNIa-binned_LIGO-13"]]

c = [["#8080ff", "#0000ff", "#000080"],
    ["red"],
    ["#80ff80", "#00ff00", "#008000"]]

labels = ["LISA", "ET", "LIGO"]
markers = ["o", "s", "P"]

legend_elements = []
for i in range(0, len(labels)):
    label = labels[i]
    marker = markers[i]
    legend_elements.append(Line2D([0], [0], marker=marker, color='w', label=label, markerfacecolor='black'))

h = []
M = []
for i in range(0, len(l)):
    observatory =  l[i]
    colors = c[i]
    label = labels[i]
    marker = markers[i]

    for j in range (0, len(observatory)):
        folder = observatory[j]
        color = colors[j]

        names = ["h", "Omega_m", "M"]
        d = {}
        for name in names:
            d[name] = []

        file = open(f"output/{folder}/CIs.tex", "r")

        content = file.read()
        header, sigma1, sigma2, = content.split("\n\n")

        sigma1 = sigma1.split("\n")[3:-2]
        sigma2 = sigma2.split("\n")[3:-3]

        for k in range(len(names)):
            if "\pm" in sigma2[k]:
                value, sigma = sigma2[k].replace(" ", "").replace("$", " ").replace("\pm", " ").split(" ")[3:5]
                value = float(value)
                sigma = float(sigma)
                area = round(2*sigma, 3)
            else:
                value, sigmalow, sigmahigh = sigma2[k].replace(" ", "").replace("$", " ").replace("^{+", " ").replace("}_{-", " ").replace("}", "").split(" ")[3:6]
                value = float(value)
                sigmalow = float(sigmalow)
                sigmahigh = float(sigmahigh)
                area = round(sigmalow + sigmahigh, 3)

            d[names[k]].append(area)

        file.close()

        h.extend(d["h"])
        M.extend(d["M"])
        plt.scatter(d["h"], d["M"], color=color, zorder=3.5, label=label, marker=marker)


res = linregress(h, y=M)
print(f"R² = {res.rvalue**2:.6f}")
print(f"m = {res.slope}, b = {res.intercept}")
plt.plot(h, [res.slope*i + res.intercept for i in h], color="black", linestyle="-", alpha = 0.25)
plt.xlabel("Δh")
plt.ylabel("ΔM")
plt.grid(alpha=0.5)
plt.legend(handles=legend_elements)
plt.show()
