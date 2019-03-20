import sys
import node
import json
import time
import multiprocessing

config_file = sys.argv[1]
config = json.load(open(config_file))
nodes = []
for i, c in enumerate(config):
    print("Starting node with ", c["ip"], c["port"])
    n = node.node(i, c["ip"], c["port"], config)
    p = multiprocessing.Process(target=n.start_node)
    p.start()
    nodes.append(n)
    print("Started node", c["ip"], c["port"], p.pid)
