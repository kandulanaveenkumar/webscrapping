from email import header
import encodings
from platform import libc_ver
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

for p in range(1,21):
    url = f"https://www.cfseu.bc.ca/media/page/{p}"
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    data_tag = requests.get(url)

    htmlcontent = data_tag.content
    #print(htmlcontent)

    soup = BeautifulSoup(htmlcontent,'html.parser')

    correct_links = [i.find("a",href=True) for i in soup.find_all("div",{"class":"isotopePadding"})]
    #print(correct_links)


    #links_with_text = [a['href'] for a in correct_links if a.text]
    #print(links_with_text)

    #print(properlinks)

    for i in correct_links:
        d = {
            "Title" : "",
            "Source" : "www.cfseu.bc.ca",
            "publishedAt" : "",
            "URL" : "",
            "query" : "",
            "uid" : "",
            "Content" : ""
        }
        url = i['href']
        #print(url)
        title = i.text
        d["Title"] = title
        #print(title)
        d["URL"] = url
        res = requests.get(url)
        # res_soup = BeautifulSoup(res.content,'html.parser')
        resp = HtmlResponse("example.com",body=res.text,encoding='utf=8')
        # print(res.xpath("//table"))
        content  = "".join(resp.xpath("//div[@itemprop='articleBody']//text()").getall())
        date = resp.xpath("//a[@itemprop = 'datePublished']/@content").get()
        d["Content"] = content
        d["publishedAt"] = date
        #print(date)
        #print(content)

        d["uid"] = hashlib.sha256(
            ((d["Title"] +"Combined Forces Special Enforcement Unit (CFSEU ) Press Release, Canada").lower()).encode()).hexdigest()


        if d["Title"]!="":
            mylist.append(d)
            print(d)


with open('w1.json', 'w', encoding="utf-8") as file:
   json.dump(mylist, file, ensure_ascii=False, indent=4)