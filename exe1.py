from platform import libc_ver
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import hashlib
import json
last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

url = "https://www.cftc.gov/LawRegulation/CEACases/index.htm"

data_tag = requests.get(url)

htmlcontent = data_tag.content
#print(htmlcontent)

soup = BeautifulSoup(htmlcontent,'html.parser')

def transform_name(name):
        name=name.replace("  ","")
        name=name.replace("\r","")
        name=name.replace("\t","")
        name=name.replace('\n','')
        name = name.replace("_", "")
        name = name.replace("Shri ", "")
        name = name.replace("SRI ", "")
        name = name.replace("Smt. ", "")
        name = name.replace("Dr. ", "")
        name = name.replace("Dr ", "")
        name = name.replace("Capt. ", "")
        name = name.replace("Sh. ", "")
        name = name.replace("Sri ","")
        name = name.replace("Smt ","")
        name = name.replace("Smti. ","")
        name = name.replace("Smti ","")
        name = name.replace("Mr. ","")
        name = name.replace("Sri. ","")
        name = name.replace("H.E. ","")
        name = name.replace("Sir ","")
        name = name.replace("Sh ","")
        name = name.replace("Shri. ","")
        name = name.replace("Smt. ","")
        name = name[0]
        name = name.strip()
 
        return name

def alias_name(name):
    alias_list=[]
    subname = name.split(' ')
    l = len(subname)
    if l>=3:
        name1 = subname[l-1] + " " + subname[0]
        name2 = subname[l-2] + " " + subname[0]
        alias_list.append(name1)
        alias_list.append(name2)
    if l==2:
        name1 = subname[1] + " " + subname[0]
        alias_list.append(transform_name(name1))
    return alias_list
# links_with_text = [a['href'] for a in soup.find_all('a', href=True) if a.text]
# print(links_with_text)

# for i in anchors:
#     list.append(i)

# print(list)

mylist=[]

for link in soup.find_all('a',title = True):
    data = link.get_text()
    data = data
    data = data.strip()
    d = {
            "uid": "",
                    "name": "",
                    "alias_name": [],
                    "country": [],
                    "list_type": "Individual",
                    "last_updated": last_updated_string,
                    "list_id": "ISR_T10011",
                    "individual_details": {
                    "date_of_birth": [],
                    "gender": ""
                    },
                    "nns_status": "False",
                    "address": [
                    {
                    "country": "",
                    "complete_address": ""
                    }
                    ],
                    "documents": {
                    "passport": "",
                    "SSN": ""
                    },
                    "comment": "null",
                    "sanction_list": {
                    "sl_authority": "",
                    "sl_url": "",
                    "watch_list": "EMEA Watchlists",
                    "sl_host_country": "",
                    "sl_type": "",
                    "sl_source": "",
                    "sl_description": ""

                    }
        }

    try:
        first_name = data
        print(first_name)
        if first_name!="":
            d['name']=first_name
            d['alias_name']=alias_name(d['name'])
    except:
        pass

    try:
        d["uid"] = hashlib.sha256(
            ((d["name"] + d["sanction_list"]["sl_type"]).lower()).encode()).hexdigest()
    except:
        pass

    try:
        mylist.append(d)
        print("k")
    except:
        pass


with open('w1.json', 'w', encoding="utf-8") as file:
    json.dump(mylist, file, ensure_ascii=False, indent=4)