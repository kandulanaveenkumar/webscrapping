from audioop import alaw2lin
from cgi import print_directory
from cmath import nan
from numpy import NAN
import pandas as pd
from datetime import datetime
import hashlib
import json
import math

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

def transform_name(name):
        name=name.replace("  ","")
        name=name.replace("\r","")
        name=name.replace("\t","")
        name=name.replace('\n','')
        name = name.replace("_", "")
        name = name.replace("Mr. ","")
        name = name.replace("Mrs ","")
        name = name.split(',')
        name = name[0]
        name = name.strip()
 
        return name

def alias_name(name):
    alias_list=[]
    rearrangedNamelist=name.split(' ')
    lastname= rearrangedNamelist.pop(-1)
    rearrangedNamelist=[lastname] + rearrangedNamelist
    alias_list.append(' '.join(rearrangedNamelist))
    return alias_list 

file = pd.read_excel("C:\\Users\\Personal\\Downloads\\prs_ra_others.xls")
# lol = file.sheet_names
data = file.values.tolist()
#print(data)
mylist=[]
temp=1

for i in data:
    if not (type(i[2])==str and ("Limited" in i[2] or "pvt" in i[2] or "Pvt" in i[2] or "Ltd" in i[2])):
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
                        "sanction_details":{
                            "Nse_Circular_no":"",
                            "date_of_Nse_circular":""
                        },
                        "documents": {
                            "PAN":[],
                            "DIN":[]
                        },
                        "comment": "",
                        "sanction_list": {

                        "sl_authority": "National Stock Exchange of India Limited, India",

                        "sl_url": "https://www.nseindia.com/regulations/member-sebi-debarred-entities",

                        "watch_list": "India Watchlists",

                        "sl_host_country": "India",

                        "sl_type": "Sanctions",

                        "sl_source": "NSE Debarred Entities, India",

                        "sl_description": "list of Debarred Entities by National Stock Exchange of India Limited, India",

                        "list_id": "IND_E20313"
                        }
            }
        try:
            names = i[2]
            first_name = transform_name(names)
            #print(alias2)

            if len(first_name)!="":
                d['name']=first_name
                d['alias_name']=alias_name(d['name'])
        except:
            pass

        try:
            din = i[5]
            print(din)
            if din:
                if "revoked" not in din and "Not Available" not in din:
                    d["documents"]["DIN"].append(din)

        except:
            pass

    elif type(i[2])!= float:
        d = {
            "uid": "",
                    "name": "",
                    "alias_name": [],
                    "country": [],
                    "list_type": "Entity",
                    "last_updated": last_updated_string,
                    "nns_status": "False",
                    "address": [
                    {
                    "country": "",
                    "complete_address": ""
                    }
                    ],
                    "entity_details": {},
                    "sanction_details":{
                        "Nse_Circular_no":"",
                        "date_of_Nse_circular":""
                    },
                    "documents": {
                        "PAN":[],
                        "DIN":[]
                    },
                    "comment": "",
                    "sanction_list": {

                        "sl_authority": "National Stock Exchange of India Limited, India",

                        "sl_url": "https://www.nseindia.com/regulations/member-sebi-debarred-entities",

                        "watch_list": "India Watchlists",

                        "sl_host_country": "India",

                        "sl_type": "Sanctions",

                        "sl_source": "NSE Debarred Entities, India",

                        "sl_description": "list of Debarred Entities by National Stock Exchange of India Limited, India",

                        "list_id": "IND_E20313"
                        }

                }

        try:
            first_name = i[2]
            #print(alias2)
            if len(first_name)!="":
                d['name']=first_name
        except:
            pass
    
    try:
        pan=i[3]
        #print(pan)
        if type(pan)!= float:
            d["documents"]["PAN"].append(pan)

    except:
        pass

    try:
        din =i[5]
        if not (type(din)==float):
            d["documents"]["DIN"].append(din,temp)
            temp+=1
        
    except:
        pass

    try:
        nse = i[6]
        if type(nse)!=float:
            d["sanction_details"]["Nse_Circular_no"] = nse

        nseno = i[7]
        if type(nseno)!=float:
            d["sanction_details"]["date_of_Nse_circular"] = nseno

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
