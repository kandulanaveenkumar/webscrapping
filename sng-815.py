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

for i in range(1,944):
    print(i)
    
    url = f"https://www.ibbi.gov.in/orders?page={i}"
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    data_tag = requests.get(url)

    resp = HtmlResponse("example.com",body=data_tag.text,encoding='utf-8')

    for tr in resp.xpath("//table/tbody/tr"):
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

            dates = tr.xpath("./td[1]/text()").get()
            names = tr.xpath("./td[2]/a/text()").get()
            url = tr.xpath("./td[2]/a/@onclick").get()
            prourl = url[url.find("(")+1:url.find(")")]

            if dates!="":
                d["publishedAt"] = dates

            if names!="":
                d["Title"] = names

            if prourl!="":
                d["URL"] = prourl
                d["Content"] = "For More Information:"+""+prourl

        except:
            pass


        try:


            d["uid"] = hashlib.sha256(
                ((d["Title"]+ d["publishedAt"] +"Insolvency and Bankruptcy Board of India Press Releases, India").lower()).encode()).hexdigest()
        
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

            


