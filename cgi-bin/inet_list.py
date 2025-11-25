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

import re
import sys
import bs4
import requests
from urllib.parse import urljoin





cgitb.enable()
form=cgi.FieldStorage()
dbname='../'+ form.getvalue("sent4")
news_comment=form.getvalue("sent3")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

zip_code=[]
def  get_link(url):
    f = open('links.txt', 'w', encoding='UTF-8')
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "lxml")
    links = soup.select("a")

    type_links=type(links)
    f.write(str(type_links))
    f.write("\n")

    keys = set()
    results = []
    for link in links:
        f.write(link.text)
        f.write("\n")
        link_url = link.get("href")
        if not link_url:
            continue

        if not link_url.startswith("http"):
            link_url = urljoin(url, link_url)

        link_text = link.text
        if not link_text:
            link_text = ""
        link_text = link_text.strip()
        link_text = re.sub(r"\n", " ", link_text)

        key = link_url + link_text
        if key in keys:
            continue
        keys.add(key)

        results.append({"url": link_url, "text": link_text})

    return results


def  copy_link(url,filter):
    results = get_link(url)
    f = open('tracefile.txt', 'w', encoding='UTF-8')
    f2 = open('tracefile2.txt', 'w', encoding='UTF-8')
    text = ""
    for result in results:
        result_text = result["text"]
        #if  filter == "all":
        if  filter == None:
            text +=  "<a href= \"" + result["url"] +  "\"" +" target=\"_blank\"" + "</a>" +"<br>" +"\n"   
            text +=  result["text"] +"<br>"   
            text +=  "<div>"+result["url"] +"</div>"   

            text +=  "<a>"   

            text+=" <input value=\"scrape\" style=\"background-color:gray\" onclick=\"func_news_list("
            text+=repr(result["url"])
            text+=","
            text+=repr(result["text"])
            text+=")  \"  type=\"button\"></input>"

            text +=  "</a>"   
            text +=  "<a>"

            text+=" <input value=\"next\" style=\"background-color:gray\" onclick=\"func_list_next("
            text+=repr(result["url"])
            text+=","
            text+=repr(result["text"])
            text+=")  \"  type=\"button\"></input>"

            text +=  "</a>"




            f2.write(result["url"])
            f2.write("\n")

            f.write(result["text"])
            f.write("<br>")
            f.write(result["url"])
            f.write("<br>")
            f.write("<br>")
            f.write("\n")
        else:
            if  filter in result_text:
                text +=  "<a href= \"" + result["url"] +  "\"" +" target=\"_blank\"" + "</a>" +"<br>" +"\n"   
                text +=  result["text"] +"<br>"   
                f.write(result["text"])
                f.write("<br>")
                f.write(result["url"])
                f.write("<br>")
                f.write("<br>")
                f.write("\n")


    return(text)



zip_code=form.getvalue("sent2")
filter=form.getvalue("sent5")
find_data=copy_link(zip_code,filter)

date = datetime.date.today()

name="URLリスト"
weather=news_comment
kind=filter

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
    Contents = Contents.replace("\n","")
    Contents = Contents.replace("\t","")
    zip_code="<a href=\""+zip_code+"\" target=\"_blank\">"+zip_code+"</a>"
    insert_sql = 'insert into users (date, name, weather, kind, zip_code,Contents) values (?,?,?,?,?,?)'
    users = [
    (date, name, weather, kind, zip_code,Contents)
    ]
    c.executemany(insert_sql, users)
    conn.commit()

print("Content-type: text/html\n")

f = open('tracefile.txt', 'r', encoding='UTF-8')
read_data=f.read()


#print("<font color=\"red\">"  + "テキスト表示" + "</font>")
#print("<br>")
#print(read_data)
#print("<br>")
#print("<br>")
#print("<br>")
print("<font color=\"green\">"  + "リンク表示" + "</font>")
print(find_data)
