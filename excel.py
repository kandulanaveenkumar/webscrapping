from audioop import alaw2lin
from cgi import print_directory
from numpy import NAN
import pandas as pd
from datetime import datetime
import hashlib
import json

last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

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
        alias_list.append(name1)
    return alias_list

file = pd.read_excel("C:\\Users\\Personal\\Downloads\\shisantouketsu20220128.xls",sheet_name=23)
# lol = file.sheet_names
data = file.values.tolist()
print(data)

mylist=[]

for i in data:
    d = {
            "uid": "",
                    "name": "",
                    "alias_name": [],
                    "country": [],
                    "list_type": "Individual",
                    "last_updated": last_updated_string,
                    "list_id": "JPN_S10012",
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
                    "sl_authority": "Ministry of Finance, Japan",
                    "sl_url": "https://www.mof.go.jp/policy/international_policy/gaitame_kawase/gaitame/economic_sanctions/list.html",
                    "watch_list": "APAC Watchlists",
                    "sl_host_country": "Japan",
                    "sl_type": "Sanctions",
                    "sl_source": "Japan Ministry of Finance Sanctions List",
                    "sl_description": "List of Designated Terrorists by Ministry of Finance, Japan"

                    }
        }

    try:
        first_name = i[3]
        alias=i[2]
        alias2=i[4]
        #print(alias2)
        if len(first_name)!="":
            d['name']=first_name
            d['alias_name']=alias_name(d['name'])+[alias]+[alias2]
    except:
        pass

    # try:
    #     dob = i[6]
    #     if len(dob)!="":
    #         d["individual_details"]["date_of_birth"].append(dob)

    # except:
    #     pass

    try:
        country=i[10]
        if country!="" and country!="not clear":
            d["country"].append(country) 

    except:
        pass
    
    try:
        address=[i[20]]
        if address!="":
            d["address"][0]["complete_address"]=address[0]

    except:
        pass
    
    try:
        passn=i[20]
        print(passn)
        if passn!="":
            d["documents"]["passport"]=passn

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
            print("fiding--->",address)
            print("k")
    except:
        pass


with open('w1.json', 'w', encoding="utf-8") as file:
    json.dump(mylist, file, ensure_ascii=False, indent=4)
