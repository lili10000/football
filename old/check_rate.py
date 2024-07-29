# encoding=utf8
import requests
import re
import time
import threading
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
    def __init__(self, score = 0, rate = 0, name="", matchTime=0, notify=False):
        self.score = score
        self.rate = rate
        self.name = name
        self.time = matchTime
        self.notify = notify
        self.updata = int(time.time())

dataRecord = {}

def notifyMsg(msg):
    # ctypes.windll.user32.MessageBoxA(0, msg.encode('gb2312'),u'赔率异常'.encode('gb2312'),0)



def doCheck(rowData):
    try:
        jsonData = json.loads(rowData)
    except Exception as e:
        print("err:"+ repr(e)+" data:" + rowData)
        return ""
    
    dataArray = jsonData['rs']
    for oneData in dataArray:
        if ('id' in oneData) == False: 
            continue
        key = oneData['id']

        name = ""
        if ('host' in oneData): 
            host = oneData['host']['n']
            guest = oneData['guest']['n']
            name = host + " vs " + guest

        score_sum = -1
        newRate = 0
        time = 0
        notify = False
        if dataRecord.__contains__(key):
            name = dataRecord[key].name
            score_sum = dataRecord[key].score
            newRate = dataRecord[key].rate
            time = dataRecord[key].time
            notify = dataRecord[key].notify

        if ('events_graph' in oneData):
            time = int(oneData['events_graph']['status'])

        dataKey = 'rd'
        if (dataKey in oneData):
            host_score = int(oneData[dataKey]['hg'])
            guest_score = int(oneData[dataKey]['gg'])
            score_sum = host_score + guest_score
        
        rateLow = False
        LowInfo = ""
        LowValue = 1.68
        if ('f_ld' in oneData) :
            rateTmp = oneData['f_ld']['hdx']
            if rateTmp != None:
                newRate = float(oneData['f_ld']['hdx'])

            rateTmp = oneData['f_ld']['hdxsp']
            if rateTmp != None and float(rateTmp) < LowValue:
                rateLow = True
                LowInfo = " 主队赔率:" +rateTmp
            rateTmp = oneData['f_ld']['gdxsp']
            if rateTmp != None and float(rateTmp) < LowValue:
                rateLow = True
                LowInfo = " 客队赔率:" +rateTmp

        newElement = dataElement(score_sum,newRate, name, time, notify)

        if dataRecord.__contains__(key) == False:
            dataRecord[key] = newElement
        oldElement = dataRecord[key]
        dataRecord[key] = newElement
        if time > 80:
            continue


        conditionScore = bool(newElement.score == oldElement.score)
        conditionRate = bool(newElement.rate >= oldElement.rate + 0.5)

        nowTime = datetime.now().strftime('%H:%M:%S')
        # print(nowTime+ "    " +  newElement.name + "    " + str(newElement.rate) + " vs " + str(oldElement.rate))
        msg = ""
        if conditionScore and  conditionRate:
            msg = nowTime + " " + newElement.name + " new:" + str(newElement.rate) +  " old:" + str(oldElement.rate)
        if rateLow:
            msg = nowTime + " " + newElement.name + " rate <" + str(LowValue)  + LowInfo
        if msg != "" and newElement.notify == False:
            print(msg)
            t =threading.Thread(target=notifyMsg,args=(msg,))
            t.start()
            newElement.notify = True
            dataRecord[key] = newElement

    if 'mt' in jsonData:
        mt = "?mt=" + jsonData['mt']
        return mt


index = 0
while(True):
    index += 1
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

    if index % 540 == 0:
        print("[+] start clear dataRecord")
        for key in dataRecord:
            oneData = dataRecord[key]
            now = int(time.time())
            if (now - oneData.updata) > 5400:
                dataRecord.pop(key)
                print("delete "+ key)
        print("[-] end clear dataRecord")

