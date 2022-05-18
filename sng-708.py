import time
import json
from json import dump
import hashlib
import datetime
from datetime import datetime
import requests
last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


url = "https://www.mas.gov.sg/api/v1/ialsearch?json.nl=map&wt=json&sort=date_dt%20desc&q=*:*&rows=731&start=0"
headers = {"Content-Type": "application/json, text/plain, */*","Host" : "www.mas.gov.sg"}
resp = requests.get(url, headers= headers)
print(resp)
data = json.loads(resp.text)
num = data['response']['numFound']

mylist = []

for i in data['response']['docs']:
    d = {
        "uid": "",
                        "name": "",
                        "alias_name": [],
                        "country": [],
                        "list_type": "Entity",
                        "last_updated": last_updated_string,
                        "list_id": "SGP_E20249",
                        "nns_status": "False",
                        "address": [
                        {
                        "country": "",
                        "complete_address": ""
                        }
                        ],
                        "documents": {},
                        "comment": "",
                        "sanction_details":{},
                        "entity_details":{
                            "email":[],
                            "website":[]
                        },
                        "sanction_list": {
                        "sl_authority": "Monetary Authority of Singapore, Singapore",
                        "sl_url": "https://www.mas.gov.sg/investor-alert-list",
                        "watch_list": "APAC Watchlists",
                        "sl_host_country": "Singapore",
                        "sl_type": "Sanctions",
                        "sl_source": "Monetary Authority of Singapore investor Alert List, Singapore",
                        "sl_description": "list of unregulated entites who have been wrongly perceived as being licensed or regulated by Monetary Authority of Singapore, Singapore"
                        }
    }
    try:
        name = i['unregulatedpersons_t'][0]
        if name!="":
            d["name"]=name

    except:
        pass

    try:
        for j in i['alternativename_t']:
            if j.strip()!="":
                d["alias_name"].append(j)

    except:
        pass

    try:
            d["uid"] = hashlib.sha256(
                ((d["name"] + i['id'] + d["sanction_list"]["sl_source"]+d["sanction_list"]["sl_host_country"]).lower()).encode()).hexdigest()
    except:
            pass

    try:
        remail = i['email_s'].split("\n")
        email = [k for k in remail if k.strip()]
        d["entity_details"]["email"] = email

        rweb = i['website_s'].split("\n")
        web = [k for k in rweb if k.strip()]
        d["entity_details"]["website"] = web

    except:
        pass

    try:
        address  = i['address_s']
        if address!="":
            d["address"][0]["complete_address"] = address

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
