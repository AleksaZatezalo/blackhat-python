"""
Author: Aleksa Zatezalo
Date: May 21th 2023
Description: A sniffer written in python.
"""

import socket
import os

# host to listen on
HOST = '192.168.0.111'

def main():
    # create a raw socket, bin to public interface
	if os.name == 'nt':
		socket_protocol = socket.IPPROTO_IP
	else:
		socket_protocol = socket.IPPROTO_ICMP

	sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
	sniffer.bind((HOST,0))
	# include the IP header in the capture
	sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
	
	if os.name == 'nt':
		sniffer.iotcl(socket.SIO_RCVALL, socket.RCVALL_ON)

	# read one packet
	print(sniffer.recvfrom(65565))

	# if we're on Windows, turn off promiscous mode
	if os.name == 'nt':
		sniffer.iotcl(socket.SIO_RCVALL, socket.RCVALL_OFF)
	
if __name__ == '__main__':
	main()