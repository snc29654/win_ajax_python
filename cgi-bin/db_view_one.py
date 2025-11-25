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

f = open('tracefile.txt', 'w', encoding='UTF-8')

zip_code=form.getvalue("sent2")
kensaku=form.getvalue("sent3")

#f.write(kensaku)

find_data=data_print("http://search.yahoo.co.jp/search")

date = datetime.date.today()

name=""
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
    users = [
    (date, name, weather, kind, zip_code,Contents)
    ]
    find_data=[]
    
    select_sql = 'select * from users where id ='+ str(zip_code)
    try:
        for row in c.execute(select_sql):

            if(kensaku == None):
                find_data.append(row)
            else:
                row_str=str(row[:7])
                row_str=row_str.replace(kensaku,"<font color=\"red\">"  + kensaku + "</font>" )
                row_str=row_str + "<br>"
                find_data.append(row_str)

    except:
        pass

    conn.commit()

print("Content-type: text/html\n")

string8=""
string8=string8+" <input value=\"サブタイトル変更\" style=\"background-color:gray\" onclick=\"func_chg_sub_title("
string8=string8+str(zip_code)
string8=string8+")\"  type=\"button\"></input>"

add_string2=" <input value=\"削除\" style=\"background-color:gray\" onclick=\"func_del_2("
add_string2=add_string2+str(zip_code)
add_string2=add_string2+")\"  type=\"button\"></input>"
string8=string8+add_string2

add_string3=" <input value=\"戻る\" style=\"background-color:gray\" onclick=\"func_search_kind("
add_string3=add_string3+")\"  type=\"button\"></input>"
string8=string8+add_string3

print(kensaku)
print(string8)
print(find_data)
