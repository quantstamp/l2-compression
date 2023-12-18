import json
import requests
import multiprocessing

provider_url = "https://eth-mainnet.g.alchemy.com/v2/aYS28CZ9Ro8olOAlAE04iYYuWOYi6HYq"


def get_tx_by_hash(hash: str):
    return requests.post(provider_url, json={
        "id": 0,
        "jsonrpc": "2.0",
        "method": "eth_getTransactionByHash",
        "params": [hash]
    }).json()


with open("./optimism_batches_log.json", "r") as f:
    tx_hashes = json.load(f)["transaction_hashes"]


def process_tx_hash(task_queue):
    while not task_queue.empty():
        hash = task_queue.get()
        tx = get_tx_by_hash(hash)
        if not tx.get("result"):
            print("error")
            continue
        with open(f"./data/raw_batches/{int(tx['result']['blockNumber'], 0)}_{tx['result']['hash']}.json", "w+") as f:
            json.dump(tx["result"], f, indent=2)
    return True


def run():
    task_queue = multiprocessing.Queue()
    for hash in tx_hashes:
        task_queue.put(hash)
    processes = []
    for _ in range(5):
        p = multiprocessing.Process(target=process_tx_hash, args=(task_queue,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()


if __name__ == "__main__":
    run()
