#!/usr/bin/env python3

# imports
from getdist import plots, MCSamples
from random import gauss, uniform
import matplotlib.pyplot as plt
import numpy as np
import getdist
import pandas
import stan
import yaml

# main
def main():
    # get relevant parameters from .yml file
    with open("model/gaussian.yml", "r") as file:
        d = yaml.full_load(file)
        ndim = d["ndim"]
        names = d["names"]
        labels = d["labels"]
        initial = d["initial"]

    # get model from the .stan file
    with open("model/gaussian.stan", "r") as file:
        program = file.read()

    # user defined parameters
    chains = 2
    warmup = 20
    samples = 1000

    # get data from .csv file
    csv = pandas.read_csv("data/gaussian.csv", comment="#")
    values = list(csv["value"])
    data = {"n": len(values), "y": values}

    # get initial conditions
    init = []
    for i in range(0, chains):
        init.append({})
        for name in names:
            init[i][name] = eval(initial[name])

    print(init)
    # run the sampler
    posterior = stan.build(program, data=data)
    fit = posterior.sample(num_chains=chains, num_samples=samples, num_warmup=warmup, init=init)

    # plot the time series for each parameter
    fig, axes = plt.subplots(ndim, figsize=(10, 7), sharex=True)
    for i in range(ndim):
        ax = axes[i]
        ax.plot(fit[names[i]][0], "k", alpha=0.75)
        ax.set_xlim(0, samples)
        ax.set_ylabel(labels[i])
        #ax.axvline(x=warmup, linestyle="--", color="red")
        ax.yaxis.set_label_coords(-0.1, 0.5)
        ax.grid()
    axes[-1].set_xlabel("step number")
    plt.show()

    # plot the corner plot
    samples = np.column_stack((fit["mu"][0], fit["sigma"][0]))
    mcsamples = MCSamples(samples=samples, names = ["mu", "sigma"], labels = ["\mu", "\sigma"])
    g = plots.get_subplot_plotter()
    g.triangle_plot(mcsamples, filled=True, markers={"mu": 2, "sigma": 3})
    plt.show()

    return

# run if called
if __name__ == "__main__":
    main()
