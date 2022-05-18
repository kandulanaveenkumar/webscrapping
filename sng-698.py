from email import header
from platform import libc_ver
from random import betavariate
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import hashlib
import json
from lxml import etree
from deep_translator import GoogleTranslator

last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

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

def transform_name(name):
        name=name.replace("  ","")
        name=name.replace("\r","")
        name=name.replace("\t","")
        name=name.replace('\n','')
        name = name.replace("<p>","")
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

def returnformatedhtml(content:str):
    result = re.sub("\\s+", " ", content).replace(" \"", "\"").replace("\" >", "\">").replace(" >", ">").replace("> <","><").replace("\" />", "\"/>").replace(" =", "=").replace("= ", "=")
    return result

def formatstring(content : str):
    return re.sub("<(.|\n)*?>", " ", content).strip()



def returnvalue(content: str, start: str, end: str):
    result = ""
    pattern = re.compile(re.escape(start) + "(.*?)" + re.escape(end))
    match = pattern.search(content)
    if match:
            result = match.groups()[0].strip()
    return result


def collecturl(content:str, start: str, end: str):
    result = []
    pattern = re.compile(re.escape(start) + "(.*?)" + re.escape(end))
    match = pattern.findall(content)
    if match:
        result = [sub.strip() for sub in match]
    return result


url = "https://www.nationalsecurity.gov.au/what-australia-is-doing/terrorist-organisations/listed-terrorist-organisations"

res = requests.get(url)

htmlcontent = res.content

soup = BeautifulSoup(htmlcontent,'html.parser')

get_small_source = returnformatedhtml(res.text)

get_individuals = collecturl(get_small_source,"<tr>","</tr>")
#print(get_individuals)
mylist = []
myname = []

for ele in get_individuals:
    d = {
        "uid": "",
                        "name": "",
                        "alias_name": [],
                        "country": [],
                        "list_type": "Entity",
                        "last_updated": last_updated_string,
                        "list_id": "",
                        "nns_status": "False",
                        "address": [
                        {
                        "country": "",
                        "complete_address": ""
                        }
                        ],
                        "documents": {},
                        "comment": "",
                        "sanction_details":{
                            "listed_on":""
                        },
                        "entity_details":{},
                        "sanction_list": {
                        "sl_authority": "Australian National Security, Australia",
                        "sl_url": "https://www.nationalsecurity.gov.au/what-australia-is-doing/terrorist-organisations/listed-terrorist-organisations",
                        "watch_list": "APAC Watchlists",
                        "sl_host_country": "Australia",
                        "sl_type": "Sanctions",
                        "sl_source": "Australian National Security Listed Terrorist Organization, Australia",
                        "sl_description": "list of terrorist organisations by Australian National Security, Australia"
                        }
    }

    try:
        #print(date)
        rsoup = BeautifulSoup(ele,"lxml")
        dateb = rsoup.find_all("td")[1].text
        print(dateb)
        name = rsoup.find("a").text
        #print(name)
        d["sanction_details"]["listed_on"]=dateb
        d["name"] = name


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
        #print(d)
    except:
        pass

with open('w1.json', 'w', encoding="utf-8") as file:
   json.dump(mylist, file, ensure_ascii=False, indent=4)