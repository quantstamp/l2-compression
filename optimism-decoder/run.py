import json
import multiprocessing
import subprocess

with open('fps.json') as json_file:
    data = json.load(json_file)

for x in data:
    subprocess.run(["yarn", "start", x[0], x[1]])

# def process_tx_hash(task_queue):
#     while not task_queue.empty():
#         hash = task_queue.get()
#         subprocess.run(["yarn", "start", hash[0], hash[1]])
        
#     return True

# def run():
#     task_queue = multiprocessing.Queue()
#     for hash in data:
#         task_queue.put(hash)
#     processes = []
#     for _ in range(5):
#         p = multiprocessing.Process(target=process_tx_hash, args=(task_queue,))
#         processes.append(p)
#         p.start()
#     for p in processes:
#         p.join()

# if __name__ == "__main__":
#     run()