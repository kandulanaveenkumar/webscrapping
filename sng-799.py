from audioop import alaw2lin
from cgi import print_directory
from numpy import NAN
import pandas as pd
from datetime import date, datetime
import hashlib
import json

last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

# def alias_name(name):
#     alias_list=[]
#     subname = name.split(' ')
#     l = len(subname)
#     if l>=3:
#         name1 = subname[l-1] + " " + subname[0]
#         name2 = subname[l-2] + " " + subname[0]
#         alias_list.append(name1)
#         alias_list.append(name2)
#     if l==2:
#         name1 = subname[1] + " " + subname[0]
#         alias_list.append(name1)
#     return alias_list

def alias_name(name):
    alias_list=[]
    rearrangedNamelist=name.split(' ')
    lastname= rearrangedNamelist.pop(0)
    rearrangedNamelist=rearrangedNamelist + [lastname]
    alias_list.append(' '.join(rearrangedNamelist))
    return alias_list 

file = pd.read_excel("C:\\Users\\Personal\\Downloads\\Defaulting_Client_Database.xlsx")
# lol = file.sheet_names
data = file.values.tolist()
print(data)
mylist=[]

for i in data:
    if not (("Consultants" in i[1]) or ("pvt" in i[1]) or ("Pvt" in i[1])):
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
                        "relationship_details":{
                            "Associate":""
                        },
                        "sanction_details":{
                            "body":"",
                            "date_of_order":""
                        },
                        "documents": {
                            "PAN":[]
                        },
                        "comment": "null",
                        "sanction_list": {

                            "sl_authority": "National Stock Exchange of India Limited, India",

                            "sl_url": "https://www.nseindia.com/regulations/exchange-defaulting-clients",

                            "watch_list": "India Watchlists",

                            "sl_host_country": "India",

                            "sl_type": "Sanctions",

                            "sl_source": "NSE Defaulting Clients, India",

                            "sl_description": "list of Defaulting Clients by National Stock Exchange of India Limited, India",

                            "list_id": "IND_E20314"
                        }
            }
        try:
            first_name = i[1]
            #print(alias2)
            if len(first_name)!="":
                d['name']=first_name
                d["alias_name"] = alias_name(first_name)
        except:
            pass

    else:
        d = {"uid": "",
                    "name": "",
                    "alias_name": [],
                    "country": [],
                    "list_type": "Entity",
                    "last_updated": last_updated_string,
                    "list_id": "UKR_S10049",
                    "nns_status": "False",
                    "address": [
                    {
                    "country": "",
                    "complete_address": ""
                    }
                    ],
                    "entity_details": {},
                    "sanction_details":{
                            "body":"",
                            "date_of_order":""
                    },
                    "documents": {
                        "PAN":[]
                    },
                    "comment": "",
                    "sanction_list": {

                            "sl_authority": "National Stock Exchange of India Limited, India",

                            "sl_url": "https://www.nseindia.com/regulations/exchange-defaulting-clients",

                            "watch_list": "India Watchlists",

                            "sl_host_country": "Mexico",

                            "sl_type": "Sanctions",

                            "sl_source": "NSE Defaulting Clients, India",

                            "sl_description": "list of Defaulting Clients by National Stock Exchange of India Limited, India",

                            "list_id": "IND_E20314"
                        }

                }
    

        try:
            first_name = i[1]
            #print(alias2)
            if len(first_name)!="":
                d['name']=first_name
        except:
            pass

    try:
            pan=i[2]
            if pan!="":
                d["documents"]["PAN"].append(pan)

    except:
        pass


    try:
        relations = i[3]
        if relations!="":
            d["relationship_details"]["Associate"] = relations

    except:
        pass

    try:
        details = i[4]
        #print(details)
        if details!="":
            d["sanction_details"]["body"]=details

        dates = i[5]
        if dates!="":
            d["sanction_details"]["date_of_order"] = dates

    except:
        pass


    try:
        comm = i[6]
        if comm!="":
            d["comment"] = comm

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
