MPC
===
Simple Many to Many Server/Client Messaging system.

##Abstract

This is just a demo project aimed to learn python.

Server use select() to handle every connections.

Client use basic threading to handle connections and user input.


##How to

### Server

Default configuration will listen on port 4242 `python3 ./server.py` on every interfaces.

For help `$ python3 ./server.py -h`



### Client

Default configuration will connect to localhost on port 4242  `python3 ./client.py` on every interfaces.

For help `$ python3 ./client.py -h`
You can specify the port and hostname of the server.


## Features

* A lobby where eveyone can talk together
* Private Messages
* Custom user names
* Autompletion with tab for commands
* Up to 512 clients


### Lobby

To talk to everyone, simply type your message and press enter.

### Private messages

Type `whisper userName A message` to send a private message to userName

### Changing name

Type `change_name name` to change your name to  name

### Exit

`Ctrl-c`
