#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

r=requests.get("https://kma.kkbox.com/charts/?terr=tw&lang=tc")
soup=BeautifulSoup(r.text,"html")
content=soup.select("script")[18].contents[0]
#===================================
n=content.split("\n")[2]
sam=n.split(" = ")[1].replace(";","")
jd=json.loads(sam)

print("=========新歌及時榜=========")
for i in range(len(jd["charts"]["newrelease"])):   
    song=jd["charts"]["newrelease"][i]["song_name"]
    artist=jd["charts"]["newrelease"][i]['artist_name']
    print("排名",i+1,song,'---',artist)

#作圖
plt.figure(figsize=(10,10))

h=[]
H = int(datetime.now().strftime('%H'))
for z in range(24):
    h.append(int(H)-24+z)

for i in range(len(jd['charts']["newrelease"])):
    ranklist=[]
    rank=[]
    for a in range(len(jd['charts']["newrelease"][i]["rankings"])):   
        rank.append(jd['charts']["newrelease"][i]["rankings"][a]["rank"])
    ranklist.append(rank)
    df=pd.DataFrame(ranklist,columns=h)
    p=plt.plot(df.T,'o--',label=i+1)
       
plt.xlabel("Hour")
plt.ylabel("Rank")
plt.legend()
plt.axis([H-24,H-1,40,0])
date=datetime.now().strftime('%Y/%m/%d %H:%M:%S')
plt.title(date)

print(p)
plt.savefig("新歌即時榜.png")    
#===================================    
n2=content.split("\n")[4]
sam2=n2.split(" = ")[1].replace(";","")
jd=json.loads(sam2)
chinesenewsong=[]
chineseone=[]

print("=========日榜_華語新歌=========")
for i in range(len(jd['newrelease_297']["data"])):
    song=jd['newrelease_297']["data"][i]["song_name"]
    artist=jd['newrelease_297']["data"][i]["artist_name"]
    print("排名",i+1,song,'---',artist)
    newsong=["排名{}".format(i+1),song,artist]
    chinesenewsong.append(newsong)


print("=========日榜_華語單曲=========")
for i in range(len(jd['song_297']["data"])):
    song=jd['song_297']["data"][i]["song_name"]
    artist=jd['song_297']["data"][i]["artist_name"]
    print("排名",i+1,song,'---',artist)
    onesong=["排名{}".format(i+1),song,artist]
    chineseone.append(onesong)
    
#===================================
n3=content.split("\n")[5]
sam3=n3.split(" = ")[1].replace(";","")
jd=json.loads(sam3)

print("=========週榜_華語新歌=========")
for i in range(len(jd['newrelease_297']["data"])):
    song=jd['newrelease_297']["data"][i]["song_name"]
    artist=jd['newrelease_297']["data"][i]["artist_name"]
    print("排名",i+1,song,'---',artist)

print("=========週榜_華語單曲=========")
for i in range(len(jd['song_297']["data"])):
    song=jd['song_297']["data"][i]["song_name"]
    artist=jd['song_297']["data"][i]["artist_name"]
    print("排名",i+1,song,'---',artist)

print("=========週榜_華語專輯=========")
for i in range(len(jd['album_297']["data"])):
    album=jd['album_297']["data"][i]["album_name"]
    artist=jd['album_297']["data"][i]["artist_name"]
    print("排名",i+1,album,'---',artist)

    
time=datetime.now().strftime('%m%d')    
jd=pd.DataFrame(chinesenewsong,columns=("排名","歌名","歌手"))
jd.to_excel("{}的華語新歌日榜.xlsx".format(time),index=False)
jd2=pd.DataFrame(chineseone,columns=("排名","歌名","歌手"))
jd2.to_excel("{}的華語單曲日榜.xlsx".format(time),index=False)


# In[ ]:




