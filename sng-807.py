from email import header
import encodings
from lib2to3.pgen2.tokenize import TokenError
from platform import libc_ver
from tkinter import N
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

url = "https://www.msei.in/Investors/defaulters"
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

data_tag = requests.get(url)

htmlcontent = data_tag.content
#print(htmlcontent)
#print(correct_links)

resp = HtmlResponse("example.com",body=data_tag.text,encoding='utf-8')

mylist = []

for j in resp.xpath("//tr[@class='alt']"):
    name = j.xpath("normalize-space(./td[4]/text())").get()
    date = j.xpath("normalize-space(./td[3]/text())").get()
    #print(date)
    d= {
        "uid": "",
                    "name": "",
                    "alias_name": [],
                    "country": [],
                    "list_type": "Entity",
                    "last_updated": last_updated_string,
                    "nns_status": "False",
                    "address": [
                    {
                    "country": "",
                    "complete_address": ""
                    }
                    ],
                    "entity_details": {},
                    "sanction_details":{
                        "issue_date":""
                    },
                    "documents": {},
                    "comment": "",
                    "sanction_list": {

                        "sl_authority": "Metropolitan Stock Exchange, India",

                        "sl_url": "https://www.msei.in/Investors/defaulters",

                        "watch_list": "India Watchlists",

                        "sl_host_country": "India",

                        "sl_type": "Sanctions",

                        "sl_source": "MSE Expelled Members, India",

                        "sl_description": "list of Debarred Entities by Metropolitan Stock Exchange, India",

                        "list_id": "IND_E20322"
                        }
    }
    try:
        if name!="" and name!="Defaulting Clients database":
            d["name"] = name

        if date!="":
            d["sanction_details"]["issue_date"] = date

    except:
        pass


    try:
        d["uid"] = hashlib.sha256(
            ((d["name"] + d["sanction_list"]["sl_source"]+d["sanction_list"]["sl_host_country"]+d["address"][0]["complete_address"]).lower()).encode()).hexdigest()
    except:
        pass


    try:
        if d["name"]!="":
            mylist.append(d)
            #print("k")
    except:
        pass
    


with open('w1.json', 'w', encoding="utf-8") as file:
    json.dump(mylist, file, ensure_ascii=False, indent=4,default=str)
