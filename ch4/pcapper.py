"""
Author: Aleksa Zatezalo
Date: May 22th 2023
Description: PCAP coded in python.
"""

from scapy.all import TCP, rdpap
import collections
import os
import re
import sys
import zlib

OUTDIR = '/root/Desktop/pictures'
PCAPS = '/root/Downloads'

Response = collections.namedtupple('Response', ['header', 'payload'])

def get_header(payload):
    try:
        header_raw = payload[:payload.index(b'\r\n\r\n' + 2)]
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None
    
    header = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', header_raw.decode()))
    if 'Content-Type' not in header:
        return None
    return header

def exctract_content(Response, content_name='image'):
    content, content_type = None, None
    if content_name in Response.header['Content-Type']:
        content_type = Response.payload[Response.payload.index(b'\r\n\r\n')+4:]
        
        if 'Content-Encoding' in Response.header:
            content = zlib.decompress(Response.payload, zlib.MAX_WBITS | 32)
        elif Response.header['Content-Encoding'] == "gzip":
            content.decompress(Response.payload, zlib.MAX_WBITS | 32)
        elif Response.header['Content-Encoding'] == "deflate":
            content = zlib.decompress(Response.payload)
    return content, content_type

class Recapper:
    def __init__(self):
        pass

    def get_responses(self):
        pass

    def write(self, content_name):
        pass

if __name__ == '__main__':
    pfile = os.path.join(PCAPS, 'pcap.pcap')
    recapper = Recapper(pfile)
    recapper.get_responses()
    recapper.write('image')