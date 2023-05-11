"""
Author: Aleksa Zatezalo
Date: May 10th 2023
Description: A Basic UDP Client in Python
"""

import socket

target_host = "127.0.0.1"
target_port = 9997

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send some data
client.sendto(b"AAABBBCCC", (target_host, target_port))

# recive some data
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()