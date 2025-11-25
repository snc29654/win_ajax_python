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
sub_title=[]

zip_code=form.getvalue("sent2")
sub_title=form.getvalue("sent5")
sub_title="<font color=\"green\">"  + sub_title + "</font>" + "<br>"
sub_title=sub_title.replace("。","。<br>")

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
        
    #select_sql = 'update users set weather = ? where id =?',(str(sub_title), str(zip_code))
    c.execute("UPDATE users SET kind = ? WHERE id = ?", (sub_title, zip_code))
    conn.commit()

print("Content-type: text/html\n")

print(str(zip_code)+"のサブタイトルを変更しました")
