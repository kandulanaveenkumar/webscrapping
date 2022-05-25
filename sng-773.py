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

def alias_name(name):
    alias_list=[]
    rearrangedNamelist=name.split(' ')
    lastname= rearrangedNamelist.pop(-1)
    rearrangedNamelist=[lastname]+rearrangedNamelist
    alias_list.append(' '.join(rearrangedNamelist))
    return alias_list

last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

url = "https://www.fgjtam.gob.mx/mas-buscados/"
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

data_tag = requests.get(url)

htmlcontent = data_tag.content
#print(htmlcontent)

soup = BeautifulSoup(htmlcontent,'html.parser')

correct_links = soup.find("div" ,{"class":"row cols-same-height"}).find_all("a",{"class":"img-nota col-xs-5"},href = True)
#print(correct_links)

links_with_text = [a['href'] for a in correct_links if a.text]
#print(links_with_text)

mylist = []
for i in links_with_text:
    d = {
        "uid": "",
                        "name": "PETRONILO MORENO FLORES",
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

                        "sl_authority": "Attorney General's Office (Fiscalía General de Justicia), Mexico",

                        "sl_url": "https://www.fgjtam.gob.mx/mas-buscados/",

                        "watch_list": "South and Central America Watchlists",

                        "sl_host_country": "Mexico",

                        "sl_type": "Sanctions",

                        "sl_source": "Mexican Prosecutors General Offices Wanted List, Mexic",

                        "sl_description": "list of wanted criminals by Attorney General's Office (Fiscalía General de Justicia), Mexico",

                        "list_id": "MEX_T30106"
                        }
    }

    # try:
    #     res = requests.get(i)
    #     rsoup = BeautifulSoup(res.content, "html.parser")

    #     nam = soup.find("div",{"class":"row"}).find_all("h1")
    #     print(nam)
    #     mon = rsoup.find_all("a")[0].text
    #     #print(nam)

    # except:
    #         pass

    try:
        d["alias_name"] = alias_name(d["name"])

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
    

