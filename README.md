# Total Order Mutlicast

Requirements:
Python 3.6.5

Steps to Run:

1. python3 tester.py config.json

Intially the tester will start all the nodes and their middleware.
It will then send few multicast messages from each node to the network nodes.
It will also send few peer to peer messages to the next node in the ring. 
After recieving messages it prints the application layer's inbox on STDOUT.

More details about the implementation can be found in /report/report.pdf
