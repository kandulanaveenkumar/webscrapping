from xml.etree.ElementTree import Comment
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

    url="https://www.sec.gov/litigation/admin.htm"

    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    res=requests.get(url)
    
    get_small_source = htmlhelper.returnformatedhtml(res.text)

    get_individuals = htmlhelper.collecturl(get_small_source,"<tbody>","</tbody>")
    #print(get_individuals)
    mylist = []

    for ele in get_individuals:

        source_data = htmlhelper.collecturl(ele,"<tr>","</tr>")
        print(source_data)
        for go in source_data:

                d = {
                    "uid": "",
                    "name": "",
                    "alias_name": [],
                    "country": [],
                    "list_type": "Entity",
                    "last_updated": last_updated_string,
                    "list_id": "HKG_E20291",
                    "nns_status": "False",
                    "address": [],
                    "entity_details" : {
                        "Registrations Details" : "",
                        "Website":[]
                    },
                    "documents": {},
                    "comment": "",
                    "sanction_list": {

            "sl_authority": "",

            "sl_url": "https://www.sfc.hk/en/alert-list",
            
            "watch_list": "APAC Watchlists",

            "sl_host_country": "",

            "sl_type": "Sanctions",

            "sl_source": "",

            "sl_description": ""
                    }
    }
                try:
                    get_last_name = htmlhelper.collecturl(go, "<td>","</td>")
                    print(get_last_name)
                    print("kj")
                except:
                    print("hi")
                    pass

                try:
                    first_name = get_last_name[1]
                    if first_name!="":
                        d['name']=transform_name(first_name)
                except:
                    pass

                # try:
                #     Com = htmlhelper.collecturl(go, "<div class=\"desciptiveText\" itemprop=\"bodyText\" itemtype=\"text\">","</div>")
                #     print("+++",Com)
                #     d["comment"] = Com

                # except:
                #     pass
                
                try:
                    address = get_last_name[5]
                    if "<br/>" in address:
                        splittedaddress = address.split("<br/>")
                        print(len(splittedaddress))
                        print("===",splittedaddress)
                        for i in splittedaddress:
                            if i.strip()!="":
                                samp_adr = {}
                                samp_adr["complete_address"] = i
                                samp_adr["country"] = ""
                                d["address"].append(samp_adr)
                except:
                    pass
                
                try:
                    com = get_last_name[9]
                    if com!="":
                        d["comment"]= com
                
                except:
                    pass

                try:
                    urlweb = get_last_name[7]
                    print("+++",urlweb)
                    if urlweb!="":
                        d["entity_details"]["Website"].append(urlweb)
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











