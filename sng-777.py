from ast import alias
from cgitb import text
from email import header
import encodings
from platform import libc_ver
from xml.etree.ElementTree import Comment
from django import urls
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import hashlib
import json
from lxml import etree
from scrapy.http import HtmlResponse
from deep_translator import GoogleTranslator

last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def alias_name(name):
    alias_list=[]
    rearrangedNamelist=name.split(' ')
    lastname= rearrangedNamelist.pop(-1)
    rearrangedNamelist=[lastname]+rearrangedNamelist
    alias_list.append(' '.join(rearrangedNamelist))
    return alias_list


def transform_name(name):
        name=name.replace("  ","")
        name=name.replace("\r","")
        name=name.replace("\t","")
        name=name.replace('\n','')
        name = name.replace("_", "")
        name = name.replace("Orientation","")
        name = name.replace("Orientation:","")
        name = name.replace("Ориентировка:","")
        name = name.replace("Ориентировка","")

        name = name.split(',')
        name = name[0]
        name = name.strip()
 
        return name

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


mylist = []

for p in range(0,15):

    print(p)

    url = f"https://fsin.gov.ru/criminal/?PAGEN_1={p}"
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    data_tag = requests.get(url)

    htmlcontent = data_tag.content
    #print(htmlcontent)

    soup = BeautifulSoup(htmlcontent,'html.parser')

    correct_links = [i.find("a",href=True) for i in soup.find_all("div",{"class":"sl-item-title links"})]
    #print(correct_links)

    comments = [i.text for i in soup.find_all("div",{"sl-item-text"})]
    #print(comments)

    listofnames = []
    for i in correct_links:
        names = i.text
        listofnames.append(names)
    #print(listofnames)

    for i,c in zip(listofnames,comments):

            #print(c)
        #for j in comments:
            d = {
            "uid": "",
                            "name": "",
                            "alias_name": [],
                            "country": [],
                            "list_type": "Individual",
                            "last_updated": last_updated_string,
                            "individual_details": {
                            "date_of_birth": [],
                            },
                            "nns_status": "False",
                            "address": [
                            {
                            "country": "",
                            "complete_address": ""
                            }
                            ],
                            "relationship_details":{},
                            "sanction_details": {},
                            "documents": {
                            },
                            "comment": "",
                            "sanction_list": {

                            "sl_authority": "",

                            "sl_url": "https://fsin.gov.ru/criminal/",

                            "watch_list": "APAC Watchlists",

                            "sl_host_country": "Russia",

                            "sl_type": "Sanctions",

                            "sl_source": "Russian Federal Prison Authority Wanted List, Russia",

                            "sl_description": "List of the criminals wanted by Federal Penitentiary Service, Russia",

                            "list_id": "RUS_T30081"
                            }
            }

            try:
                if i[0]!="":
                    trans = langtranslation(i)
                    perfectname = transform_name(trans)
                    perfectname1 = alias_name(perfectname)
                    d["name"] = perfectname1[0]
                    rus = transform_name(i)

                    if c!="":
                        trnslatedcom = langtranslation(c)
                    d["comment"] = trnslatedcom
                    if trnslatedcom!="":
                        if ',' in trnslatedcom:
                            splitcom = trnslatedcom.split(',')
                            firstpart = splitcom[0]

                    d["alias_name"] = [perfectname] + [rus] + [firstpart]
                    print(d["alias_name"])
                    print(d["name"])

            except:
                pass


            try:
                d["uid"] = hashlib.sha256(
                    ((d["name"] + d["sanction_list"]["sl_source"]+d["sanction_list"]["sl_host_country"]).lower()).encode()).hexdigest()
            except:
                pass

            
            try:
                if d["name"]!="":
                    mylist.append(d)
                    #print(d)
            except:
                pass

with open('w1.json', 'w', encoding="utf-8") as file:
   json.dump(mylist, file, ensure_ascii=False, indent=4)