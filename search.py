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
existing = glob.glob("*/*.bib")
print(existing)

#input()
from datetime import date,datetime
from re import sub
from time import sleep
import bibtexparser
from fake_useragent import UserAgent
ua = UserAgent()

def read_list(file):
    terms=[]
    with open (file, mode="r") as f:
        for line in f:
            terms.append(line.rstrip())
    print(terms)
    return terms

def single_search(term1):
    pause=0
    b = mechanicalsoup.StatefulBrowser(soup_config={'features':'lxml'},raise_on_404=False,user_agent=ua.random,)
    acm_url_cse = "https://dl.acm.org/results.cfm?within=owners.owner%3DHOSTED&srt=_score&query=%28%252B{0}%29++AND+acmdlCCS%3A%28%252B%22Computing+Education%22%29&Go.x=0&Go.y=0".format(term1)
    acm_url_all = "https://dl.acm.org/results.cfm?query=(%252B{})&within=owners.owner=HOSTED&filtered=&dte=&bfr=".format(term1)
    print(term1)

    results = 0
    filename="CSE/{}.bib".format(term1.strip('\"'))
    print(filename)
    if filename in existing:
        print("skipping CSE")
    else:
        print("searching CSE")
        response = b.open(acm_url_cse)
        print(response)
        with open("HTML/CSE/{}.html".format(term1),mode="wb") as f:
            f.write(response.content)
        sleep(randint(5,10))
        try:
            bib = b.follow_link("bibtex")
            with open(filename, mode="wb") as f:
                f.write(bib.content)
            with open("log.csv", mode="a") as f:
                f.write("{},{},{},{}\n".format(term1,"CSE","Success",acm_url_cse,"\n"))

        except:
            with open("log.csv", mode="a") as f:
                f.write("{},{},{},{},{}\n".format(pause,term1,"CSE","Failed",acm_url_cse))
        pause = randint(60,120)
        print("pause",pause)
        sleep(pause)



    #filename="ALL/{}.bib".format(term1.strip('\"'))
    #print(filename)
    #if filename in existing:
    #    print("skipping ALL")
    #else:
    #    print("searching ALL")

    #    response = b.open(acm_url_all)
    #    print(response)
    #    with open("HTML/ALL/{}.html".format(term1),mode="wb") as f:
    #        f.write(response.content)
    #    sleep(randint(5,10))
    #    try:
    #        bib = b.follow_link("bibtex")
    #        with open(filename.format(term1), mode="wb") as f:
    #            f.write(bib.content)
    #        with open("log.csv", mode="a") as f:
    #            f.write("{},{},{},{}\n".format(term1,"ALL","Success",acm_url_all))
    #    except:
    #        with open("log.csv", mode="a") as f:
    #            f.write("{},{},{},{},{}\n".format(pause,term1,"ALL","Failed",acm_url_all))
    #    pause = randint(60,120)
    #    print("pause",pause)

    #    sleep(pause)
    #b.close()
#def multi_search(term1, term2):
#    b = mechanicalsoup.StatefulBrowser(soup_config={'features':'lxml'},raise_on_404=False,user_agent='Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',)
#    acm_url = "https://dl.acm.org/results.cfm?query=(%252B%22{0}%22%20%252B%22{1}}%22)&within=owners.owner=HOSTED&filtered=&dte=&bfr=".format(term1,term2)
#    print(acm_url)
#    #response = b.open(url)
#    return b,response


#sleep(300)
terms = read_list("terms")
for term_x in terms:
    single_search(term_x)
