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
    # user defined parameters
    chains = 2
    warmup = 1000
    samples = 10000

    # get relevant parameters from .yml file
    with open("model/gaussian.yml", "r") as file:
        d = yaml.full_load(file)
        ndim = d["ndim"]
        names = d["names"]
        labels = d["labels"]
        initial = d["initial"]

    # get initial conditions specified in the .yml file
    init = []
    for i in range(0, chains):
        init.append({})
        for name in names:
            init[i][name] = eval(initial[name])

    # get model from the .stan file
    with open("model/gaussian.stan", "r") as file:
        program = file.read()

    # get data from .csv file
    csv = pandas.read_csv("data/gaussian.csv", comment="#")
    values = list(csv["value"])
    data = {"n": len(values), "y": values}

    # run the sampler
    posterior = stan.build(program, data=data)
    fit = posterior.sample(num_chains=chains, num_samples=samples, num_warmup=warmup, init=init, save_warmup=True)

    # plot the time series
    fig, axes = plt.subplots(ndim, figsize=(10, 7), sharex=True)
    steps = np.arange(samples+warmup)
    for i in range(ndim):
        ax = axes[i]
        for j in range(0, chains):
            ax.plot(steps, fit[names[i]][0][j::chains], alpha=0.75)
        ax.set_xlim(0, samples)
        ax.set_ylabel(labels[i])
        ax.axvline(x=warmup, linestyle="--", color="red")
        ax.yaxis.set_label_coords(-0.1, 0.5)
        ax.grid()
    axes[-1].set_xlabel("step number")
    plt.show()

    # show the corner plot
    print(len(fit["sigma"][0][chains*warmup:]))
    samples = np.column_stack((fit["mu"][0][chains*warmup:], fit["sigma"][0][chains*warmup:]))
    mcsamples = MCSamples(samples=samples, names = ["mu", "sigma"], labels = ["\mu", "\sigma"])
    g = plots.get_subplot_plotter()
    g.triangle_plot(mcsamples, filled=True, markers={"mu": 2, "sigma": 3})
    plt.show()

    return

# run if called
if __name__ == "__main__":
    main()
