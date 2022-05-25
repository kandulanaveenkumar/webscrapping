from email import header
import encodings
from platform import libc_ver
from tkinter.font import names
from django import urls
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import hashlib
import json
from lxml import etree
from scrapy.http import HtmlResponse

last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

mylist = []

for i in range(1,2225):
    print(i)
   

    url = f"https://www.sebi.gov.in/sebiweb/ajax/home/getnewslistallinfo.jsp"



    # payload = "companyname=Idea Engine"

    payload = {"nextValue": f"{i}"}

    headers = {

        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',

        # "authority": "www.mca.gov.in",

        # "content-type": "application/x-www-form-urlencoded; charset=UTF-8",

    }

    res = requests.post(url, headers=headers, data=payload)

    resp = HtmlResponse("example.com",body=res.text,encoding='utf-8')
    #print(resp.xpath("//table//tr"))

    for j in resp.xpath("//table//tr"):
        d = {
            "Title" : "",
            "Source" : "www.sebi.gov.in",
            "publishedAt" : "",
            "URL" : "",
            "query" : "",
            "uid" : "",
            "Content" : ""
        }
        try:

            date = j.xpath("./td[1]/text()").get()
            if date!="":
                d["publishedAt"] = date

        except:
            pass
        #print(date)
        try:

            title = j.xpath("./td[3]/a/text()").get()
            if title!="":
                d["Title"] = title

        except:
            pass
        
        try:

            url = j.xpath("./td[3]/a/@href").get()
            if url!="":
                d["URL"] = url

        except:
            pass

        try:

            d["Content"] = "For more information : " + d["URL"]

        except:
            pass

        try:


            d["uid"] = hashlib.sha256(
                ((d["Title"]+ d["publishedAt"] +"Combined Forces Special Enforcement Unit (CFSEU ) Press Release, Canada").lower()).encode()).hexdigest()
        
        except:
            pass

        try:

            if d["Title"]!="":
                mylist.append(d)
                print(d)

        except:
            pass


with open('w1.json', 'w', encoding="utf-8") as file:
   json.dump(mylist, file, ensure_ascii=False, indent=4)







