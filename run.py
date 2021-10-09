#!/usr/bin/env python3

# imports
from getdist import plots, MCSamples
import matplotlib.pyplot as plt
from random import gauss, seed
import numpy as np
import getdist
import stan

# main
def main():
    # define relevant parameters
    ndim = 2
    chains = 1
    warmup = 250
    samples = 500
    names = ["mu", "sigma"]
    labels = ["$\mu$", "$\sigma$"]

    # get model
    file = open("model/gaussian.stan", "r")
    program = file.read()
    file.close()

    # get data
    n = 100
    seed(1)
    data = {"n": n, "y": [gauss(2, 3) for i in range(0, n)]}

    # get initial conditions
    # (...)

    # run the sampler
    posterior = stan.build(program, data=data)
    fit = posterior.sample(num_chains=chains, num_samples=samples, num_warmup=warmup)

    # plot the time series for each parameter
    fig, axes = plt.subplots(ndim, figsize=(10, 7), sharex=True)
    for i in range(ndim):
        ax = axes[i]
        ax.plot(fit[names[i]][0], "k", alpha=0.75)
        ax.set_xlim(0, samples)
        ax.set_ylabel(labels[i])
        ax.axvline(x=warmup, linestyle="--", color="red")
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
