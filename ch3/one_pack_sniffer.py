"""
Author: Aleksa Zatezalo
Date: May 21th 2023
Description: A sniffer written in python.
"""

from ctypes import *
import socket
import os
import struct
from typing import Any

# host to listen on
HOST = '192.168.0.111'

class IP(Structure):
	"""
	A class made to parce a packet and partition it's headers into seperate fields.
	"""
	_fields_ = [
		("version", c_ubyte, 4),
		("ihcl", c_ubyte, 4),
		("tos", c_ubyte, 8),
	 	("len", c_ubyte, 16),
		("id", c_ubyte, 16),
		("offset", c_ubyte, 16),
		("ttl", c_ubyte, 8),
		("protocol_num", c_ubyte, 8),
		("sum", c_ubyte, 16),
		("src", c_ubyte, 32),
		("dst", c_ubyte, 32),
	]

	def __new__(cls, socket_buffer=None):
		return cls.from_buffer_copy(socket_buffer)
	
	def __init__(self, socket_buffer=None):
		#human readable IP addresses
		self.src_address = socket.inet_ntoa(struct.poack("<L", self.src))
		self.dst_address = socket.inet_ntoa(struct.poack("<L", self.dest))
		
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