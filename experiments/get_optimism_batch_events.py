import requests
import json
from Cryptodome.Hash import keccak


def keccak256(data):
    hasher = keccak.new(digest_bits=256)
    hasher.update(data)
    return hasher.digest()


batch_appended_event = "TransactionBatchAppended(uint256,bytes32,uint256,uint256,bytes)"
batch_appened_event_sig = "0x" + \
    keccak256(batch_appended_event.encode("utf-8")).hex()
provider_url = "https://eth-mainnet.g.alchemy.com/v2/aYS28CZ9Ro8olOAlAE04iYYuWOYi6HYq"

first_block = 16326163
end_block = 16384047
step = 2000
transaction_hashes = []


def make_batch_logs_request(from_block: int, to_block: int):
    params = [{
        "fromBlock": hex(from_block),
        "toBlock": hex(to_block),
        "topics": [batch_appened_event_sig]
    }]

    return requests.post(provider_url, json={
        "id": 0,
        "jsonrpc": "2.0",
        "method": "eth_getLogs",
        "params": params
    }).json()


for i in range(first_block, end_block - step, step):
    from_block = i
    to_block = i + step - 1
    response = make_batch_logs_request(from_block, to_block)
    if response.get("result") is None or not len(response["result"]):
        continue

    results = response["result"]
    transaction_hashes += [result["transactionHash"] for result in results]

with open("./optimism_batches_log.json", "w+") as f:
    json.dump({
        "log_topic": batch_appened_event_sig,
        "total_batches": len(transaction_hashes),
        "from_block": first_block,
        "to_block": end_block,
        "transaction_hashes": transaction_hashes
    }, f, indent=2)
