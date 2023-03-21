import requests
import sys
import os
import subprocess
import time 
import json
import requests

#from config import quote_api_key, news_api_key

def newsFeed():
    limit = 7
    api_url = 'https://newsapi.org/v2/everything?domains=techcrunch.com'
    response = requests.get(api_url, headers={'X-Api-Key': news_api_key})
    output = response.json()
    for index, item in enumerate(output['articles']):
        print (item['title'])
        if index == limit:
            break
   # data = output['articles'][0]['title']
   # print (data)
    #news = "Todays Headlines: " + response.json#[0]["title"]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def getQuote():
    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': quote_api_key})
    if response.status_code == requests.codes.ok:
        pretty_json = json.loads(response.text)
        quote = "Fact of the day: " + pretty_json[0]["fact"]
        print(quote)
    else:
        print("Error:", response.status_code, response.text)
        
def delete():
    while True:
        sys.stdout.write("\r" + time.ctime())
        sys.stdout.flush()
        time.sleep(1)

def getHostStatus():
    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(
                ['ping', '-c', '3', 'google.no'],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
            )
            sys.stdout.write('\r'+"                                                  ")
            is_up = True
            host_status = (f"Plex Media Server Status: {bcolors.OKGREEN}available{bcolors.ENDC}")
            sys.stdout.write('\r'+host_status)
            sys.stdout.flush()
        except subprocess.CalledProcessError:
            is_up = False
            host_status = (f"Plex Media Server Status: {bcolors.WARNING}not available{bcolors.ENDC}")
            sys.stdout.write('\r'+host_status)
            sys.stdout.flush()

def bufferWriter():
    with open("/dev/tty1", "wb+", buffering=0) as term:
        term.write("\033[2J".encode())
        term.write("\033[H".encode())
        term.write("\n".encode())
        term.write("\n".encode())
        term.write("\n\n\n".encode())
        #term.write("Terminal Write Access Granted".encode())
#        while True:
#            print(term.read(1).decode(), end='')
#            sys.stdout.flush()

while True:
#    delete()
#    bufferWriter()
#    newsFeed()
#    getQuote()
    getHostStatus()
    time.sleep(5)


