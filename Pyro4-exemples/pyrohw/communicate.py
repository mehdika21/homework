import Pyro4
import time
from Pyro4 import naming
from multiprocessing import Process
from test import num_processes


table = [0]*num_processes


@Pyro4.expose
class Something:
    def __init__(self, pid, num_processes):
        # self.ns_process = None
        self.pid = pid
        self.vector_clock = [0] * num_processes

    # def start_nameserver(self, host, port):
    #     self.ns_process = Process(target=start_nameserver, args=(host, port))
    #     self.ns_process.start()
    def local_event(self):
        global table
        self.vector_clock[self.pid] += 1
        table[self.pid]+=1
        print(f"Process {self.pid+1}: Local event occurred. Vector clock: {table}")
        # print(f"table: {table}")


    def send_event(self, receiver_pid, message=None):
        global table
        table[self.pid] += 1
        self.vector_clock[self.pid] += 1
        table[receiver_pid] += 1
        print(f"Process {self.pid+1}: Sending event to Process {receiver_pid+1}. Vector clock: {table}")
        receiver = Pyro4.Proxy(f"PYRONAME:process.{receiver_pid}@localhost:{9090+receiver_pid}")
        receiver.receive_event(self.pid, self.vector_clock, message)


    def receive_event(self, sender_pid, sender_vector_clock, message=None):
        global table

        for i in range(len(self.vector_clock)):
            self.vector_clock[i] = max(self.vector_clock[i], sender_vector_clock[i])
            table[i] = max(self.vector_clock[i], sender_vector_clock[i])

        # print(f"table: {table}")
        print(f"Process {self.pid+1}: Received event from Process {sender_pid+1}. Vector clock: {table}")
        if message:
            print(f"Message: {message}")


def server_thread(process, host, port):
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS(host=host, port=port)
    uri = daemon.register(process)
    ns.register(f"process.{process.pid}", uri)
    print(f"Process {process.pid+1} is ready.")
    daemon.requestLoop()


if __name__ == "__main__":
    base_port = 9090
    somethings = []
    processes = []
    for i in range(num_processes):
        port = base_port + i
        process = Something(i, num_processes)
        somethings.append(process)
        p = Process(target=server_thread, args=(process, "localhost", port))
        p.start()
        processes.append(p)

    time.sleep(3)
    somethings[0].local_event()
    somethings[0].send_event(1, message="Hello from Process 0 to Process 1")
    somethings[1].local_event()
    somethings[2].local_event()
    somethings[2].send_event(0, message="Hello from Process 2 to Process 0")
    somethings[3].local_event()
    somethings[2].send_event(1, message="Hello from Process 2 to Process 1")
    somethings[1].local_event()
