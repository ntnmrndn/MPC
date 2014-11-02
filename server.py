#!/usr/local/bin/python3

import argparse
import socket
import select
import random

class AbstractSocket:
        anonymous_number = 0

        def __init__(self, socket):
                self.socket = socket
                self.name = "Anonymous%i" % (AbstractSocket.anonymous_number)
                AbstractSocket.anonymous_number += 1

        def format_message(self, message):
                return "[%s] : %s" % (self.name, message)

        def send_message(self, message):
                print('BROADCASTING',  message)

class Client(AbstractSocket):
        def __init__(self, socket):
                super().__init__(socket)
                self.changed_name()

        def read_ready(self):
                try:
                        raw = self.socket.recv(1024).decode("utf-8").strip()
                except: #XXX not pretty
                        Server.instance.disconnect(self)
                        return
                if not raw:
                        Server.instance.disconnect(self)
                if raw.startswith('NAME:'):
                        #XXX check names unicity
                        old_name = self.name
                        self.name = raw.split(':', 1)[1]
                        Server.instance.broadcast("User %s is now known as %s" %(old_name, self.name))
                        self.changed_name()
                elif raw.startswith('MSG:'):
                        message = self.format_message(raw.split(':', 1)[1])
                        Server.instance.broadcast(message)
                elif raw.startswith('PRIV:'):
                        args = raw.split(':',2)
                        to = args[1]
                        message = args[2]
                        print ("Private message from", self.name, "to", to , ":", message)
                        Server.instance.private_message(self.format_message(message), self, to)
        def send_message(self, message):
                self.socket.send(message.encode('utf-8'))
        def changed_name(self):
                self.send_message("NAME:%s" % (self.name))


class Server(AbstractSocket):
        instance = None

        def __init__(self, port):
                super().__init__(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                self.name = '[SERVER]'
                Server.instance = self
                self.socket.bind(('0.0.0.0', port))
                self.socket.listen(512)
                self.socket.setblocking(0)
                self.abstract_socket_hash = {self.socket : self}

        def broadcast(self,  message):
                for abstractSocket in self.abstract_socket_hash.values():
                        abstractSocket.send_message(message)

        def private_message(self, message, sender, receiver_name):
                for abstractSocket in self.abstract_socket_hash.values():
                        if abstractSocket.name == receiver_name:
                                abstractSocket.send_message("[PRIVATE] %s" %(message))
                                return
                sender.send_message("[SERVER]: User %s unknow" % (receiver_name))


        def disconnect(self, client):
                self.abstract_socket_hash.pop(client.socket)
                self.broadcast("[SERVER] %s disconnected" % (client.name))

        def clientList(self):
                names = "" #XXX handle no other clients
                for abstractSocket in self.abstract_socket_hash.values():
                        if abstractSocket != self:
                                names += abstractSocket.name + " "
                return names.strip()

        def read_ready(self):
                (new_client_socket, address) = self.socket.accept()
                client = Client(new_client_socket)
                self.broadcast("[SERVER] %s joined" % (client.name))
                clientList = self.clientList()
                if not clientList:
                        client.send_message("Welcome !\nYou are alone")
                else:
                        client.send_message("Welcome !\nCurrent users are: %s" %  (clientList))
                self.abstract_socket_hash[new_client_socket] = client


        def run(self):#XXX check for write readiness
                while 1:
                        (ready_read, write_ready, errors) = select.select(self.abstract_socket_hash.keys(), [], [], 60)
                        for ready_socket in ready_read:
                                self.abstract_socket_hash[ready_socket].read_ready()

#Arguments
parser = argparse.ArgumentParser(description='A simple chat server.')
parser.add_argument('port', metavar='p', type=int, nargs='?', default=4242,
                    help='A port to listen to')
args = parser.parse_args()
print('Will now listen for clients on port:', args.port)
print('Exit with Ctrl-C')
Server(args.port).run()
