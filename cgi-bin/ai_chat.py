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
memo_title=form.getvalue("sent3")

from openai import OpenAI
import key_list

client = OpenAI(api_key=key_list.API_KEY)

completion = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": memo_title,
    }],
    model="gpt-4o-mini",
)

find_data = completion.choices[0].message.content
find_data=find_data.replace("。","。<br>")

date = datetime.date.today()

name="AIチャット"
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
    Contents = Contents.replace ("\n","")
    Contents = Contents.replace ("\t","")
    memo_title="<font color=\"red\">"  + memo_title + "</font>" + "<br>"
    memo_title=memo_title.replace("\u3000"," ")
    insert_sql = 'insert into users (date, name, weather, kind, zip_code,Contents) values (?,?,?,?,?,?)'
    users = [
    (date, name, memo_title, kind, weather,Contents)
    ]
    c.executemany(insert_sql, users)
    conn.commit()

print("Content-type: text/html\n")

print(find_data)
