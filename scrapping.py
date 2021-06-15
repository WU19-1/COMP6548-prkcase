import requests
from bs4 import BeautifulSoup
import getopt
import sys

class Product:
    productName = ""
    productPrice = 0

    def __init__(self,productName,productPrice):
        self.productName = productName
        self.productPrice = productPrice

ip = ''
port = 0

# print(sys.argv[1:])

try:
    opts, args = getopt.getopt(sys.argv[1:],"ht:p:",["help","target=","port="])
except:
    print("Invalid option")
    exit(0)

for o,a in opts:
    # print(o)
    if o in ("-t","--target"):
        ip = a
    elif o in("-p","--port"):
        try:
            port = int(a)
            print(port)
            if port < 1 or port > 65535:
                print("Invalid port number")
                exit()
        except:
            print("Invalid port")
            exit()
    elif o in ("-h","--help"):
        print("Usage:")
        print("python attacker.py -t targetip -p portnumber")
        print("-t or --target : The ip of the target that you want to attack")
        print("-p or --port : The port number of the target that you want to attack")
        print("\npython attacker.py -h")
        print("-h or --help : print this menu")
        exit()
    
if port == 0 or ip == '':
    print("You must specify ip address and port number")
    exit()

customHeader = {"User-Agent" : "Chrome"}
webPage = requests.get("http://" + ip + ":" + str(port) + "/index.php",headers=customHeader)
# print(webPage.text)

bSoup = BeautifulSoup(webPage.text, 'html.parser')
allProductName = bSoup.find_all("h1", {"class" : "text-4xl"})
allProductPrice = bSoup.find_all("pre")
print(len(allProductName))
# print(allProductName)
# print(allProductPrice)

arr = []

for i in range(0,len(allProductName)):
    try:
        print(allProductName[i].decode_contents(),int(allProductPrice[i].decode_contents().split(" ")[1]))
        obj = Product(allProductName[i].decode_contents(),int(allProductPrice[i].decode_contents().split(" ")[1]))
        # print("obj",obj.productName,obj.productPrice)
        arr.append(obj)
    except:
        continue

# print(arr)

totalAll = 0
for i in arr:
    totalAll = totalAll + i.productPrice
    
print("Sum : $",totalAll)
print("Count :",len(arr),"items")
print("Average : $",totalAll / len(arr))