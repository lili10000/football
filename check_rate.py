# encoding=utf8
import requests
import re
import time
from datetime import datetime
# from bs4 import BeautifulSoup
import json
import ctypes
# from html.parser import HTMLParser



# url = 'https://live.dszuqiu.com/ajax/score/data'
# req = requests.get(url)

# with open("tmp.txt", 'w') as f:
#     f.write(req.text)

mt = ""

class dataElement():
    def __init__(self, score = 0, rate = 0):
        self.score = score
        self.rate = rate

dataRecord = {}
def doCheck(rowData):
    try:
        jsonData = json.loads(rowData)
    except Exception as e:
        print("err:"+ repr(e)+" data:" + rowData)
        return ""
    
    dataArray = jsonData['rs']
    for oneData in dataArray:
        if ('host' in oneData) == False: 
            continue
        if ('events_graph' in oneData) == False:
            continue

        host = oneData['host']['n']
        guest = oneData['guest']['n']
        key = host + "_" + guest

        time = oneData['events_graph']['status']
        if int(time) > 80:
            if dataRecord.__contains__(key):
                dataRecord.pop(key)
            continue

        dataKey = 'rd'
        if (dataKey in oneData) == False :
            continue

        host_score = int(oneData[dataKey]['hg'])
        guest_score = int(oneData[dataKey]['gg'])
        score_sum = host_score + guest_score
        
        if ('f_ld' in oneData) == False :
            continue
        newRate = float(oneData['f_ld']['hdx'])
        newElement = dataElement(score_sum,newRate)

        if dataRecord.__contains__(key) == False:
            dataRecord[key] = newElement

        oldElement = dataRecord[key]
        
        conditionScore = bool(newElement.score == oldElement.score)
        conditionRate = bool(newElement.rate >= oldElement.rate + 0.5)
        if conditionScore and  conditionRate:
            nowTime = datetime.now().strftime('%H:%M:%S')
            msg = nowTime + " " + key + " new:" + newElement.rate +  " old:" + oldElement.rate
            print(msg)
            ctypes.windll.user32.MessageBoxA(0, msg.encode('gb2312'),u'赔率异常'.encode('gb2312'),0)
            
        dataRecord[key] = newElement
    if 'mt' in jsonData:
        mt = "?mt=" + jsonData['mt']
        return mt
# data=""
# with open("tmp.txt", 'r') as f:
#     data = f.read()
#     doCheck(data)


while(True):
    url = 'https://live.dszuqiu.com/ajax/score/data' + mt

    headers = {'accept':'application/json, text/javascript, */*; q=0.01',\
                'accept-encoding':'gzip, deflate',\
                'accept-language': 'zh-CN,zh;q=0.9', \
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }
    req = requests.get(url=url , headers=headers)
    if req.status_code == 200:
        mt = doCheck(req.text)
    elif req.status_code == 304:
        print("data not modify")

    nowTime = datetime.now().strftime('%H:%M:%S')
    print(nowTime," start check. url:",url)
    time.sleep(10)


