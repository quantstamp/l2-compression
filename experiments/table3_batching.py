import csv
import matplotlib.pyplot as plt

results_path = "./results"
plot_path="{}/plots".format(results_path)

with open('./results/zero_runs.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

x = [int(item[0]) for item in data]
y = [int(item[1]) for item in data]
print(y)

bucket_ranges = [0, 2, 5, 25, 50, 75, 100, 150, 200, 500, 1000, 10000]

bucket_counts = [0] * (len(bucket_ranges) - 1)

for i in range(len(bucket_ranges) - 1):
    for j,k in zip(x, y):
        if bucket_ranges[i] <= j < bucket_ranges[i + 1]:
            bucket_counts[i] += k

print(bucket_counts)

# bucket_counts = [sum(value for value in y if bucket_ranges[i] <= value < bucket_ranges[i + 1]) for i in range(len(bucket_ranges) - 1)]

bucket_labels = [f'[{bucket_ranges[i]}-{bucket_ranges[i + 1]})' for i in range(len(bucket_ranges) - 1)]
with open('./results/zero_runs_buckets.csv', 'w') as f:
    for range, item in zip(bucket_labels, bucket_counts):
        f.write("{},{}\n".format(range, item))

plt.bar(bucket_labels, bucket_counts, align='edge')

plt.xlabel('Total Number of Zero Runs')
plt.ylabel('Count')
plt.title('Zero Runs Distribution')
plt.xticks(rotation = 50)
plt.savefig("{}/zero_runs.png".format(plot_path), bbox_inches = "tight")
plt.close()
