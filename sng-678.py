import json
from urllib import response
import requests
import hashlib
from bs4 import BeautifulSoup
from lxml import etree

url = "https://www.mas.gov.sg/api/v1/search?json.nl=map&fq=mas_mastercontenttypes_sm:%22News%22&q=Terrorism%20Suppression%20of%20financing%20Act&rows=10000&fq=site_s:MAS&start=0&wt=json"


data = requests.get(url)
#print(data)

textdata = json.loads(data.text)
print(len(textdata["response"]["docs"]))

mylist = []

for i in textdata["response"]["docs"]:
    d = {
        "Title" : "",
        "Source" : "www.mas.gov.sg",
        "publishedAt" : "",
        "URL" : "",
        "query" : "",
        "uid" : "",
        "Content" : ""
    }
    try:
        title = i["document_title_string_s"]
        if title!="":
            d["Title"] = title
        #print("00000",title)
    except:
        #print("hi")
        pass

    try:
        link = "https://www.mas.gov.sg"+i["page_url_s"]
        d["URL"] = link
        webpage = requests.get(link)

        soup = BeautifulSoup(webpage.content, "html.parser")

        dom = etree.HTML(str(soup))
        content_l = []
        for j in dom.xpath("//div[@class='_mas-typeset contain m-t:l m-b:3xl mas-rte-content']//text()"):
            if j.strip():
                content_l.append(j.strip().replace("\xa0\xa0",""))
        content = "".join(content_l)
        d["Content"] = content
        #print(content)

    except:
        pass


    try:
        published = i["mas_date_tdt"]
        if published!="":
            d["publishedAt"] = published

    except:
        pass

    try:

        d["uid"] = hashlib.sha256(
            ((d["Title"] + i["itemid_s"]+"Monetary Authority of Singapore MAS Terrorism Suppression of financing Act, Singapore").lower()).encode()).hexdigest()

    except:
        pass

    try:
        mylist.append(d)
        print(d)
    except:
        pass

with open('w1.json', 'w', encoding="utf-8") as file:
   json.dump(mylist, file, ensure_ascii=False, indent=4)