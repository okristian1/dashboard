#!/bin/env python

import requests
import sys
import os
import subprocess
import time 
import json
import requests
import schedule

from config import quote_api_key, news_api_key

host_status=""
quote=""
news=""

print("bagofdicks")

def newsFeed():
    global news
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
    global quote
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
    global host_status
    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(
                ['ping', '-c', '3', '192.168.68.111'],
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

def clear():
    os.system('clear')


clear()
newsFeed()
getQuote()
getHostStatus()

schedule.every(1130).seconds.do(clear)
schedule.every(1130).seconds.do(newsFeed)
schedule.every(1130).seconds.do(getQuote)
schedule.every(5).seconds.do(getHostStatus)

while True:
    schedule.run_pending()
    time.sleep(5)

