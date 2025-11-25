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
find_all_param=form.getvalue("sent8")

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

    r = requests.get(url)

    data = BeautifulSoup(r.content, 'html.parser')
    find_data=data.find_all(find_all_param)
    return(find_data)



zip_code=form.getvalue("sent2")
news_comment=form.getvalue("sent3")

find_data=data_print(zip_code)
date = datetime.date.today()

name="お気に入り"
weather=news_comment
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
    Contents = Contents.replace ("\n","")
    Contents = Contents.replace ("\t","")
    Contents = Contents.replace ("。","。<br>")
    Contents=Contents.replace("\u3000"," ") 
    zip_code="<a href=\""+zip_code+"\" target=\"_blank\">"+zip_code+"</a>"
    #weather=weather.replace("\u3000"," ")
    insert_sql = 'insert into users (date, name, weather, kind, zip_code,Contents) values (?,?,?,?,?,?)'
    users = [
    (date, name, weather, kind, zip_code,Contents)
    ]
    c.executemany(insert_sql, users)
    conn.commit()

print("Content-type: text/html\n")
Contents=Contents.replace("<a","<a target=\"_blank\"")
print(Contents)
