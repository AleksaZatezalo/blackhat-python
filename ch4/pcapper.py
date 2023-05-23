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
    pass

def exctract_content(Response, content_name='image'):
    pass

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