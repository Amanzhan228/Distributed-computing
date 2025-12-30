RPC System - Distributed Computing Lab

This project is a simple Remote Procedure Call (RPC) system made for a Distributed Computing lab.

The project consists of two parts:
- Server
- Client

The client connects to the server using TCP sockets and sends requests in JSON format.
The server processes the request and sends back a JSON response.

Server and client run on different machines.
Communication is done on TCP port 6000.
The project is deployed on AWS EC2.

RPC functions available on the server:
- server_time() : returns current server time
- sum_values(a, b) : returns the sum of two numbers
- invert_text(text) : reverses the given string

The client includes basic fault handling:
- connection timeout
- retry up to 3 times
- exponential backoff
- handling network errors such as blocked port

How to run the project:

Start the server:
python3 server.py

Run the client:
python3 client.py --server <SERVER_IP> --function server_time
python3 client.py --server <SERVER_IP> --function sum_values --param1 15 --param2 25
python3 client.py --server <SERVER_IP> --function invert_text --param1 "distributed"

Firewall test on server:
sudo ufw deny 6000
sudo ufw allow 6000

Technologies used:
Python 3
TCP sockets
JSON
AWS EC2
Linux (UFW)

This project demonstrates basic client-server communication,
remote procedure calls, and simple network failure handling.
