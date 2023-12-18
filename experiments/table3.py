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

def count_zero_runs(string):
    current_run = 0 
    totals=[]
    for char in string:
        if char == '0':
            current_run += 1
        else:
            if current_run > 0:
                totals.append(current_run)
                current_run = 0

    return totals

counts = []
counter = 0
total = len(files)
for fp in files:
    counter +=1
    fp = data_path + fp
    batch = read_batch(fp)
    for tx in batch:
        counts.extend(count_zero_runs(tx["raw"]))
    print(counter, total)
x = sorted(counts)
c = collections.Counter(x)
final = sorted(c.items())

# save final to file
with open('./results/zero_runs.csv', 'w') as f:
    for item in final:
        f.write("{},{}\n".format(item[0], item[1]))
