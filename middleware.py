import socket
import threading
import pickle
import heapq


class middleware:
    def __init__(self, pid, ip, port, group):
        self.queue = []
        self.clock = 0
        self.pid = pid
        self.ip = ip
        self.port = port
        self.group = group
        self.inbox = []
        self.e = threading.Event()
        self.ack_sent = set()
        self.ack_recv = {}

    def _middle_recv(self, c):
        '''
            Recieve message and process it accordingly on the base of type
        '''
        data = c.recv(1024)
        data = pickle.loads(data)
        # print("Server received", data)
        self.clock = max(self.clock, int(data[1].split(".")[0]))
        self.clock += 1
        # Check the message type here. It can be of ACK, P2P or MC
        if data[0] == "P2P":
            self.inbox.append(data[2])
            self.e.set()

        if data[0] == "MC":
            # Append to queue and heapify
            clock, pid = data[1].split(".")
            self.queue.append((int(clock), int(pid), data[1], data[2]))
            heapq.heapify(self.queue)
            # Check if we have sent the ack for the new head
            # If not then send the ack
            if self.queue[0][2] not in self.ack_sent:
                self.ack_sent.add(self.queue[0][2])
                self.middle_send_ack(self.queue[0][2])

        if data[0] == "ACK":
            # Add to ACK received
            self.ack_recv[data[2]] = self.ack_recv.get(data[2], 0) + 1
            # Check if we have recevied ACK from all nodes
            # start from the top of the heap and break
            while len(self.queue):
                if self.ack_recv.get(self.queue[0][2], 0) == len(self.group):
                    # Pop from the heap and append to the inbox
                    temp = heapq.heappop(self.queue)
                    self.inbox.append(temp[3])
                    self.e.set()
                else:
                    # Check if we have sent the ack of the new head
                    # Else send the ack and break
                    if self.queue[0][2] not in self.ack_sent:
                        self.ack_sent.add(self.queue[0][2])
                        self.middle_send_ack(self.queue[0][2])
                    break

        # print("Current clock is ", self.clock, "for PID", self.pid)
        c.close()

    def get_inbox(self):
        '''
            Send the inbox to the application
        '''
        return self.inbox

    def set_event(self):
        '''
            Return True once the event has been set
        '''
        self.e.wait()
        return True

    def clear_event(self):
        '''
            Return True once the event has been cleared
        '''
        self.e.clear()
        return True

    def clear_inbox(self):
        '''
            Clear the inbox after read by the application
        '''
        self.inbox = []
        return True

    def middle_send_p2p(self, msg, dest):
        '''
            Send message to given destination
            Destinatiion is a tuple of IP and Port
        '''
        self.clock += 1
        s = socket.socket()
        s.connect((dest[0], dest[1]))
        final_msg = ("P2P", str(self.clock)+"."+str(self.pid), msg)
        # print("Sending data", final_msg)
        data = pickle.dumps(final_msg)
        s.send(data)
        s.close()

    def middle_send_mc(self, msg):
        '''
            Send the message to all the nodes
            Along with clock and PID
        '''
        self.clock += 1
        issue_clock = self.clock
        for n in self.group:
            s = socket.socket()
            s.connect((n["ip"], n["port"]))
            final_msg = ("MC", str(issue_clock)+"."+str(self.pid), msg)
            # print("Sending data", final_msg, "to", n["port"])
            data = pickle.dumps(final_msg)
            s.send(data)
            s.close()

    def middle_send_ack(self, msg_id):
        '''
            Send message to given destination
            Destinatiion is a tuple of IP and Port
        '''
        self.clock += 1
        for n in self.group:
            s = socket.socket()
            s.connect((n["ip"], n["port"]))
            final_msg = ("ACK", str(self.clock)+"."+str(self.pid), msg_id)
            data = pickle.dumps(final_msg)
            s.send(data)
            s.close()

    def _start_server(self):
        '''
            Start the TCP server
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(5)

        while True:
            c, addr = s.accept()
            t = threading.Thread(target=self._middle_recv, args=(c,))
            t.start()

        s.close()
        return 1

    def start_middleware(self):
        '''
            Start the middleware on the give IP and Port
        '''
        server = threading.Thread(target=self._start_server)
        server.start()
        return 1
