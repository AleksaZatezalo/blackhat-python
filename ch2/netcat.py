"""
Author: Aleksa Zatezalo
Date: May 10th 2023
Description: Netcat re-written in python.
"""

import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)

    return output.decode()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BHP Net Tool', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''Example:
                                     netcat.py -t 192.168.1.108 - p 555 -l -c #command shell
                                     netcat.py -t 192.168.1.108 - p 555 -l -u=mytest.txt #file to upload
                                     netcat.py -t 192.168.1.108 - p 555 -l -e \"cat /etc/passwd\" #execute command
                                     echo ABC | ./netcat.py -t 192.168.1.108 - p 135 #echo text to port 135
                                     netcat.py -t 192.168.1.108 - p 555 #connect to server'''))
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specific command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('t', '--target', default='192.168.1.203', help="specific IP")
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    
    nc = NetCat(args, buffer.encode)
    nc.run()
