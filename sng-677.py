from email import header
from platform import libc_ver
from random import betavariate
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

url = "https://www.sec.gov/litigation/admin/adminarchive/adminarc1995.shtml"

res = requests.get(url)

htmlcontent = res.content

soup = BeautifulSoup(htmlcontent,'html.parser')

get_small_source = htmlhelper.returnformatedhtml(res.text)

get_individuals = htmlhelper.collecturl(get_small_source,"<tr>","</tr>")
#print(get_individuals)
mylist = []
myname = []

for ele in get_individuals:
    d = {
        "Title" : "",
        "Source" : "www.mas.gov.sg",
        "publishedAt" : "",
        "URL" : "",
        "query" : "",
        "uid" : "",
        "Content" : ""
    }

    try:
        date = htmlhelper.collecturl(ele, "<td valign=top align=left>","</td>")
        print(date)
        rsoup = BeautifulSoup(ele,"lxml")
        linkt = rsoup.find("a",href=True).get("href")
        properlink = "https://www.sec.gov"+linkt
        #published = htmlhelper.collecturl(ele, "<TD nowrap>","</TD>")
        d["publishedAt"] = date[1]
        d["URL"] = properlink
        d["Content"] = "FOR MORE INFORMATION:"+properlink
        #text = htmlhelper.collecturl(ele, "<td>","</td>")
        title = date[2]
        if "<BR>" in title:
            splittedtitle = title.split("<BR>")
            #print(splittedtitle)
            d["Title"] = transform_name(splittedtitle[0])

        else:
            d["Title"] = transform_name(title)

    except:
        pass

    try:
        d["uid"] = hashlib.sha256(
            ((d["Title"] +d["publishedAt"]+"The U.S. Securities and Exchange Commission Administrative Proceedings, USA").lower()).encode()).hexdigest()

    except:
        pass

    try:
        mylist.append(d)
        #print(d)
    except:
        pass

with open('w1.json', 'w', encoding="utf-8") as file:
   json.dump(mylist, file, ensure_ascii=False, indent=4)




# from email import header
# from platform import libc_ver
# from random import betavariate
# import requests
# from bs4 import BeautifulSoup
# import re
# from scrapinghelp import htmlhelper
# from datetime import datetime
# import hashlib
# import json
# from deep_translator import GoogleTranslator
# last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

# def transform_name(name):
#         name=name.replace("  ","")
#         name=name.replace("\r","")
#         name=name.replace("\t","")
#         name=name.replace('\n','')
#         name = name.replace("_", "")
#         name = name.replace("Shri ", "")
#         name = name.replace("SRI ", "")
#         name = name.replace("Smt. ", "")
#         name = name.replace("Dr. ", "")
#         name = name.replace("Dr ", "")
#         name = name.replace("Capt. ", "")
#         name = name.replace("Sh. ", "")
#         name = name.replace("Sri ","")
#         name = name.replace("Smt ","")
#         name = name.replace("Smti. ","")
#         name = name.replace("Smti ","")
#         name = name.replace("Mr. ","")
#         name = name.replace("Sri. ","")
#         name = name.replace("H.E. ","")
#         name = name.replace("Sir ","")
#         name = name.replace("Sh ","")
#         name = name.replace("Shri. ","")
#         name = name.replace("Smt. ","")
#         name = name.replace("(Chinese name only)","")
#         name = name.split(',')
#         name = name[0]
#         name = name.strip()
 
#         return name
 
# def alias_name(name):
#     alias_list=[]
#     subname = name.split(' ')
#     l = len(subname)
#     if l>=3:
#         name1 = subname[l-1] + " " + subname[0]
#         name2 = subname[l-2] + " " + subname[0]
#         alias_list.append(transform_name(name1))
#         alias_list.append(transform_name(name2))
#     if l==2:
#         name1 = subname[1] + " " + subname[0]
#         alias_list.append(transform_name(name1))
    
#     return alias_list

# url = "https://www.sec.gov/litigation/admin/adminarchive/adminarc2015.shtml"

# res = requests.get(url)

# htmlcontent = res.content

# soup = BeautifulSoup(htmlcontent,'html.parser')

# get_small_source = htmlhelper.returnformatedhtml(res.text)

# get_individuals = htmlhelper.collecturl(get_small_source,"<tr>","</tr>")
# #print(get_individuals)
# mylist = []
# myname = []


# for ele in get_individuals:
#     d = {
#         "Title" : "",
#         "Source" : "www.mas.gov.sg",
#         "publishedAt" : "",
#         "URL" : "",
#         "query" : "",
#         "uid" : "",
#         "Content" : ""
#     }

#     try:
#         date = htmlhelper.collecturl(ele, "<td>","</td>")
#         rsoup = BeautifulSoup(ele,"lxml")
#         linkt = rsoup.find("a",href=True).get("href")
#         properlink = "https://www.sec.gov"+linkt
#         d["publishedAt"] = date[1]
#         d["URL"] = properlink
#         d["Content"] = "FOR MORE INFORMATION:"+properlink
#         title = date[2]
#         if "<br>" in title:
#             splittedtitle = title.split("<br>")
#             #print(splittedtitle)
#             d["Title"] = splittedtitle[0]

#         else:
#             d["Title"] = title

#     except:
#         pass

#     try:
#         d["uid"] = hashlib.sha256(
#             ((d["Title"] +d["publishedAt"]+"The U.S. Securities and Exchange Commission Administrative Proceedings, USA").lower()).encode()).hexdigest()

#     except:
#         pass

#     try:
#         mylist.append(d)
#         #print(d)
#     except:
#         pass

# with open('w1.json', 'w', encoding="utf-8") as file:
#    json.dump(mylist, file, ensure_ascii=False, indent=4)