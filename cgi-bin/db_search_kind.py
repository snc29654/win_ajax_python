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
    
    select_sql = 'select * from users where name like '+'"%'+str(zip_code)+'%"'
    try:
        for row in c.execute(select_sql):
            row=row[:6]
            number=row[0]

            row3=row[3]
            row5=row[5]



            add_string7="<script>    "
            add_string7=add_string7+"function  func_chg_sub_title"
            add_string7=add_string7+str(number)
            add_string7=add_string7+"(no){"
            add_string7=add_string7+"let str2 = no;"
            add_string7=add_string7+"let str4 = document.getElementById(\"text7\").value;"
            add_string7=add_string7+"if(str4==\"\"){"
            add_string7=add_string7+"str4 = scrapeaction.value;"
            add_string7=add_string7+"}"
            add_string7=add_string7+"let str5 = document.getElementById(\""
            add_string7=add_string7+str(number)
            add_string7=add_string7+"\").value;"
            add_string7=add_string7+"if(str5==\"\"){"
            add_string7=add_string7+"alert(\"サブタイトル未入力\");"
            add_string7=add_string7+"return;"
            add_string7=add_string7+"}"

            add_string7=add_string7+"$.ajax({"

            add_string7=add_string7+"url:'./chg_sub_title.py',"
            add_string7=add_string7+"type:'POST',"
            add_string7=add_string7+"data:{sent2:str2,sent4:str4,sent5:str5}"
            add_string7=add_string7+"})"
            add_string7=add_string7+".done(function(data){"
            add_string7=add_string7+"var smp=document.getElementById(\"inbox\");"
            add_string7=add_string7+"smp.innerHTML = data;"
            add_string7=add_string7+"func_search_kind();"

            add_string7=add_string7+"})"
            add_string7=add_string7+".fail(function(){"
            add_string7=add_string7+"var smp=document.getElementById(\"inbox\");"
            add_string7=add_string7+"smp.innerHTML = \"failed\";"
            add_string7=add_string7+"});"

            add_string7=add_string7+"}"

            add_string7=add_string7+" </script>"

            find_data.append(add_string7)

            f.write(add_string7)


            add_string=" <input value=\"詳細\"  style=\"background-color:lightgreen\" onclick=\"func_one_2("
            add_string=add_string+str(number)
            add_string=add_string+")\"  type=\"button\"></input>"
            find_data.append(add_string)

            add_string3=" <input value=\"text\"  style=\"background-color:lightgreen\" onclick=\"func_one_3("
            add_string3=add_string3+str(number)
            add_string3=add_string3+")\"  type=\"button\"></input>"
            find_data.append(add_string3)
            if(str(zip_code)=="ごみ箱"):
                add_string2=" <input value=\"削除\" style=\"background-color:gray\" onclick=\"func_trush_one("
                add_string2=add_string2+str(number)
                add_string2=add_string2+")\"  type=\"button\"></input>"
                find_data.append(add_string2)

            else:

                add_string2=" <input value=\"削除\" style=\"background-color:gray\" onclick=\"func_del_2("
                add_string2=add_string2+str(number)
                add_string2=add_string2+")\"  type=\"button\"></input>"
                find_data.append(add_string2)

            add_string4=" <input value=\"クリップ\" style=\"background-color:gray\" onclick=\"func_chg_1("
            add_string4=add_string4+str(number)
            add_string4=add_string4+")\"  type=\"button\"></input>"
            find_data.append(add_string4)


            add_string5=" <input value=\"サブタイトル変更\" style=\"background-color:gray\" onclick=\"func_chg_sub_title("
            add_string5=add_string5+str(number)
            add_string5=add_string5+")\"  type=\"button\"></input>"
            find_data.append(add_string5)




            add_string6=" <input type=\"text\" id="
            add_string6=add_string6+str(number)
            add_string6=add_string6+" size=\"160\" value=\""
            add_string6=add_string6+ str(row3)
            add_string6=add_string6+" \" /><br>"
            #find_data.append(add_string6)

            add_string8=" <input value=\"null\" style=\"background-color:gray\" onclick=\"func_chg_sub_title"
            add_string8=add_string8+str(number)
            add_string8=add_string8+"("
            add_string8=add_string8+str(number)
            add_string8=add_string8+")\"  type=\"button\"></input>"
            find_data.append(add_string8)



            f.write(add_string8)


            find_data.append(row)

            find_data.append("<br>")
    except:
        pass

    conn.commit()

print("Content-type: text/html\n")



print(find_data)
