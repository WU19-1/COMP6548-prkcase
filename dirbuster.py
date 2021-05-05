from getopt import getopt
from threading import Thread
import sys
import requests

wordlist = []
thread_count = 0
extension = ['']
ip = ''
port = 0
uri = ''

def check(path,index,end,step):
    global extension
    try:
        for i in range(index,end,step):
            for ext in extension:
                full_path = path + wordlist[i].rstrip() + (("." + ext) if ext != '' else '/')
                # print("fullpath : ",full_path)
                resp = requests.get(url=full_path)
                if resp.status_code == 404:
                    continue
                elif resp.status_code == 200:
                    print(full_path,"200 OK")
                elif resp.status_code == 403:
                    print(full_path,"403 Forbidden")
    except Exception as e:
        print(e)

def process():
    global wordlist, thread_count, extension, ip, port, uri
    target = (ip + (":" + str(port)) if port != 0 else ip) + (uri + "/" if uri != '' else '')
    print(target)

    end = len(wordlist)

    for i in range(thread_count):
        # print(i,end,thread_count)
        t = Thread(target=check,args=(target,i,end,thread_count,))
        t.start()

        t.join()


def main():
    global wordlist, thread_count, extension, ip, port, uri
    args, _ = getopt(sys.argv[1:], shortopts="w:T:e:t:p:u:", longopts=["wordlist=","thread=","extension=","target=","port=","uri="])

    if len(args) == 0:
        print("usage:")
        print("python dirbuster.py -w ./wordlist.txt -T 20 -e php,txt -t 127.0.0.1 -p 80 -u /admin")
        exit()

    for k, v in args:
        if k in ['-w','--wordlist']:
            wordlist = open(v).readlines()
        elif k in ['-T','--thread']:
            thread_count = int(v)
        elif k in ['-e','--extension']:
            extension = v.split(',')
            extension.append('')
        elif k in ['-t','--target']:
            ip = 'http://' + v
        elif k in ['-p','--port']:
            port = int(v)
        elif k in ['-u','--uri']:
            uri = v
    
    process()

if __name__ == "__main__":
    main()