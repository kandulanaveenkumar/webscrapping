import requests
from scrapinghelp import htmlhelper
from datetime import datetime
import hashlib
import json
last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

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
        name = name.replace(" REWARD OF Rs 10","")
        name = name.split(',')
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


if __name__=="__main__":

    url="https://www.sfc.hk/en/alert-list"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    res=requests.get(url,headers=headers)
    get_small_source = htmlhelper.returnformatedhtml(res.text)

    get_individuals = htmlhelper.collecturl(get_small_source,"<tr>","</tr>")
    #print(get_individuals)
    mylist = []
    myname = []

    for ele in get_individuals: 
        d = {

                            "uid": "",
                            "name": "",
                            "alias_name": [],
                            "country": [],
                            "list_type": "Individual",
                            "last_updated": last_updated_string,
                            "list_id": "JPN_T30041",
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
                            "complete_address": "",
                            "city":"",
                            "state":""
                            }
                            ],
                            "documents":{},
                            "relationship_details":{},
                            "comment": "",
                            "sanction_list": {
                                "sl_authority": "State Police of Massachusetts, USA",
                                "sl_url": "National Police Agency, Japan",
                                "watch_list": "APAC Watchlists",
                                "sl_host_country": "Japan",
                                "sl_type": "Sanctions",
                                "sl_source": "NPSC/NPA (Japan) - Terrorist List, Japan",
                                "sl_description": "List of the wanted suspects designated by the National Police Agency, Japan"
        }
                            }
        try:
                get_last_name = htmlhelper.returnvalue(ele, "<td>","</td>")
                print(get_last_name)
        except:
                print("hi")
                pass

        try:
                first_name = get_last_name[0]
                if first_name!="":
                    d['name']=transform_name(first_name)
                    d['alias_name']=alias_name(d['name'])
        except:
                pass

        try:
                d["uid"] = hashlib.sha256(
                        ((d["name"] + d["sanction_list"]["sl_source"]+d["sanction_list"]["sl_host_country"]).lower()).encode()).hexdigest()
        except:
                pass

        try:
                mylist.append(d)
                print("k")
        except:
                pass
    
    with open('w1.json', 'w', encoding="utf-8") as file:
        json.dump(mylist, file, ensure_ascii=False, indent=4)