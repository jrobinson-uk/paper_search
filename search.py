from subprocess import call
from datetime import datetime,timedelta
import mechanicalsoup
import csv
import re
import json

import configparser
from random import randint
from pprint import pprint
import glob
import urllib.parse

existing = glob.glob("*/*.bib")
with open("files_captured",mode="w") as f:
    for file in existing:
        f.write("{}\n".format(str(file)))

from datetime import date,datetime
from re import sub
from time import sleep

from fake_useragent import UserAgent
ua = UserAgent()

def read_list():
    queue = [line. rstrip('\n') for line in open("theories-terms.csv")].copy()
    complete = [line. rstrip('\n') for line in open("complete")].copy()
    failed = [line. rstrip('\n') for line in open("failed")].copy()
    return queue,complete,failed

def single_search(term1,folder,url):
    pause = randint(30,60)
    b = mechanicalsoup.StatefulBrowser(soup_config={'features':'lxml'},raise_on_404=False,user_agent=ua.random,)
    print(term1)
    print(url)
    results = 0
    filename="{}/{}.bib".format(folder,term1)
    #print("searching {}".format(folder))
    response = b.open(url)

    with open("HTML/{}/{}.html".format(folder,term1),mode="wb") as f:
        f.write(response.content)
    results=re.search(b'[\d,]+<\/strong>',response.content)
    print(results)
    if results==None:
        status = False
    else:
        status=True
        results = int(results.group(0).decode("utf-8")[:-9].replace(',', ''))
        with open("log.csv", mode="a") as f:
            f.write("{}.{},{},{}\n".format(datetime.now(),term1,results,url))
        sleep(randint(5,10))
        try:
            with open(filename, mode="wb") as f:
                print("{} open...".format(filename))
                if results > 0:
                    bib = b.follow_link("bibtex")
                    f.write(bib.content)
                    print("...bibtex written.")

        except:

            with open("log.csv", mode="a") as f:
                f.write("{},{},{},{}\n".format(datetime.now(),term1,"FAIL",url))

    print("pause",pause)
    sleep(pause)
    return status

#sleep(300)
queue,complete,failed = read_list()
print("{} in search queue".format(len(queue)))
print("{} already complete".format(len(complete)))
print("OUTSTANDING SEARCHS")
for search in list(set(queue)-set(complete)):
    print(search)
#pprint(failed)
#with open("log.csv", mode="w") as f:
    #f.write("Result,Term,URL\n")
for term in queue:
    #print(term)
    terms = term.split(",")
    #print(terms)
    #print(type(terms))
    if term not in complete:
        url1 ="https://dl.acm.org/results.cfm?query=(%252B{})&within=owners.owner=HOSTED&filtered=&dte=&bfr=".format(urllib.parse.quote(terms[1]))
        url2 ="https://dl.acm.org/results.cfm?within=owners.owner%3DHOSTED&srt=_score&query=(%252B{}%29++AND+acmdlCCS%3A%28%252B%22Computing+Education%22%29&Go.x=0&Go.y=0".format(urllib.parse.quote(terms[1]))
        #print(url1)
        #print(url2)
        status1 = True#single_search(term,"ALL",url1)
        status2 = single_search(term,"CSE",url2)
        print(status1,status2)
        if status1 and status2:                           #  https://dl.acm.org/results.cfm?query=(%252B%22{}%22)&within=owners.owner=HOSTED&filtered=&dte=&bfr=
            complete.append(term)
            with open ("complete",mode="w") as f:
                for term in complete:
                    f.write("{}\n".format(term))
        else:
            failed.append(term)
            with open ("failed",mode="w") as f:
                for term in failed:
                    f.write("{}\n".format(term))







    #single_search(term_x,"CSE","https://dl.acm.org/results.cfm?within=owners.owner%3DHOSTED&srt=_score&query=%28%252B{0}%29++AND+acmdlCCS%3A%28%252B%22Computing+Education%22%29&Go.x=0&Go.y=0".format(term_x))
    #input()

#acm_url_cse = "https://dl.acm.org/results.cfm?within=owners.owner%3DHOSTED&srt=_score&query=%28%252B{0}%29++AND+acmdlCCS%3A%28%252B%22Computing+Education%22%29&Go.x=0&Go.y=0".format(term1)
#acm_url_all = "https://dl.acm.org/results.cfm?query=(%252B{})&within=owners.owner=HOSTED&filtered=&dte=&bfr=".format(term1)
