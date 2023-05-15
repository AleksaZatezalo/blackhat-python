from ctypes import *
import socket
import struct

# hodst to listen on
HOST = '127.0.0.1'

class IP(Structure):
	_fields_ = [
		("version", c_ubyte, 4) # 4 bit unsigned chart
		("ihl", c_ubyte, 4) # 4 bit unsigned chart
		("tos", c_ubyte, 8) # 1 byte unsigned chart
		("len", c_ubyte, 16) # 2 byte unsigned chart
		("offset", c_ubyte, 16) # 2 byte unsigned chart
		("id", c_ubyte, 16) # 2 byte unsigned chart
		("ttl", c_ubyte, 8) # 1 byte unsigned chart
		("protocol_num", c_ubyte, 8) # 1 byte unsigned chart
		("sum", c_ubyte, 16) # 2 byte unsigned chart
		("src", c_ubyte, 32) # 4 byte unsigned chart
		("dst", c_ubyte, 32) # 4 byte unsigned chart
		]
	
	def __new__(cls, socket_buffer=None):
		return cls.from_buffer_copy(socket_buffer)
		
	def __init__(self, socket_buffer=None):
		self.src_address = socket.inet_ntoa(struct.pacl("<L", self.src))
		self.dst_address = socket.inet_ntoa(struct.pacl("<L", self.dst))
