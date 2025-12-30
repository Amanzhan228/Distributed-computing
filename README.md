# RPC System – Distributed Computing Lab

## Overview

This project is a simple Remote Procedure Call (RPC) system created for a Distributed Computing laboratory work.  
A client can call functions that are executed on a remote server using TCP sockets and JSON messages.

---

## Architecture

- Client and Server run on different machines
- Communication uses TCP on port 6000
- Data is exchanged in JSON format
- Deployed on AWS EC2 instances

Client ---> TCP / JSON ---> Server

---

## Remote Functions

The server provides the following RPC functions:

- server_time() – returns the current server time  
- sum_values(a, b) – returns the sum of two numbers  
- invert_text(text) – reverses the given string  

---

## Reliability

The client supports:
- Connection timeout
- Up to 3 retry attempts
- Exponential backoff
- Handling of network failures (for example, blocked port)

The system automatically recovers after the connection is restored.

---

## How to Run

### Start the server
```bash
python3 server.py
```

### Run the client

Get server time:
```bash
python3 client.py --server <SERVER_IP> --function server_time
```

Sum two values:
```bash
python3 client.py --server <SERVER_IP> --function sum_values --param1 15 --param2 25
```

Invert text:
```bash
python3 client.py --server <SERVER_IP> --function invert_text --param1 "distributed"
```

---

## Firewall Test (Server Side)

```bash
sudo ufw deny 6000
sudo ufw allow 6000
```

Used to simulate network failure and recovery.

---

## Technologies Used

- Python 3
- TCP Sockets
- JSON
- AWS EC2
- Linux (UFW)

---

## Summary

This project demonstrates:
- Remote procedure calls
- Client-server communication
- Data serialization
- Network failure handling
- Distributed system deployment
