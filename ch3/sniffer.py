"""
Author: Aleksa Zatezalo
Date: May 15th 2023
Description: The begginings of a sniffer in python.
"""

from ctypes import *
import struct
import socket
import os


def main():
	# create raw socket, bin to public interface
	if os.name == 'nt':
		socket_protocol = socket.IPPROTO_IP
	else:
		socket_protocol = socket.IPPROTO_ICMP
	
	sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocal)
	sniffer.bind(HOST,0)
	# include the IP header in capture
	sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,1)
	
