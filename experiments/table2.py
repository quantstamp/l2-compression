import os
import json
import collections

data_path = "./data/batches/"
results_path = "./results"
plot_path="{}/plots".format(results_path)
batch_stats_path = "{}/batch_stats".format(results_path)
files = os.listdir(data_path)


def read_batch(fp):
    with open(fp, 'r') as f:
        data = json.load(f)
    return data["txs"]

def count_longest_zero_run(string):
    longest_run = 0
    current_run = 0 
    for char in string:
        if char == '0':
            current_run += 1
            if current_run > longest_run:
                longest_run = current_run
        else:
            current_run = 0

    return longest_run

counts = []
counter = 0
total = len(files)
for fp in files:
    counter +=1
    fp = data_path + fp
    batch = read_batch(fp)
    for tx in batch:
        counts.append(count_longest_zero_run(tx["raw"]))
    print(counter, total)
x = sorted(counts)
c = collections.Counter(x)
final = sorted(c.items())

# save final to file
with open('./results/longest_zero_run.csv', 'w') as f:
    for item in final:
        f.write("{},{}\n".format(item[0], item[1]))


