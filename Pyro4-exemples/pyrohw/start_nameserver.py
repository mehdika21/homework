import sys
import Pyro4
from Pyro4 import naming
from multiprocessing import Process


def start_nameserver(host, port):
    Pyro4.naming.startNSloop(host=host, port=port)


if __name__ == "__main__":
    num_processes = int(sys.argv[1])
    starting_port = 9090
    processes = []
    for i in range(num_processes):
        port = starting_port + i
        p = Process(target=start_nameserver, args=("localhost", port,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
