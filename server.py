import socket
from threading import Thread
from getopt import getopt
import sys
from typing import final

IP = '127.0.0.1'
PORT = 1234
LISTEN = True

def info():
    print("Help info here...")
    print("Figure it yourself")

def send(con):
    try:
        while True:
            msg = input("Input message : ")
            if msg == "exit":
                break
            con.send(msg.encode())
    except Exception:
        con.close()
    finally:
        con.close()

def recv(con):
    try:
        while True:
            msg = con.recv(4096).decode()
            print("\nMessage : ")
            print(msg)
    except Exception:
        con.close()
    finally:
        con.close()

def main():
    global IP, PORT

    args, _ = getopt(sys.argv[1:],"i:p:h",["ip","port","help"])
    for key, value in args:
        if key in ['-h','--help']:
            exit(info())
        elif key in ['-i','--ip']:
            IP = value
        elif key in ['-p','--port']:
            PORT = int(value)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((IP, PORT))

    s.listen(1)
    con, addr = s.accept()

    print("[ + ] Connected to %s:%s"%(addr[0], addr[1]))

    t1 = Thread(target=recv, args=(con,))
    t2 = Thread(target=send, args=(con,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()