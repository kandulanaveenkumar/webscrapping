import requests
from scrapinghelp import htmlhelper
from datetime import datetime
import hashlib
import json
last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

newlist = []
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
        name = name.replace("<strong>POST VACANT</strong>","")
        name = name.split(',')
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
        alias_list.append(transform_name(name1))
        alias_list.append(transform_name(name2))
    if l==2:
        name1 = subname[1] + " " + subname[0]
        alias_list.append(transform_name(name1))
    
    return alias_list


if __name__=="__main__":

    url="https://rajyasabha.nic.in/rsnew/rssorgchart/js.aspx"

    res=requests.get(url)

    get_small_source = htmlhelper.returnformatedhtml(res.text)

    get_details = htmlhelper.collecturl(get_small_source,"<table style=\"width: 226px\">","</table>")
    print(get_details)

    mylist = []

    for ele in get_details:

        source_data = htmlhelper.collecturl(ele, "<tr>", "</tr>")

        for go in source_data:
            

            if "Name of the Judge" not in go:

                d = {
                        "uid": "",
                        "name": "",
                        "alias_name": [],
                        "gender": "",
                        "date_of_birth": [],
                        "country": [
                            "India"
                        ],
                        "family-tree": {
                            "parent": "",
                            "sibling": "",
                            "children": "",
                            "spouse": ""
                        },
                        "designation": "",
                        "last_updated": "2021-09-22T19:25:40",
                        "address": [
                            {
                                "complete_address": "",
                                "state": "",
                                "city": "",
                                "country": "India"
                            }
                        ],
                        "nns_status": "False",
                        "organisation": "",
                        "documents": {},
                        "source": {
                            "host_country": "India",
                            "name": "Joint Secretaries-RAJYASABHA",
                            "description": "Joint Secretaries-RAJYASABHA",
                            "type": "PEP",
                            "url": "https://rajyasabha.nic.in/rsnew/rssorgchart/js.aspx"
                        },
                        "comment": ""
                }

                try:
                    get_name = htmlhelper.collecturl(go, "<span id=\"ctl00_ContentPlaceHolder1_GridView1_ctl13_Label1\" style=\"display:inline-block;\">","</span>")
                    print(get_name)

                except:
                    pass

                try:
                    first_name = get_name[0]
                    if first_name!="":
                        d['name']=transform_name(first_name)
                        d['alias_name']=alias_name(d['name'])
                except:
                    pass

                try:
                    designation = get_name[1]
                    if first_name!="":
                        d['individual_details']['Designation']= designation
                except:
                    pass

                try:
                    d["uid"] = hashlib.sha256(
                        ((d["name"] + d["source"]["type"]).lower()).encode()).hexdigest()
                except:
                    pass

                try:
                    mylist.append(d)
                    print("k")
                except:
                    pass


    with open('j1.json', 'w', encoding="utf-8") as file:
        json.dump(mylist, file, ensure_ascii=False, indent=4)

































    #print(res)

