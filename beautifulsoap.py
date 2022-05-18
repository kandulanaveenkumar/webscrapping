from platform import libc_ver
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import hashlib
import json
last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

url = "https://www.devon-cornwall.police.uk/news/court-and-convicted/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
res=requests.get(url,headers=headers)


htmlcontent = res
print(htmlcontent)

soup = BeautifulSoup(htmlcontent,'html.parser')
print(soup.prettify)

anchors = (soup.find_all('h4'))
print(anchors)

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
    rearrangedNamelist=name.split(' ')
    lastname= rearrangedNamelist.pop(-1)
    rearrangedNamelist=[lastname]+rearrangedNamelist
    alias_list.append(' '.join(rearrangedNamelist))
    return alias_list
# links_with_text = [a['href'] for a in soup.find_all('a', href=True) if a.text]
# print(links_with_text)

# for i in anchors:
#     list.append(i)

# print(list)
#lists = []

# for link in soup.find_all('p'):
#     for links in link.find_all('a'):
#         data = link.get_text()
#         data = data
#         data = data.strip()
#         lists.append(data)
# print(lists)
lists=[]
for link in soup.find_all("div", {"class": "person__title"}):
    #for links in link.find_all():
        data = link.get_text()
        data = data
        #data = data.strip()
        lists.append(data)
print(lists)

mylist=[]

for i in lists:
    d = {
            "uid": "",
            "name": "",
        "alias_name": [
            ""
        ],
        "country": [
            "Pakistan"
        ],
        "list_type": "Individual",
        "last_updated": "2022-03-11T02:46:43",
        "list_id": "INT_S10048",
        "individual_details": {
            "date_of_birth": [
                "1933"
            ],
            "deceased_date": "",
            "gender": "Male"
        },
        "designation":[
            "Lieutenant General (Retired) - Pakistan Armed Force,Head - pakistan cricket Board,Chairman - water and power Development Authority of Pakistan"
        ],
        "nns_status": "False",
        "address": [
            {
                "country": "",
                "complete_address": ""
            }
        ],
        "relationship_details": {},
        "documents": {},
        "comment": "Khan is accused of misappropriating Rs176 million (US$ 2.9 million) while head of WAPDA. Max Account Balance isCHF 15,535,345",
        "sanction_list": {
            "sl_authority": "Credit Suisse",
            "sl_url": "https://cdn.occrp.org/projects/suisse-secrets-interactive/en/",
            "other_urls": [
                "https://cdn.occrp.org/projects/suisse-secrets-interactive/en/ https://cdn.occrp.org/projects/suisse-secrets-interactive/en/person/42/zahid-ali-akbar-khan/ https://www.occrp.org/en/suisse-secrets/pakistan-corruption-cash-concealed-in-credit-suisse-accounts"
            ],
            "sl_host_country": "Global Watchlists",
            "sl_type": "Sanctions",
            "sl_source": "Credit Suisse’s Most Problematic Account Holders - Global",
            "sl_description": "The Suisse Secrets data leak includes dozens of corrupt government officials, criminals, and alleged human rights abusers who have been clients of the Swiss banking giant."
        }
        }

    try:
        first_name = data
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