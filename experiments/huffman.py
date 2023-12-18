import os
import json
import collections
import batch_compression as BatchCompress
import compression_algorithms as ca
import gas_cost

path = "./data/batches/"
files = os.listdir(path)


def read_batch(fp):
    with open(fp, 'r') as f:
        data = json.load(f)
    return data["txs"]


collector = collections.Counter()
x = 0

# for fp in files[0:100]:
#     batch = read_batch(path + fp)
#     batch_str = ""
#     for tx in batch:
#         trimmed_tx = tx["raw"][2:]
#         batch_str += trimmed_tx

#     batch_str, _, _ = BatchCompress.whole(batch, ca.compress_with_zstd)
#     bytesx = []
#     for i in range(0, len(batch_str), 2):
#         char_2 = batch_str[i:i+2]
#         bytesx.append(char_2)
#         x += 1
#     collector += collections.Counter(bytesx)

# print(collector)
# print(x)
# print(len(collector))

batch = read_batch(path + files[2])
batch_str = ""
for tx in batch:
    trimmed_tx = tx["raw"][2:]
    batch_str += trimmed_tx
batch_cmp, _, _ = BatchCompress.whole(batch, ca.compress_with_zstd)

bytesx = []
x = 0
for i in range(0, len(batch_cmp), 2):
    char_2 = batch_cmp[i:i+2]
    bytesx.append(char_2)
    x+=1
print(collections.Counter(bytesx))
print(x)
print(gas_cost.compute_gas_cost(batch_cmp))
# print(batch)
bin_str = bin(int(batch_cmp, base=16))[2:] + "00000000"


result = []

i = 0
max_zeros = 0
num_64 = 0
num_zero_runs = 0
while i < len(bin_str)-8:
    num_zeros = 0
    # rem = bin_str[i:]
    # for x in rem:
    #     if x == "0":
    #         num_zeros+=1
    #     else:
    #         break
    # if num_zeros > 2:
    #     result.append("00000000")
    #     num_zero_runs += 1
    #     i+=num_zeros
    #     max_zeros = max(num_zeros, max_zeros)
    if bin_str[i:i+2] == "00":
        result.append("00000000")
        i+=2
    elif bin_str[i] == "0":
        ret = bin_str[i:i+8]
        if ret == "01000000":
            result.append("00000001")
            num_64 += 1
            i+=8
        else:
            ret = bin_str[i+1:i+9]
            # print(bin((int(bin_str[i+1:i+9], 2) << 1) & 0x7f)[2:])
            result.append(ret)
            i+=9
    else:
        ret = bin_str[i:i+8]
        result.append(ret)
        i+=8

for r in result:
    if r == "00001111":
        print(r)
fin = "".join(result)
fin = hex(int(fin, 2))[2:]

bytesx = []
x = 0
for i in range(0, len(fin), 2):
    char_2 = fin[i:i+2]
    bytesx.append(char_2)
    x+=1
collector = collections.Counter(bytesx)
print(collector)
print(x)
print(gas_cost.compute_gas_cost(fin))
# print(max_zeros)
# print(num_64)
# print(num_zero_runs)