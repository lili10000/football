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



class dataElement():
    def __init__(self, score = 0, rate = 0):
        self.score = score
        self.rate = rate

dataRecord = {}
def doCheck(data):
    jsonData = json.loads(data)
    dataArray = jsonData['rs']
    for oneData in dataArray:
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

# data=""
# with open("tmp.txt", 'r') as f:
#     data = f.read()
#     doCheck(data)


while(True):
    url = 'https://live.dszuqiu.com/ajax/score/data'
    req = requests.get(url)
    doCheck(req.text)
    nowTime = datetime.now().strftime('%H:%M:%S')
    print(nowTime," start check")
    time.sleep(10)


