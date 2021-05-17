import target
import time
from threading import Thread,Event
import os

FILENAME = "log.txt"
targets = []
locked = {}
threads = []
event = Event()

def view_targets():
    global targets
    print("Websites :")
    for i in range(len(targets)):
        if type(targets[i]).__name__ == 'Website':
            print("%d."%(i + 1),targets[i].name,targets[i].bandwith,targets[i].location,targets[i].address)

    print("Servers :")
    for i in range(len(targets)):
        if type(targets[i]).__name__ == 'Server':
            print("%d."%(i + 1),targets[i].name,targets[i].bandwith,targets[i].location,targets[i].spec)
            

def read():
    global FILENAME, event
    try:
        file = open(FILENAME,"r")
        while True:
            event.wait()
            data = file.readlines()

            for log in range(len(data) - 5 if len(data) >= 5 else 0, len(data)):
                print(data[log].rstrip())

            event.clear()
            file.seek(os.SEEK_SET)

    except Exception:
        print("Error happened")
        try:
            file.close()
        except:
            pass

def attack(victim):
    global FILENAME
    for _ in range(20):
        file = open(FILENAME,"a")
        file.write(victim.attacks())
        time.sleep(1.5)
        file.close()

def lock(idx):
    global targets, locked, threads, event
    
    victim = targets.pop(idx)
    
    locked[victim.name] = {}
    locked[victim.name]['bandwith'] = victim.bandwith
    locked[victim.name]['location'] = victim.location
    locked[victim.name]['type'] = type(victim).__name__
    locked[victim.name]['address' if locked[victim.name]['type'] == 'Website' else 'spec'] = victim.address if locked[victim.name]['type'] == 'Website' else victim.spec
    locked[victim.name]['attack_count'] = 0

    t = Thread(target=attack,args=(victim,),daemon=True)
    threads.append(t)

    t.start()
    
def check_ip(ip):
    try:
        invalid = True
        octets = list(map(int,ip.split(".")))
        for octet in octets:
            if octet < 0 or octet > 255:
                break
        else:
            invalid = False
        return invalid
    except:
        return True

def main():
    global targets, threads, event

    reading_thread = Thread(target=read,daemon=True)
    reading_thread.start()
    choose = 0

    while choose != 6:
        print("1. Add Target")
        print("2. View Target")
        print("3. Delete Target")
        print("4. Check Attack Log")
        print("5. Lock Target")
        print("6. Exit")

        try:
            choose = int(input("Choose >> "))
        except:
            print("Invalid input!")

        if choose == 1:
            name = ''
            bandwith = 0
            location = ''
            variety = ''
            address = ''
            spec = ''
            ip = ''
            
            while len(name) < 5 or len(name) > 25:
                name = input("Insert target name [ 5 - 25 characters ] : ")
            
            while bandwith < 100:
                bandwith = int(input("Insert bandwith [ must be more than 100 ] : ")) 
            
            while not location.endswith(('Nation','State','Country')):
                location = input("Insert location [ ends with Nation | State | Country ] [cs] : ")
            
            while variety not in ['Website','Server']:
                variety = input("Insert variety [ Website | Server ] [cs] : ")
            
            if variety == 'Website':
                while not address.startswith('https://'):
                    address = input("Insert address [ starts with https:// ] : ")
                targets.append(target.Website(name, bandwith, location, address))
            elif variety == 'Server':
                while spec not in ['ftp', 'smb']:
                    spec = input("Insert server's type [ ftp | smb ] [cs] : ")
                
                while check_ip(ip):
                    ip = input("Insert ipv4 [ ex : 127.0.0.1 ] : ")
                    
                targets.append(target.Server(name, bandwith, location, spec, ip))



        elif choose == 2:
            view_targets()
        elif choose in [3,5]:
            if len(targets) == 0:
                print("There is no active target!")
                continue
            idx = 0
            while idx < 1 or idx > len(targets):
                view_targets()
                idx = int(input("Insert target [ 1 - %d ] : "%(len(targets))))
            if choose == 3:
                targets.pop(idx - 1)
            else:
                lock(idx - 1)
        elif choose == 4:
            event.set()
            time.sleep(1)
    
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()