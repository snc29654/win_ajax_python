#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json
import sys
import io
import requests
from bs4 import BeautifulSoup
import sqlite3
from contextlib import closing
import datetime

cgitb.enable()
form=cgi.FieldStorage()
dbname='../'+ form.getvalue("sent4")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

zip_code=[]

def  data_print(url):
    global zip_code

    params = {'p':zip_code,
          'search.x':'1',
          'fr':'top_ga1_sa',
          'tid':'top_ga1_sa',
          'ei':'UTF-8',
          'aq':'',
          'oq':'',
          'afs':'',}

    r = requests.get(url, params=params)

    data = BeautifulSoup(r.content, 'html.parser')
    return(data)



zip_code=form.getvalue("sent2")

zip_code_split=zip_code.split()

split_len=len(zip_code_split)

find_data=data_print("http://search.yahoo.co.jp/search")

date = datetime.date.today()

name="検索"
weather=""
kind=""
with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()
    create_table = '''create table users (id INTEGER PRIMARY KEY,date varchar(64), name varchar(64),
                      weather varchar(64), kind varchar(32), zip_code varchar(64),Contents varchar(256))'''
    try:
        c.execute(create_table)
    except:
        pass
        
    scraping_contents=find_data
    Contents = str(scraping_contents)
    Contents=Contents.replace("<a","<a target=\"_blank\"")
    
    if (split_len==3):
        Contents=Contents.replace(zip_code_split[0],"<font color=\"red\">"  + zip_code_split[0] + "</font>" )
        Contents=Contents.replace(zip_code_split[1],"<font color=\"red\">"  + zip_code_split[1] + "</font>" )
        Contents=Contents.replace(zip_code_split[2],"<font color=\"red\">"  + zip_code_split[2] + "</font>" )
    if (split_len==2):
        Contents=Contents.replace(zip_code_split[0],"<font color=\"red\">"  + zip_code_split[0] + "</font>" )
        Contents=Contents.replace(zip_code_split[1],"<font color=\"red\">"  + zip_code_split[1] + "</font>" )
    if (split_len==1):
        Contents=Contents.replace(zip_code_split[0],"<font color=\"red\">"  + zip_code_split[0] + "</font>" )
    
    #Contents=Contents.replace(zip_code,"<font color=\"red\">"  + zip_code + "</font>" )
    zip_code="<font color=\"red\">"  + zip_code + "</font>"

    zip_code=zip_code.replace("\u3000"," ")

    insert_sql = 'insert into users (date, name, weather, kind, zip_code,Contents) values (?,?,?,?,?,?)'
    users = [
    (date, name, zip_code, kind, weather,Contents)
    ]
    c.executemany(insert_sql, users)
    conn.commit()

print("Content-type: text/html\n")
#print(find_data)
print(Contents)
