#!/usr/bin/env python
# coding: utf-8

# In[11]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

r=requests.get("https://www.leagueoflegends.com/en-us/champions/?_gl=1*34nf3u*_ga*Nzc3MjA5MTA2LjE2NTExMzIyMzY.*_ga_FXBJE5DEDD*MTY1MTEzMjIzNS4xLjEuMTY1MTEzMjMzMy4yNg..")
soup=BeautifulSoup(r.text,"html")
t=soup.select(".style__Text-sc-n3ovyt-3") #英文名字
#建立空list
nick=[]
name=[]
job=[]
intro=[]
passiveskill=[]
skill=[]
cos=[]
nameerror=[]


for i in range(len(t)):
    n=t[i].text
    punct=".' "
    for character in punct:
        n=n.replace(character,"")
    url="https://www.leagueoflegends.com/zh-tw/champions/{}".format(n)
    print(url)
    res=requests.get(url)
    soup2=BeautifulSoup(res.text,"html")
    
    try:     #測試網址有無錯誤(用能不能抓到最基本的名字測試)
        soup2.find_all(attrs={"data-testid": "overview:title"})[0].text
    except:
        print(n,"有誤")
        nameerror.append(n)
        continue
    else:
        print(soup2.find_all(attrs={"data-testid": "overview:title"})[0].text)
        nick.append(soup2.find_all(attrs={"data-testid": "overview:subtitle"})[0].text) #稱號
        name.append(soup2.find_all(attrs={"data-testid": "overview:title"})[0].text) #名字
        job.append(soup2.find_all(attrs={"data-testid": "overview:role"})[0].text) #職業
        intro.append(soup2.find_all(attrs={"data-testid": "overview:description"})[0].text) #介紹
        passiveskill.append(soup2.find_all(attrs={"data-testid": "abilities:name-0"})[0].text) #被動技能
    
    sample=str(soup2.select("script")[3]) 
    temskill=[]
    temcos=[]
    
    #舊版技能抓取
    '''
    for a in range(sample.count(",description:")-1):   #技能
        f1=sample.split(",description:")[a]
        remo=f1.split(",")[-1]
        sam=remo.replace("name:","")
        ok=sam.replace("\\u002"," ")
        temskill.append(ok)    #先把四個技能放在一起
    skill.append(temskill)     #再加進技能list 
    '''
    
    #新版技能抓取
    a = 1
    while True:
        abilities_name_count = "abilities:name-{}".format(a)
        try:
            skill_name = soup2.find_all(attrs={"data-testid": abilities_name_count })[0].text
        except:
            break
        else:
            temskill.append(skill_name)
            a = a+1
    skill.append(temskill)
    
    #舊版外觀抓取
    '''
    for b in range(1,sample.count(",chromas:")):    #外觀
        f1=sample.split(",chromas:")[b]
        remo=f1.split(",")[-1]
        sam=remo.replace("name:","")  #移除開頭的name:
        ok=sam.replace("\\u002"," ")
        temcos.append(ok)    #先把服裝放在一起
    cos.append(temcos)   #再加進服裝list
    '''
    
    #新版技能抓取
    b = 0
    while True:
        skin_name_count = "skins:button-{}".format(b)
        try:
            skin_name = soup2.find_all(attrs={"data-testid": skin_name_count })[0].text
        except:
            print("hi")
            break
        else:
            temcos.append(skin_name)
            b = b + 1
    cos.append(temcos)
    
    #time.sleep(random.randint(6,11))

    print("OK!")


print(nameerror)   #發生錯誤，無法讀取網站的角色
hi=pd.DataFrame(zip(nick,name,job,intro,passiveskill,skill,cos),columns=("英雄稱號","名字","角色定位","角色介紹","被動技能","技能","特殊外觀"))
hi.to_excel("LOL.xlsx")

df = pd.read_excel("LOL.xlsx")    #算出每個職業各有多少人
p=pd.DataFrame(df['角色定位'].value_counts())
print(p)


# In[9]:





# In[ ]:





# In[ ]:




