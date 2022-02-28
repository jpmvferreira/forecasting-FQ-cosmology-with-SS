import matplotlib.pyplot as plt
import os

LISA_others = ["FQ_LISA-1_SNIa-binned", "FQ_LISA-2_SNIa-binned", "FQ_LISA-3_SNIa-binned", "FQ_LISA-4_SNIa-binned", "FQ_LISA-5_SNIa-binned", "FQ_LISA-6_SNIa-binned", "FQ_LISA-7_SNIa-binned", "FQ_LISA-8_SNIa-binned", "FQ_LISA-11_SNIa-binned", "FQ_LISA-13_SNIa-binned", "FQ_LISA-14_SNIa-binned", "FQ_LISA-15_SNIa-binned"]
LISA_worst = ["FQ_LISA-12_SNIa-binned"]
LISA_median = ["FQ_LISA-10_SNIa-binned"]
LISA_best = ["FQ_LISA-9_SNIa-binned"]
ET = ["FQ_ET-1_SNIa-binned", "FQ_ET-2_SNIa-binned", "FQ_ET-2_SNIa-binned", "FQ_ET-4_SNIa-binned", "FQ_ET-5_SNIa-binned"]
l = [LISA_others, LISA_worst, LISA_median, LISA_best, ET]

colors = ["grey", "red", "yellow", "green", "blue"]
labels = ["LISA (others)", "LISA (worst)", "LISA (median)", "LISA (best)", "ET"]

for i in range (0, len(l)):
    folders = l[i]
    color = colors[i]
    label = labels[i]

    names = ["h", "Omega_m", "M"]
    d = {}
    for name in names:
        d[name] = []

    for folder in folders:
        file = open(f"output/{folder}/CIs.tex", "r")

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

    plt.scatter(d["h"], d["M"], color=color, label=label)

plt.xlabel("Δh")
plt.ylabel("ΔM")
plt.grid(alpha=0.5)
plt.legend()
plt.show()
