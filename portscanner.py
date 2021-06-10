from re import L
from scapy.all import *
from socket import socket
import getopt
from threading import Thread, Event, current_thread
import sys

THREAD_LIST = []
event = Event()
OPEN_PORTS = []
FILTERED_PORTS = []
TIMEOUT = 3
ICMP_UNREACHABLE_ERROR = [1,2,3,9,10,13]

# https://scapy.readthedocs.io/en/latest/api/scapy.layers.inet.html

def xmas(ip, start, end, step):
    for port in range(start, end, step):
        resp = sr1(IP(dst=ip)/TCP(dport=port,flags="FPU"),timeout=TIMEOUT)
        if type(resp).__name__ == 'NoneType':
            OPEN_PORTS.append(port)
        elif resp.haslayer(TCP):
            if resp.haslayer(ICMP):
                if int(resp.haslayer(ICMP).type) == 3 and int(resp.haslayer(ICMP).code) in ICMP_UNREACHABLE_ERROR:
                    FILTERED_PORTS.append(port)

def null(ip, start, end, step):
    for port in range(start, end, step):
        resp = sr1(IP(dst=ip)/TCP(dport=port,flags=""),timeout=TIMEOUT)
        if type(resp).__name__ == 'NoneType':
            OPEN_PORTS.append(port)
        elif resp.haslayer(TCP):
            if resp.haslayer(ICMP):
                if int(resp.haslayer(ICMP).type) == 3 and int(resp.haslayer(ICMP).code) in ICMP_UNREACHABLE_ERROR:
                    FILTERED_PORTS.append(port)

def fin(ip, start, end, step):
    for port in range(start, end, step):
        resp = sr1(IP(dst=ip)/TCP(dport=port,flags="F"),timeout=TIMEOUT)
        if type(resp).__name__ == 'NoneType':
            OPEN_PORTS.append(port)
        elif resp.haslayer(TCP):
            if resp.haslayer(ICMP):
                if int(resp.haslayer(ICMP).type) == 3 and int(resp.haslayer(ICMP).code) in ICMP_UNREACHABLE_ERROR:
                    FILTERED_PORTS.append(port)

def syn(ip, start, end, step):
    for port in range(start, end, step):
        s = socket()
        s.settimeout(3)
        res = s.connect_ex((ip, port))
        if res == 0:
            OPEN_PORTS.append(port)

def stealthsyn(ip, start, end, step):
    for port in range(start, end, step):
        resp = sr1(IP(dst=ip)/TCP(dport=port,flags="S"), timeout=TIMEOUT)
        if type(resp).__name__ == 'NoneType':
            FILTERED_PORTS.append(port)
        elif resp.haslayer(TCP):
            if resp.haslayer(TCP).flags == 0x12:
                # send rst packet, cancel SYN packet
                sr1(IP(dst=ip)/TCP(dport=port,flags="R"), timeout=TIMEOUT)
                OPEN_PORTS.append(port)
            elif resp.haslayer(ICMP):
                if int(resp.haslayer(ICMP).type) == 3 and int(resp.haslayer(ICMP).code) in ICMP_UNREACHABLE_ERROR:
                    FILTERED_PORTS.append(port)

def checker():
    while len(THREAD_LIST) != 0:
        pass
    else:
        event.set()

def main():
    options, _ = getopt(sys.argv[1:], "i:s:e:t:", ["--ip=", "--startPort=", "--endPort=", "--thread=", "--xmas",  "--fin", "--null", '--syn', '--stealthsyn'])
    mode = -1
    count = 0
    for k, v in options:
        if k in ['-i', '--ip']:
            ip = v
        elif k in ['-s', '--startPort']:
            start = int(v)
        elif k in ['-e', '--endPort']:
            end = int(v)
        elif k in ['-t', '--thread']:
            count = int(v)
        elif mode == -1:
            if k == '--xmas':
                mode = 0
            elif k == '--fin':
                mode = 1
            elif k == '--null':
                mode = 2
            elif k == '--syn':
                mode = 3
            elif k == '--stealthsyn':
                mode = 4
    
    scan_mode = {
        0 : xmas,
        1 : fin,
        2 : null,
        3 : syn,
        4 : stealthsyn
    }

    if mode != -1 and (start > 0 and start < 65536) and (end > 0 and end < 65536 and end > start):
        for begin in range(count):
            t = Thread(target=scan_mode[mode],args=(ip, begin + start, end, count,))
            THREAD_LIST.append(t)

            t.start()

    event.wait()
    
    print("Port scanning process is finish: ")
    print("Open ports : ")
    for op in OPEN_PORTS:
        print("[+] %d Open "%(op))
    for fi in FILTERED_PORTS:
        print("[+] %d Open | Filtered"%(fi))

if __name__ == "__main__":
    main()