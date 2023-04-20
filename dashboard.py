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
quote_status=""
news=""
news_status=""

print ("Beep boop initializing dashboard")
def newsFeed():
    global news
    global news_status
    news_status="no"
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
    news_status="nok"


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
    global quote_status
    quote_status = "no"
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
        print (" ")
        print (" ")
        print (" ")
        quote_status = "nok"
    else:
        print ("************************************************************************************************************************")
        print("Error:", response.status_code, response.text)
        print ("************************************************************************************************************************")
        print (" ")
        print (" ")
        print (" ")
        quote_status = "nok"

def getHostStatus():
    global plex_status
    global internet_status
    global offline_test
    iptoping = ['google.com', 'plexmediaserver', 'iphone']
    with open(os.devnull, 'w') as DEVNULL:
        for ip in iptoping:
            res = subprocess.call(
               ['ping', '-c', '1', ip],
               stdout=DEVNULL,  # suppress output
               stderr=DEVNULL
            )
            if (res==0):
                if (ip == 'google.com'):
                    internet_status = (f"Internet Status: {bcolors.OKGREEN}online     {bcolors.ENDC}")
                elif (ip == 'plexmediaserver'):
                    plex_status = (f"Plex Media Server Status: {bcolors.OKGREEN}available     {bcolors.ENDC}")
                elif (ip == 'iphone'):
                    offline_test = (f"iPhone test: {bcolors.OKGREEN}available     {bcolors.ENDC}")
            else:
                if (ip == 'google.com'):
                    internet_status = (f"Plex Media Server Status: {bcolors.WARNING}NOT available{bcolors.ENDC}")
                elif (ip == 'plexmediaserver'):
                    plex_status = (f"Plex Media Server Status: {bcolors.WARNING}NOT available{bcolors.ENDC}")
                elif (ip == 'iphone'):
                    offline_test = (f"iPhone test: {bcolors.WARNING}NOT available{bcolors.ENDC}")

def notOK():
    quote_status="not ok"
    news_status="not ok"

def printHostStatus():
    UP = "\x1B[3A"
    CLR = "\x1B[0K"

    if (quote_status == "ok") and (news_status == "ok"):
        print(f"{UP}{plex_status}{CLR}\n{internet_status}{CLR}\n{offline_test}") 
    else:
        print ("potatoe")

def clear():
    os.system('clear')

clear()
notOK()
getHostStatus()
newsFeed()
getQuote()
printHostStatus()

schedule.every().hour.do(clear)
schedule.every().hour.do(notOK)
schedule.every().hour.do(newsFeed)
schedule.every().hour.do(getQuote)
schedule.every(1).seconds.do(getHostStatus)
schedule.every(1).seconds.do(printHostStatus)

while True:
    schedule.run_pending()
    time.sleep(1)
