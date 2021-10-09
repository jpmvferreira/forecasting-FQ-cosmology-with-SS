#!/usr/bin/env python3

# imports
from getdist import plots, MCSamples
from random import gauss, uniform
import matplotlib.pyplot as plt
import numpy as np
import argparse
import getdist
import pandas
import stan
import yaml


# main
def main(model, data, samples, output, chains, warmup):
    # get model from the .stan file
    with open(model, "r") as file:
        program = file.read()

    # get relevant parameters from .yml file with the same name
    yml = model.replace(".stan", ".yml")
    with open(yml, "r") as file:
        d = yaml.full_load(file)
        ndim = d["ndim"]
        names = d["names"]
        labels = d["labels"]
        initial = d["initial"]
        markers = d["markers"]

    # get initial conditions obtained from the previous .yml file
    init = []
    for i in range(0, chains):
        init.append({})
        for name in names:
            init[i][name] = eval(initial[name])

    # get data from the .csv file
    csv = pandas.read_csv(data, comment="#")
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
        ax.set_xlim(0, samples+warmup)
        ax.set_ylabel("$" + labels[i] + "$")
        ax.axvline(x=warmup, linestyle="--", color="red")
        ax.yaxis.set_label_coords(-0.1, 0.5)
        ax.grid()
    axes[-1].set_xlabel("step number")
    plt.show()

    # show the corner plot (fix me!)
    samples = np.column_stack((fit["mu"][0][chains*warmup:], fit["sigma"][0][chains*warmup:]))
    mcsamples = MCSamples(samples=samples, names = names, labels = labels)
    g = plots.get_subplot_plotter()
    g.triangle_plot(mcsamples, filled=True, markers=markers)
    plt.show()

    return


# run if called
if __name__ == "__main__":
    # create argparser
    parser = argparse.ArgumentParser(description = "A Python command line interface (CLI) that aims to simply the usage of MCMC methods on different models, with different datasets.")

    # argparser arguments
    parser.add_argument("-m", "--model", type=str, help="The input .stan model file. Required.", required=True)
    parser.add_argument("-d", "--data", type=str, help="Input data from one (or more) .csv file(s). Required.", required=True)
    parser.add_argument("-s", "--samples", type=int, help="The number of steps to produce in each chain. Required.", required=True)
    parser.add_argument("-o", "--output", type=str, help="Output folder. Required if -n or --noshow flag is set. Warning: will overwrite existing files.", default="")
    parser.add_argument("-c", "--chains", type=int, help="The number of chains to run in parallel. Default is 1.", default=1)
    parser.add_argument("-w", "--warmup", type=int, help="The number of steps to warmup each chain. Default is 20.", default=20)

    # get arguments
    args = parser.parse_args()
    model = args.model
    data = args.data
    samples = args.samples
    output = args.output
    chains = args.chains
    warmup = args.warmup

    main(model, data, samples, output, chains, warmup)
