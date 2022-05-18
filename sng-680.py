from email import header
from platform import libc_ver
import requests
from bs4 import BeautifulSoup
import re
from scrapinghelp import htmlhelper
from datetime import datetime
import hashlib
import json
from lxml import etree
from deep_translator import GoogleTranslator

last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def langtranslation(to_translate):
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
    except:
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
        except:
            print(f">>>Translartion Bug : {to_translate}")
            translated = to_translate  
    return translated

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

url = "https://www.cpib.gov.sg/press-room/press-releases/"
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

data_tag = requests.get(url)

htmlcontent = data_tag.content
#print(htmlcontent)

soup = BeautifulSoup(htmlcontent,'html.parser')

correct_links = soup.find("div" ,{"class":"row is-multiline"}).find_all("a",href=True)

links_with_text = [a['href'] for a in correct_links if a.text]
#print(links_with_text)

# href_tags = soup.find_all(href=True)
# print(href_tags)

mylist = []
for i in links_with_text:
    d = {
        "Title" : "",
        "Source" : "www.cpib.gov.sg",
        "publishedAt" : "",
        "URL" : "",
        "query" : "",
        "uid" : "",
        "Content" : ""
    }
    link = "https://www.cpib.gov.sg"+i
    d["URL"] = link
    res = requests.get(link)
    res_soup = BeautifulSoup(res.content,'html.parser')
    dom = etree.HTML(str(res_soup))
    try:
        l = res_soup.find('title').text
        if l!="":
            d["Title"] = l
        #print(l)

    except:
        pass
    
    try:
        contex  = dom.xpath("//div[@class='col is-8 is-offset-2 print-content']//text()")
        content_l = []
        for j in contex:
            if j.strip():
                content_l.append(j.strip().replace("\xa0\xa0",""))
        content = "".join(content_l)
        if content!="":
            d["Content"] = content
        #print(content)
    except:
        pass
    
    try:
        date = dom.xpath("//small[@class='has-text-white']/text()")
        #print(date)
        d["publishedAt"]=date[0]

    except:
        pass

    try:
        d["uid"] = hashlib.sha256(
            ((d["Title"] +d["publishedAt"]+"Corrupt Practices Investigation Bureau (CPIB) Singapore Press Release, Singapore").lower()).encode()).hexdigest()

    except:
        pass

    try:
        mylist.append(d)
        print(d)
    except:
        pass

with open('w1.json', 'w', encoding="utf-8") as file:
   json.dump(mylist, file, ensure_ascii=False, indent=4)