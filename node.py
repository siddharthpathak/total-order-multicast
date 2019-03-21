import socket
import pickle
import middleware
import time
import threading


class node:

    start = False

    def __init__(self, pid, ip, port, group):
        self.pid = pid
        self.m = middleware.middleware(pid, ip, port, group)
        self.group = group

    def start_node(self):
        self.m.start_middleware()
        self.start_recv()

    def test(self):
        '''
            Sends a p2p message to each member in the group
        '''
        # for n in self.group:
        #    self.m.middle_send_p2p(["hi", 2, 3], (n["ip"], n["port"]))
        print("waiting..")
        while True:
            if node.start:
                print("Sending..", "hi "+str(self.pid))
                self.m.middle_send_mc("hi "+str(self.pid))
                break

    def start_recv(self):
        local_inbox = []
        while True:
            if self.m.set_event():
                inbox = self.m.get_inbox()
                for msg in inbox:
                    print("Process ", self.pid, "Read message", msg)
                    local_inbox.append(msg)
                self.m.clear_event()
                self.m.clear_inbox()
            print(local_inbox)
