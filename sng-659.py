import pandas as pd
from datetime import datetime
import hashlib
import json
import csv
last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def alias_name(name):
    alias_list=[]
    rearrangedNamelist=name.split(' ')
    lastname= rearrangedNamelist.pop(-1)
    rearrangedNamelist=[lastname]+rearrangedNamelist
    alias_list.append(' '.join(rearrangedNamelist))
    return alias_list

mylist= []
file = open("/content/PFSA (Poland) Penalties List (1).csv")
csvreader = csv.reader(file)

for row in csvreader:
    if row[2] == "Individual":
        d = {
                "uid": "",
                        "name": "",
                        "alias_name": [],
                        "country": [],
                        "list_type": "Individual",
                        "last_updated": last_updated_string,
                        "list_id": "POL_E20292",
                        "individual_details": {
                        "date_of_birth": [],
                        "deceased_date":"",
                        "gender": ""
                        },
                        "designation":[],
                        "nns_status": "False",
                        "address": [
                        {
                        "country": "",
                        "complete_address": ""
                        }
                        ],
                        "relationship_details":{},
                        "sanction_details": {
                            "penalty_amount":"",
                            "date_decision":""
                        },
                        "documents": {
                        },
                        "comment": "",
                        "sanction_list": {
                        "sl_authority": "The Polish Financial Supervision Authority (Komisja Nadzoru Finansowego), Poland",
                        "sl_url": "https://cdn.occrp.org/projects/suisse-secrets-interactive/en/",
                        "watch_list": "European Watchlists",
                        "sl_host_country": "Poland",
                        "sl_type": "Sanctions",
                        "sl_source": "PFSA Public Penalty, Poland",
                        "sl_description": "The Polish Financial Supervision Authority (Komisja Nadzoru Finansowego), Poland"

                        }
            }
        try:
            first_name = row[1]
            print(first_name)
            if first_name!="":
                d['name']=first_name

        except:
            pass

        try:
            alias = alias_name(d["name"])
            print("++++++",alias)
            alias2 = row[3]
            allalias = alias+[alias2]
            print(allalias)
            if alias!="":
                d["alias_name"]=allalias

        except:
            pass

        # try:
        #       dob = row[10]
        #       print(dob)
        #       if dob!="":
        #         d["individual_details"]["date_of_birth"].append(dob)
        # except:
        #       pass

        # try:
        #       death = row[11]
        #       if death!="":
        #         d["individual_details"]["deceased_date"]=death
        
        # except:
        #       pass

        # try:
        #       coun = row[9]
        #       if coun!="":
        #         d["country"].append(coun)
        
        # except:
        #         pass
        
        # try:
        #       gen = row[5]
        #       if gen!="":
        #         d["individual_details"]["gender"] = gen

        # except:
        #       pass

        try:
            comm = row[4]
            print(comm)
            if comm!="":
                d["comment"]=comm

        except:
            pass


        # try:
        #       urls1=row[21]
        #       urls2=row[22]
        #       urls3=row[23]
        #       all_urls = urls1+" "+urls2+" "+urls3
        #       print(all_urls)
        #       if all_urls!="":
        #         d["sanction_list"]["other_urls"].append(all_urls)

        # except:
        #           pass
        try:
            pen = row[5]
            if pen!="":
                d["sanction_details"]["penalty_amount"]=pen
        except:
            pass

        try:
            dates = row[6]
            if dates!="":
                d["sanction_details"]["date_decision"]=dates

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
                print("k")

        except:
            pass
    else:
        d = {
                "uid": "",
                        "name": "",
                        "alias_name": [],
                        "country": [],
                        "list_type": "Entity",
                        "last_updated": last_updated_string,
                        "list_id": "POL_E20292",
                        "nns_status": "False",
                        "address": [
                        {
                        "country": "",
                        "complete_address": ""
                        }
                        ],
                        "entity_details" : {
                            "Registrations Details" : "",
                            "Website":[]
                        },
                        "sanction_Details": {
                            "penalty_amount":"",
                            "date_decision":""
                        },
                        "documents": {},
                        "comment": "",
                        "sanction_list": {
                        "sl_authority": "The Polish Financial Supervision Authority (Komisja Nadzoru Finansowego), Poland",
                        "sl_url": "https://cdn.occrp.org/projects/suisse-secrets-interactive/en/",
                        "watch_list": "European Watchlists",
                        "sl_host_country": "Poland",
                        "sl_type": "Sanctions",
                        "sl_source": "PFSA Public Penalty, Poland",
                        "sl_description": "The Polish Financial Supervision Authority (Komisja Nadzoru Finansowego), Poland"
                        }
            }
        try:
            first_name = row[1]
            print(first_name)
            if first_name!="":
                d['name']=first_name

        except:
            pass

        try:
            alias2 = row[3]
            if alias2!="":
                d["alias_name"]=[alias2]

        except:
            pass

        # try:
        #       dob = row[10]
        #       print(dob)
        #       if dob!="":
        #         d["individual_details"]["date_of_birth"].append(dob)
        # except:
        #       pass

        # try:
        #       death = row[11]
        #       if death!="":
        #         d["individual_details"]["deceased_date"]=death
        
        # except:
        #       pass

        # try:
        #       coun = row[9]
        #       if coun!="":
        #         d["country"].append(coun)
        
        # except:
        #         pass
        
        # try:
        #       gen = row[5]
        #       if gen!="":
        #         d["individual_details"]["gender"] = gen

        # except:
        #       pass

        try:
            comm = row[4]
            print(comm)
            if comm!="":
                d["comment"]=comm

        except:
            pass

        # try:
        #       sancdet = row[12]
        #       if desig!="":
        #         d["individual_details"]["designation"].append(desig)

        # except:
        #         pass

        # try:
        #       urls1=row[21]
        #       urls2=row[22]
        #       urls3=row[23]
        #       all_urls = urls1+" "+urls2+" "+urls3
        #       print(all_urls)
        #       if all_urls!="":
        #         d["sanction_list"]["other_urls"].append(all_urls)

        # except:
        #           pass

        try:
            pen = row[5]
            if pen!="":
                d["sanction_details"]["penalty_amount"]=pen
        except:
            pass

        try:
            dates = row[6]
            if dates!="":
                d["sanction_details"]["date_deccision"]=dates

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
                print("k")

        except:
            pass
with open('w1.json', 'w', encoding="utf-8") as file:
    json.dump(mylist, file, ensure_ascii=False, indent=4)