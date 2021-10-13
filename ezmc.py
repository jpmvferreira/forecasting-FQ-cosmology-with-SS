#!/usr/bin/env python3

# imports
from getdist import plots, MCSamples
from random import gauss, uniform
import matplotlib.pyplot as plt
import numpy as np
import arviz as az
import argparse
import getdist
import pandas
import stan
import yaml
import os


def load(yml, names, labels, initial, markers, samples, warmup, chains):
    # get raw configuration data and overwrite if provided by CLI
    with open(yml, "r") as file:
        yml_loaded = yaml.full_load(file)

        if names:
            names = eval(names)
        else:
            names = yml_loaded["names"]

        if labels:
            labels = eval(labels)
        else:
            labels = yml_loaded["labels"]

        if initial:
            initial = eval(initial)
        else:
            initial = yml_loaded["initial"]

        if markers:
            markers = eval(markers)
        else:
            markers = yml_loaded["markers"]

        if not samples:
            samples = yml_loaded["samples"]

        if not warmup:
            warmup = yml_loaded["warmup"]

        if not chains:
            chains = yml_loaded["chains"]

    # run checks on sizes
    if not ( len(names) == len(labels) == len(initial) ):
        raise Exception(f"number of dimensions missmatch: len(names) = {len(names)}, len(labels) = {len(labels)}, len(initial) = {len(initial)}")

    # turn initial conditions into a dictionary
    init = []
    for i in range(0, chains):
        init.append({})
        for name in names:
            init[i][name] = eval(initial[name])

    # check if everything is provided
    if not names:
        raise Exception("Parameters names must be provided either in CLI or configuration file")
    if not labels:
        labels = names
    if not initial:
        raise Exception("Initial confitions must be provided either in CLI or configuration file")
    if not samples:
        raise Exception("The number of steps to sample the posterior distribution, after the warmup, must be provided either in CLI or configuration file")
    if not warmup:
        raise Exception("The number of steps to warmup each chain must be provided either in CLI or configuration file")
    if not chains:
        chains = 1

    return names, labels, init, markers, samples, warmup, chains


# main
def main(model, data, yml, names, labels, initial, markers, samples, warmup, chains, output, savechain, gzip, lsf, thin, noshow):
    # prepare the output folder
    if output != None and output[-1] != "/":
        output += "/"
        os.system(f"mkdir {output}")

    # get the statistical model from the provided .stan file
    with open(model, "r") as file:
        program = file.read()

    # get the configutation from the provided .yml file and/or CLI
    names, labels, initial, markers, samples, warmup, chains = load(yml, names, labels, initial, markers, samples, warmup, chains)

    # get the data from the provided .csv file(s)
    dic = {}
    aux = {0: None}
    i = 0
    for file in data:
        header = pandas.read_csv(file, comment="#", nrows=0).columns.tolist()
        columns = pandas.read_csv(file, comment="#")

        stack = False
        for j in range(0, i+1):
            if header == aux[j]:
                stack = True
                break

        if stack:
            dic[f"N{j}"] = dic[f"N{j}"] + len(columns[header[0]])
        else:
            i += 1
            aux[i] = header
            dic[f"N{i}"] = len(columns[header[0]])

        for var in header:
            if var not in dic.keys():
                dic[var] = np.array(columns[var])
            else:
                dic[var] = np.append(dic[var], np.array(columns[var]))

    # run the sampler
    posterior = stan.build(program, data=dic)
    fit = posterior.sample(num_chains=chains, num_samples=samples, num_warmup=warmup, init=initial, save_warmup=True)

    # print summary of the sample (to-do: meter percetivel e a verificar convergencia)
    #summary = az.summary(fit)
    #print(summary)

    # save the chain
    if savechain:
        dummie = 1
        # to-do (hdf5, gzip, lsf, thin)

    # plot the time series
    fig, axes = plt.subplots(len(names), figsize=(10, 7), sharex=True)
    steps = np.arange(samples+warmup)
    for i in range(len(names)):
        ax = axes[i]
        for j in range(0, chains):
            ax.plot(steps, fit[names[i]][0][j::chains], alpha=0.75)
        ax.set_xlim(0, samples+warmup)
        ax.set_ylabel("$" + labels[i] + "$")
        ax.axvline(x=warmup, linestyle="--", color="black", alpha=0.5)
        ax.axhline(y=markers[names[i]], linestyle="--", color="black", alpha=0.5)
        ax.yaxis.set_label_coords(-0.1, 0.5)
        ax.grid()
    axes[-1].set_xlabel("step number")
    if output:
        plt.savefig(output + "time-series.png")
    if not noshow:
        plt.show()
    plt.close()

    # plot the corner plot
    samples = fit[names[0]][0][chains*warmup:]
    for i in range(1, len(names)):
        samples = np.column_stack((samples, fit[names[i]][0][chains*warmup:]))
    mcsamples = MCSamples(samples=samples, names=names, labels=labels)
    g = plots.get_subplot_plotter()
    g.triangle_plot(mcsamples, filled=True, markers=markers)
    if output:
        plt.savefig(output + "corner.png")
    if not noshow:
        plt.show()
    plt.close()

    # print 1 and 2 sigma regions in a LaTex table
    if output:
        with open(output + "1sigma.tex", "w") as file:
            file.write(mcsamples.getTable(limit=1).tableTex())
        with open(output + "2sigma.tex", "w") as file:
            file.write(mcsamples.getTable().tableTex())
    if not noshow:
        print(mcsamples.getTable(limit=1).tableTex())
        print(mcsamples.getTable().tableTex())

    return


# run if called
if __name__ == "__main__":
    # create argparser
    parser = argparse.ArgumentParser(description = "A Python command line interface (CLI) that wraps the Stan programming language to simply Bayesian statistical inference with MCMC sampling.")

    # disable default help
    parser = argparse.ArgumentParser(add_help=False)

    # create argparser subgroups
    parser._action_groups.pop()
    required = parser.add_argument_group("Required arguments")
    config = parser.add_argument_group("Configuration options")
    output = parser.add_argument_group("Output arguments")
    help = parser.add_argument_group("Help dialog")

    # required arguments
    required.add_argument("-m", "--model", type=str, help="Input .stan statistical model.", required=True)
    required.add_argument("-d", "--data", nargs="*", help="Input data from one (or more) .csv file(s).", required=True)

    # configuration options
    config.add_argument("-y", "--yml", type=str, help="Input .yml configuration file. Configures the program behavior in a file with a user friendly syntax. All of the other flags in this section will either add to or overwrite the contents writen in this file.")
    config.add_argument("--names", type=str, help="String with a Python like list with the names for each parameter. Must match the names defined in the .stan model file!")
    config.add_argument("--labels", type=str, help="A string with a Python like list with the labels for each parameter.")
    config.add_argument("-i", "--initial", type=str, help="String with a Python style dictionary with the initial condition for each parameter, for each chain.") # to-do: problema do eval
    config.add_argument("--markers", type=str, help="String with a Python style dictionary with the line markers to show rendered in the plots.")
    config.add_argument("-s", "--samples", type=int, help="Number of steps to sample the posterior distribution, after the warmup.")
    config.add_argument("-w", "--warmup", type=int, help="Number of steps to warmup each chain.")
    config.add_argument("-c", "--chains", type=int, help="Number of chains to run. Will run in parallel, provided that there are enough threads to do so.")

    # output the results (to-do: implementar)
    output.add_argument("-o", "--output", type=str, help="Output folder to save the results. Warning: will overwrite existing files.")
    output.add_argument("-sc", "--savechain", action="store_true", help="Saves the chain to a .hd5 file in the output folder.")
    output.add_argument("-g", "--gzip", type=int, help="Compress the chain with GZIP. Optionally specify the compression level with an integer from 0 (fast) to 9 (slow). Default is 4.")
    output.add_argument("-l", "--lsf", action="store_true", help="Compress the chain with LSF.")
    output.add_argument("-t", "--thin", type=int, help="A positive integer specifying the period for saving samples. The default is 1, which is usually the recommended value, unless your posterior takes too much memory.")
    output.add_argument("-n", "--noshow", action="store_true", help="Don't show plots in the screen.")

    # add help to its own subsection
    help.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help="Show this help message and exit")

    # get arguments
    args = parser.parse_args()
    model = args.model
    data = args.data
    yml = args.yml
    names = args.names
    labels = args.labels
    initial = args.initial
    markers = args.markers
    samples = args.samples
    warmup = args.warmup
    chains = args.chains
    output = args.output
    savechain = args.savechain
    gzip = args.gzip
    lsf = args.lsf
    thin = args.thin
    noshow = args.noshow

    # check if output is provided if noshow is toggled
    if noshow and not output:
        raise Exception("Toggling -n, --noshow requires to provide an output folder, otherwise output will not be shown nor saved.")

    # call main with the provided arguments
    main(model, data, yml, names, labels, initial, markers, samples, warmup, chains, output, savechain, gzip, lsf, thin, noshow)
