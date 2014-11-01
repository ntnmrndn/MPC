#!/usr/local/bin/python3

import socket
import argparse
import cmd
from threading import Thread

parser = argparse.ArgumentParser(description='A simple chat server.')
parser.add_argument('host', metavar='h', type=str, nargs='?', default='127.0.0.1',
                    help='A host to connect to default: 127.0.0.1')
parser.add_argument('port', metavar='p', type=int, nargs='?', default=4242,
                    help='A port to connect to default: 4242')
parser.add_argument('name', metavar='n', type=int, nargs='?',
                    help='A user name')
args = parser.parse_args()
print('Will connect to', args.host, 'on port:', args.port)
print('Exit with Ctrl-C')

class Client(cmd.Cmd):
    def default(self, string):
        print("Sending all:", string)
        Server.instance.send_message("MSG:%s" %(string) )
    def do_change_name(self, string):
        """
        Syntax: change_name NewUserName
        Change yout name
        """
        if not string:
            print ("Syntax: name NewUserName")
        else:
            print("Changing name to", string)
            Server.instance.send_message("NAME:%s" %(string) )

    def do_whisper(self, string):
        """
        Syntax: whisper Username Message
        Send a private message to user
        """
        args = string.split(' ', 1)
        if not args[0] or not args[1]:
            print ("Syntax: whisper Username Message")
        else:
            print("Whispering to", args[0] , "with message", args[1])
            Server.instance.send_message("PRIV:%s:%s" %(args[0], args[1]))


class Server():
    instance = None
    runner = None
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        Server.instance = self
        self.runner = Thread(target = self.run)
        self.runner.start()
        #self.runner.join()

    def run(self):
        while 1:
            message = self.server.recv(1024).decode("utf-8")
            print(message)

    def send_message(self, string):
        self.server.send(string.encode('utf-8'))

server = Server(args.host, args.port)
Client().cmdloop("For help, type help. To send a message to all, type anything")
