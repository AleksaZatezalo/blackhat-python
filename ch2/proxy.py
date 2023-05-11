"""
Author: Aleksa Zatezalo
Date: May 11th 2023
Description: A TCP Proxy in Python.
"""

import sys
import socket
import threading

HEX_FILTER = ''.join(
    [(len(repr(chr(i)))==3) and chr(i) or '.' for i in range(256)]
)

def hexdump(src, length=16, show=True):
    if isinstance(src,bytes):
        src = src.decode()
    
    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length])

        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')

        if show:
            for line in results:
                print(line)
        else:
            return results
        
def recive_from(connection):
    buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer

def request_handel(buffer):
    # perform packer modefication
    return buffer

def response_handler(buffer):
    # perform packer modefication
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = recive_from(remote_socket)
    
    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost." %len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = recive_from(client_socket)
        if len(local_buffer):
            line = "[<==] Sending %d bytes to localhost." %len(remote_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handel(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote host.")
    
        remote_buffer = recive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." %len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break
