from audioop import alaw2lin
from cgi import print_directory
from cmath import nan
from smtplib import SMTPHeloError
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

file = pd.read_excel("C:\\Users\\Personal\\Downloads\\Defaulting Clients database_02052022.xls",sheet_name=3)
# lol = file.sheet_names
data = file.values.tolist()
#print(data)


mylist=[]

for i in data:
    if not (type(i[2])==str and ("Consultants" in i[2] or "pvt" in i[2] or "Pvt" in i[2] or "Ltd" in i[2])):
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
                                "PAN":[],
                                "BSE_notice_number":[]
                            },
                            "comment": "",
                            "sanction_list": {

                            "sl_authority": "National Commodity and Derivatives Exchange, India",

                            "sl_url": "https://ncdex.com/investor-awareness/defaulting-clients-database",

                            "watch_list": "India Watchlists",

                            "sl_host_country": "India",

                            "sl_type": "Sanctions",

                            "sl_source": "NCDX Defaulting Clients, India",

                            "sl_description": "list of defaulting Members by MultiNational Commodity and Derivatives Exchange, India",

                            "list_id": "IND_E20327"
                            }
                }

        try:
            names = i[3]
            if names!="":
                d["name"] = names
                d["alias_name"] = alias_name(names)

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
                        "PAN":[],
                        "BSE_notice_number":[]
                    },
                    "comment": "",
                    "sanction_list": {

                            "sl_authority": "National Commodity and Derivatives Exchange, India",

                            "sl_url": "https://ncdex.com/investor-awareness/defaulting-clients-database",

                            "watch_list": "India Watchlists",

                            "sl_host_country": "India",

                            "sl_type": "Sanctions",

                            "sl_source": "NCDX Defaulting Clients, India",

                            "sl_description": "list of defaulting Members by MultiNational Commodity and Derivatives Exchange, India",

                            "list_id": "IND_E20327"
                            }
        }
        try:
            names = i[3]
            if names!="":
                d["name"] = names
                d["alias_name"] = names

        except:
            pass


    try:
        pan = i[4]
        associate = i[5]
        body = i[6]
        comm = i[8]
        order = i[7]
        bseno = i[1]
        print(bseno)

        if bseno!="":
            d["documents"]["BSE_notice_number"].append(bseno)

        if pan!="":
            d["documents"]["PAN"].append(pan)

        if comm!="":
            d["comment"]=comm

        if order!="":
            d["sanction_details"]["date_of_order"] = order

        if associate!="":
            d["relationship_details"]["Associate"]= associate

        if body!="":
            d["sanction_details"]["body"] = body

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