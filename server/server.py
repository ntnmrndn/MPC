#!/usr/bin/python

import argparse
import socket
import select

#Arguments
parser = argparse.ArgumentParser(description='A simple chat server.')
parser.add_argument('port', metavar='p', type=int, nargs='+',
                   help='A port to listen to')
args = parser.parse_args()
print 'Will now listen for clients on port:', args.port
print 'Exit with Ctrl-C'

#Let the fun begin
class AbstractSocket:
        #XXX Abstract name ...
        def __init__(self, socket):
                self.socket = socket
        def formatMessage(self, message):
                return "[%s] : %s" % (self.name, message)

class Client(AbstractSocket):
        def read_ready(self):
                global abstractSocketHash

                raw = self.socket.recv(1024)
                print 'Received msg', raw
                if raw.startswith('NAME:'):
                        self.name = raw.split(':', 1)[1].strip()
                        print 'Client name is', self.name
                elif raw.startswith('MSG:'):
                        message = self.formatMessage(raw.split(':',1)[1])
                        for abstractSocket in abstractSocketHash.values():
                                if abstractSocket != self:
                                        abstractSocket.sendMessage(message)

        def sendMessage(self, message):
                self.socket.send(message)

class Server(AbstractSocket):
        def sendMessage(self, message):
                print 'BROADCASTING',  message

        def read_ready(self):
                self.name = '[SERVER]'
                (new_client_socket, address) = self.socket.accept()
                print 'received client from address', address
                global abstractSocketHash
                abstractSocketHash[new_client_socket] = Client(new_client_socket)   #XXX  not pretty



serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('0.0.0.0', 4242))
serversocket.listen(512)
serversocket.setblocking(0)

# (clientsocket, address) = serversocket.accept() #god python has some strange lvalues
abstractSocketHash = {serversocket : Server(serversocket)}
while 1:
        (ready_read, write_ready, errors) = select.select(abstractSocketHash.keys(), [], [], 60)
        for ready_socket in ready_read:
                abstractSocketHash[ready_socket].read_ready()
