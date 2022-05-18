from email import header
from platform import libc_ver
import requests
from bs4 import BeautifulSoup
import re
from scrapinghelp import htmlhelper
from datetime import datetime
import hashlib
import json
from deep_translator import GoogleTranslator
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
        name = name.replace("(Chinese name only)","")
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

def langtranslation(to_translate):
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
    except:
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
        except:
            print(f">>>Translartion Bug : {to_translate}")
            translated = to_translate  
    return translated

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

url = "https://www.sfc.hk/en/alert-list"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

data_tag = requests.get(url,headers=headers)

htmlcontent = data_tag.content
#print(htmlcontent)

soup = BeautifulSoup(htmlcontent,'html.parser')
#print(soup.prettify)
correct_links = soup.find("tbody" ,{"id":"alert-list-append-here"}).find_all("a",href=True)

links_with_text = [a['href'] for a in correct_links if a.text]
#print(links_with_text)

#href_tags = soup.find_all(href=True)
#print(href_tags)


mylist = []
for i in links_with_text:
    if i == '#' or i == '###':
        continue
    url= i
    print(i) 

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    res=requests.get(url,headers=headers)
    
    get_small_source = htmlhelper.returnformatedhtml(res.text)

    get_individuals = htmlhelper.collecturl(get_small_source,"<table>","</table>")
    #print(get_individuals)

    for ele in get_individuals:

        source_data = htmlhelper.collecturl(ele,"<tbody>","</tbody>")
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

            "sl_authority": "Securities and Futures Commission, Hong Kong",

            "sl_url": "https://www.sfc.hk/en/alert-list",
            
            "watch_list": "APAC Watchlists",

            "sl_host_country": "Hong Kong",

            "sl_type": "Sanctions",

            "sl_source": "Securities & Futures Commission (HK) Enforcement Actions Alert List, Hong Kong",

            "sl_description": "The Alert List is a list of entities which have come to the attention of the SFC because they are unlicensed in Hong Kong and are believed to be, or to have been, targeting Hong Kong investors or claim to have an association with Hong Kong"
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
                        if not isEnglish(first_name):
                            first_name = langtranslation(first_name)
                        d['name']=transform_name(first_name)
                #     d['alias_name']=alias_name(d['name'])
                except:
                    pass

                # try:
                #     Com = htmlhelper.collecturl(go, "<div class=\"desciptiveText\" itemprop=\"bodyText\" itemtype=\"text\">","</div>")
                #     print("+++",Com)
                #     d["comment"] = Com

                # except:
                #     pass
                
                # try:
                #     designation = get_last_name[7]
                #     if first_name!="":
                #         d['designation']= designation
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

                    else:
                        samp_adr = {}
                        samp_adr["complete_address"] = address
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



# mylist = []
# texts = soup.find_all('a')
# for text in texts:
#     name = text.get_text()
#     d = {
#                     "uid": "",
#                     "name": "",
#                     "alias_name": [],
#                     "country": [],
#                     "list_type": "Entity",
#                     "last_updated": last_updated_string,
#                     "list_id": "HKG_E20291",
#                     "nns_status": "False",
#                     "address": [
#                     {
#                     "country": "United kingdom",
#                     "complete_address": "",
#                     }
#                     ],
#                     "entity_details" : {
#                         "Registrations Details" : ""
#                     },
#                     "documents": {},
#                     "comment": "",
#                     "sanction_list": {

#             "sl_authority": "",

#             "sl_url": "https://www.sfc.hk/en/alert-list",
            
#             "watch_list": "APAC Watchlists",

#             "sl_host_country": "",

#             "sl_type": "Sanctions",

#             "sl_source": "",

#             "sl_description": ""
#                     }
#     }
#     try:
#         if name!= "":
#             d["name"] = name
#     except:
#         pass

#     try:
#             d["uid"] = hashlib.sha256(
#                     ((d["name"] + d["sanction_list"]["sl_source"]+d["sanction_list"]["sl_host_country"]).lower()).encode()).hexdigest()
#     except:
#             pass

#     try:
#             mylist.append(d)
#             print("k")
#     except:
#             pass

# with open('w1.json', 'w', encoding="utf-8") as file:
#         json.dump(mylist, file, ensure_ascii=False, indent=4)