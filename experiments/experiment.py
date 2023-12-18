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
batch_stats_path_a1 = "{}/a1_stats".format(results_path)
batch_stats_path_a2 = "{}/a2_stats".format(results_path)
files = os.listdir(data_path)


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

def run_for_algorithm(alg, approach, stats_path):
    df = pd.DataFrame(columns=('block_num', 'num_tx', 'raw_size', 'compressed_size','compression_ratio', 'gas_cost', 'compressed_gas_cost', 'gas_savings', 'algorithm'))
    idx = 0
    for fp in files:
        idx += 1
        if idx % 500 == 0:
            print(str(idx) + "/" + str(len(files)) + "for " + alg)
        block_num = fp[0:8]
        fp = data_path + fp
        batch = read_batch(fp)
        start = time.time()
        if (approach == 1):
            compressed, raw_size, raw_gas_cost = BatchCompress.by_tx(
                batch, compression_algorithms[alg])
        elif (approach == 2):
            compressed, raw_size, raw_gas_cost = BatchCompress.whole(
                batch, compression_algorithms[alg])
        else:
            print("Error - invalid option")
            sys.exit(1)
        end = time.time()
        compressed_size = len(compressed)
        compressed_gas_cost = gc.compute_gas_cost(compressed)
        batch_stats = {'block_num': block_num,
                       'raw_size': raw_size,
                       'num_tx': len(batch),
                       'compressed_size': compressed_size,
                       'compression_ratio': compressed_size/raw_size,
                       'gas_cost': raw_gas_cost,
                       'compressed_gas_cost': compressed_gas_cost,
                       'gas_savings': (raw_gas_cost - compressed_gas_cost)/raw_gas_cost,
                       'algorithm': alg,
                       'time':end-start}
        df = pd.concat([df, pd.DataFrame([batch_stats])])
    df.to_csv("{}/{}.csv".format(stats_path, alg), index=False)
    return df

results = {}
algs = compression_algorithms.keys()

if len(sys.argv) == 3:
    if sys.argv[2] == 'a1':
        print("Starting experiments for approach A1...")
        for alg in algs:
                print(alg)
                results[alg] = run_for_algorithm(alg, 1, batch_stats_path_a1)
    elif sys.argv[2] == 'a2':
        print("Starting experiments for approach A2...")
        for alg in algs:
                print(alg)
                results[alg] = run_for_algorithm(alg, 2, batch_stats_path_a2)
    else:
        print("Error - invalid option")
        sys.exit(1)
else:
    for alg in algs:
        results[alg] = pd.read_csv("{}/{}.csv".format(sys.argv[1], alg))
plot_path = "{}/plots".format(sys.argv[1])

print("Plotting compression ratio...")
compression_ratios = []
gas_savings = []

for alg in algs:
    print(alg, results[alg].compression_ratio.mean())
    compression_ratios.append(results[alg].compression_ratio.mean())

print("Plotting gas savings...")
for alg in algs:
    print(alg, results[alg].gas_savings.mean())
    gas_savings.append(results[alg].gas_savings.mean())

plt.bar(algs, compression_ratios)
plt.title('Compression Ratio by Algorithm')
plt.xlabel('Algorithm')
plt.ylabel('Ratio')
plt.savefig("{}/compression_ratio_by_algorithm.png".format(plot_path), bbox_inches="tight")
plt.close()

plt.bar(algs, gas_savings)
plt.title('Gas Savings by Algorithm')
plt.xlabel('Algorithm')
plt.ylabel('Gas Savings')
plt.savefig("{}/gas_savings_by_algorithm.png".format(plot_path), bbox_inches="tight")
plt.close()

print("Scatter plots...")


for alg in algs:
    print("...{}...".format(alg))
    fig, ax = plt.subplots()
    ax.scatter(results[alg].raw_size, results[alg].compressed_size)
    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),
        np.max([ax.get_xlim(), ax.get_ylim()]),
    ]
    ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
    ax.set_title(alg)
    plt.ylabel("Compression Size")
    plt.xlabel("Raw Size")
    plt.savefig("{}/{}.png".format(plot_path, alg), bbox_inches="tight")
    plt.close()
print("...Done.")
