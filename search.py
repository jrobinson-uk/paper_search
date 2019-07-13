from subprocess import call
from datetime import datetime,timedelta
import mechanicalsoup
import csv
import re
import json
#import os
import configparser
from random import randint
from pprint import pprint
import glob
existing = glob.glob("*.html")

from datetime import date,datetime
from re import sub
from time import sleep

def read_list(file):
    terms=[]
    with open (file, mode="r") as f:
        for line in f:
            terms.append(line.rstrip())
    print(terms)
    return terms

def single_search(b,term1):
    acm_url = "https://dl.acm.org/results.cfm?within=owners.owner%3DHOSTED&srt=_score&query=%28%252B%22{0}%22%29++AND+acmdlCCS%3A%28%252B%22Computing+Education%22%29&Go.x=0&Go.y=0".format(term1)
    print(acm_url)
#    ieee_url = ""

    #if "{}.html".format(term1) in existing:
    #    print("{}.html".format(term1),"done")   #try:
    response = b.open(acm_url)
    print(b.list_links())
    with open("{}.html".format(term1), mode="wb") as f:
        f.write(response.content)
    #        pass
    #print(response.links)

        #response = b.open(url)
    #return b,response

#def multi_search(term1, term2):
#    b = mechanicalsoup.StatefulBrowser(soup_config={'features':'lxml'},raise_on_404=False,user_agent='Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',)
#    acm_url = "https://dl.acm.org/results.cfm?query=(%252B%22{0}%22%20%252B%22{1}}%22)&within=owners.owner=HOSTED&filtered=&dte=&bfr=".format(term1,term2)
#    print(acm_url)
#    #response = b.open(url)
#    return b,response


b = mechanicalsoup.StatefulBrowser(soup_config={'features':'lxml'},raise_on_404=False,user_agent='Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',)
terms = read_list("terms")
for term_x in terms:
    single_search(b, term_x)
    pause = randint(10,30)
    print(pause)
    sleep(pause)
    #for term_y in terms:
    #    if term_x!=term_y:
    #        multi_search()
    #        term_x, term_y)

#def search():
#    b = mechanicalsoup.StatefulBrowser(soup_config={'features':'lxml'},raise_on_404=F$
#    url = "https://dl.acm.org/results.cfm?query=(%252BBehaviorist)&within=owners.owne$
#    print(url)
#    response = b.open(url)
#    return b,response

#b,page = search()#get_conferences(year)
#print(page.content)

#totalstring= re.findall(b"dash; \d+ of \d+",page.content)
#total = int(re.findall(b"\d+",totalstring[0])[-1].decode("utf-8"))
#print(total)
 #   print(year,total)
 #   pdfs= []
