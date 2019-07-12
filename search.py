from subprocess import call
from datetime import datetime,timedelta
import mechanicalsoup
import csv
import re
import json
import os
import configparser
from pprint import pprint



from datetime import date,datetime
from re import sub
from time import sleep

def search():
    b = mechanicalsoup.StatefulBrowser(soup_config={'features':'lxml'},raise_on_404=F$
    url = "https://dl.acm.org/results.cfm?query=(%252BBehaviorist)&within=owners.owne$
    print(url)
    response = b.open(url)
    return b,response

b,page = search()#get_conferences(year)
print(page.content)

totalstring= re.findall(b"dash; \d+ of \d+",page.content)
total = int(re.findall(b"\d+",totalstring[0])[-1].decode("utf-8"))
print(total)
 #   print(year,total)
 #   pdfs= []
