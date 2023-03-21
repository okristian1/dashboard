import requests
import sys
import os
import subprocess
import time 
import json
import requests

from config import quote_api_key, news_api_key

def newsFeed():
    limit = 7
    api_url = 'https://newsapi.org/v2/everything?domains=techcrunch.com'
    response = requests.get(api_url, headers={'X-Api-Key': news_api_key})
    output = response.json()
    print (" ")
    print ("Top Tech News right now: ")
    print (" ")
    print ("========================================================================================================================")
    for index, item in enumerate(output['articles']):
        print (item['title'])
        if index == limit:
            break
    print ("========================================================================================================================")
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
        quote = "Interesting Fact: " + pretty_json[0]["fact"]
        print (" ")
        print ("************************************************************************************************************************")
        print(quote)
        print ("************************************************************************************************************************")
        print (" ")
    else:
        print ("************************************************************************************************************************")
        print("Error:", response.status_code, response.text)
        print ("************************************************************************************************************************")

def getHostStatus():
    while True:
        time.sleep(5)
        with open(os.devnull, 'w') as DEVNULL:
            try:
                subprocess.check_call(
                    ['ping', '-c', '3', 'plexmediaserver'],
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

def bufferWriter(derp):
    with open("/dev/tty1", "wb+", buffering=0) as term:
        if derp == "clear":
            term.write("\033[2J".encode())
            term.write("\033[H".encode())
        elif derp == "space":
            print (" ")
            #term.write("\n\n\n".encode())
        #term.write("Terminal Write Access Granted".encode())
#        while True:
#            print(term.read(1).decode(), end='')
#            sys.stdout.flush()

while True:
    bufferWriter("clear")
    newsFeed()
    getQuote()
    getHostStatus()
    time.sleep(3600)

#sys.stdout.write("\r" + time.ctime())
