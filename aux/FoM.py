## FoM.py
# creates a figure of merit, for a given set of outputs
# this is done by computing the median of the area for each parameter in the 2 sigma region

from statistics import median
import argparse

parser = argparse.ArgumentParser(description = "Compute the FoM")
parser.add_argument("-n", "--names", type=str, help="String with a Python like list with the names for each parameter, e.g.: \"['a', 'b']\". Must match the names present in the 'CIs.tex' file.", required=True)
parser.add_argument("-i", "--input", nargs="*", help="The input folder(s) that contain a 'CIs.tex' file, for the same parameter space.", required=True)
args = parser.parse_args()
names = eval(args.names)
input = args.input

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
    med = median(d[names[i]])
    print(f"list of areas of {names[i]}: {d[names[i]]}")
    print(f"median area of {names[i]}: {med}")
    folder = d[names[i]].index(med)
    print(f"folder: {input[folder]}")
    print()
