import sys
import node
import json
import time
import multiprocessing
import threading

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

time.sleep(5)

# Test case 0
# for i, c in enumerate(nodes):
#    p = threading.Thread(target=c.test)
#    p.start()
# time.sleep(5)
# node.node.start = True

# Test case 1
# for i, c in enumerate(nodes):
#    c.m.middle_send_mc("mc" + str(i))

# for i, c in enumerate(nodes):
#    c.m.middle_send_p2p("p2p" + str(i), (config[(i+1) % len(config)]["ip"], config[(i+1) % len(config)]["port"]))
#    c.m.middle_send_p2p("p2p" + str(i), (config[(i+1) % len(config)]["ip"], config[(i+1) % len(config)]["port"]))

# for i, c in enumerate(nodes):
#    c.m.middle_send_mc("mc" + str(i))

# Test case 2
for i, c in enumerate(nodes):
    c.m.middle_send_p2p("p2p" + str(i), (config[(i+1) % len(config)]["ip"], config[(i+1) % len(config)]["port"]))
    c.m.middle_send_p2p("p2p" + str(i), (config[(i+1) % len(config)]["ip"], config[(i+1) % len(config)]["port"]))
    c.m.middle_send_p2p("p2p" + str(i), (config[(i+1) % len(config)]["ip"], config[(i+1) % len(config)]["port"]))
    c.m.middle_send_p2p("p2p" + str(i), (config[(i+1) % len(config)]["ip"], config[(i+1) % len(config)]["port"]))

for i, c in enumerate(nodes):
    c.m.middle_send_mc("mc" + str(i))


for i, c in enumerate(nodes):
    c.m.middle_send_mc("mc" + str(i))