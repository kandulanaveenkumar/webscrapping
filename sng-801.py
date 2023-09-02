from audioop import alaw2lin
from cgi import print_directory
from numpy import NAN
import pandas as pd
from datetime import date, datetime
import hashlib
import json

last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def alias_name(name):
    alias_list=[]
    rearrangedNamelist=name.split(' ')
    lastname= rearrangedNamelist.pop(-1)
    rearrangedNamelist=[lastname] + rearrangedNamelist
    alias_list.append(' '.join(rearrangedNamelist))
    return alias_list 


file = pd.read_excel("C:\\Users\\Personal\\Downloads\\list-of-clients-of-the-defaulter-members---apportioned-amount-not-claimed82ba104757fb64e3bdfdff00007acb35.xlsx")
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
                    "sanction_details":{},
                    "documents": {},
                    "comment": "",
                    "sanction_list": {

                        "sl_authority": "Multi Commodity Exchange of India Ltd, India",

                        "sl_url": "https://www.mcxindia.com/Investor-Services/defaulters/list-of-clients-of-the-defaulter-members-apportioned-amount-not-claimed",

                        "watch_list": "India Watchlists",

                        "sl_host_country": "India",

                        "sl_type": "Sanctions",

                        "sl_source": "MCX clients of the Defaulter Members, India",

                        "sl_description": "list of defaulting Members by Multi Commodity Exchange of India Ltd, India",

                        "list_id": "IND_E20316"
                    }
        }

    try:
        names = i[1]
        if names!="":
            d["name"] = names
            d["alias_name"] = alias_name(d["name"])

    except:
        pass

    try:
        relations = i[2]
        if relations!="":
            d["relationship_details"]["Associate"] = relations

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
    except:
        pass
    


with open('w1.json', 'w', encoding="utf-8") as file:
    json.dump(mylist, file, ensure_ascii=False, indent=4,default=str)

