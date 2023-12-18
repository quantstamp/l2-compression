import os
import json
files = os.listdir('./data/raw_batches')

file_paths = []
folder_path = "/Users/roshan/QuantStamp/zkr-compression-research"
for file in files:
    x = ["", ""]
    x[0] = folder_path + "/data/raw_batches/" + file
    x[1] = folder_path + "/data/batches/" + file
    file_paths.append(x)

with open('optimism_decoder/fps.json', 'w') as f:
    json.dump(file_paths, f, indent=2)
