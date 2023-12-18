import gas_cost as gc


def whole(batch, compress):
    batch_str = ""
    raw_size = 0
    raw_gas_cost = 0
    for tx in batch:
        trimmed_tx = tx["raw"][2:]
        batch_str += trimmed_tx
        raw_size += len(trimmed_tx)
        raw_gas_cost += gc.compute_gas_cost(trimmed_tx)

    return compress(batch_str), raw_size, raw_gas_cost

def by_tx(batch, compress):
    compressed_txs = []
    raw_size = 0
    raw_gas_cost = 0
    for tx in batch:
        trimmed_tx = tx["raw"][2:]
        compressed_txs.append(trimmed_tx)
        raw_size += len(tx["raw"])
        raw_gas_cost += gc.compute_gas_cost(trimmed_tx)

    batch_str = ''.join(compressed_txs)
    return compress(batch_str), raw_size, raw_gas_cost
