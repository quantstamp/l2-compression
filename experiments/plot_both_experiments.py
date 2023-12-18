import compression_algorithms as ca
import batch_compression as BatchCompress
import gas_cost as gc
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import time

data_path = "./data/batches/"
results_path = "./results"


def read_batch(fp):
    with open(fp, 'r') as f:
        data = json.load(f)
    return data["txs"]


compression_algorithms = {
    "zstd": ca.compress_with_zstd,
    "zlib": ca.compress_with_zlib,
    "brotli": ca.compress_with_brotli,
    "lzma": ca.compress_with_lzma,
    "bz2": ca.compress_with_bz2,
    "zle": ca.compress_with_zle,
    #"zle_with_bwt": ca.compress_with_zle_and_bwt,
    "rle": ca.compress_with_rle
    #"rle_with_bwt": ca.compress_with_rle_and_bwt
}

results_a1 = {}
results_a2 = {}
algs = compression_algorithms.keys()


for alg in algs:
    results_a1[alg] = pd.read_csv("results/{}/{}.csv".format("a1_stats", alg))
for alg in algs:
    results_a2[alg] = pd.read_csv("results/{}/{}.csv".format("a2_stats", alg))

plot_path = "results/plots"
plot_path_a1 = "results/a1_plots"
plot_path_a2 = "results/a2_plots"

print("Plotting compression ratio (combined)...")
compression_ratios_a1 = []
gas_savings_a1 = []

for alg in algs:
    print(alg, results_a1[alg].compression_ratio.mean())
    compression_ratios_a1.append(results_a1[alg].compression_ratio.mean())

compression_ratios_a2 = []
gas_savings_a2 = []

for alg in algs:
    print(alg, results_a2[alg].compression_ratio.mean())
    compression_ratios_a2.append(results_a2[alg].compression_ratio.mean())

# Define the width of the bars
bar_width = 0.35

# Create an array of positions for the bars
x = np.arange(len(algs))

# Plot the first set of bars
plt.bar(x - bar_width/2, compression_ratios_a1, bar_width, label='A1')

# Plot the second set of bars
plt.bar(x + bar_width/2, compression_ratios_a2, bar_width, label='A2')

# Customize the plot
plt.xlabel('Algorithm')
plt.ylabel('Compression Ratio')
plt.title('Comparison of Compression Ratios')
plt.xticks(x, algs)
plt.legend()

plt.savefig("{}/compression_ratio_by_algorithm_combined.png".format(plot_path), bbox_inches="tight")
plt.close()

print("Plotting gas savings (combined)...")
for alg in algs:
    print(alg, results_a1[alg].gas_savings.mean())
    gas_savings_a1.append(results_a1[alg].gas_savings.mean())

for alg in algs:
    print(alg, results_a2[alg].gas_savings.mean())
    gas_savings_a2.append(results_a2[alg].gas_savings.mean())

x = np.arange(len(algs))

# Plot the first set of bars
plt.bar(x - bar_width/2, gas_savings_a1, bar_width, label='A1')

# Plot the second set of bars
plt.bar(x + bar_width/2, gas_savings_a2, bar_width, label='A2')

# Customize the plot
plt.xlabel('Algorithm')
plt.ylabel('Gas Savings')
plt.title('Comparison of Gas Savings')
plt.xticks(x, algs)
plt.legend()

plt.savefig("{}/gas_savings_by_algorithm_combined.png".format(plot_path), bbox_inches="tight")
plt.close()

print("Scatter plots...")
for alg in algs:
    print("...{}...".format(alg))
    fig, ax = plt.subplots()
    ax.scatter(results_a1[alg].raw_size, results_a1[alg].compressed_size, label='A1', marker = 'x')
    ax.scatter(results_a2[alg].raw_size, results_a2[alg].compressed_size, label='A2', marker = 'o')

    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),
        np.max([ax.get_xlim(), ax.get_ylim()]),
    ]
    ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
    ax.set_title(alg)
    ax.legend()
    ax.legend(loc='upper left')

    plt.ylabel("Compression Size")
    plt.xlabel("Raw Size")
    plt.savefig("{}/{}.png".format(plot_path, alg), bbox_inches="tight")
    plt.close()
print("...Done.")
