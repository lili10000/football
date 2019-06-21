# encoding=utf8
import requests
import re
import time
import threading
from datetime import datetime
# from bs4 import BeautifulSoup
import json
# import ctypes
from db.mysql import sqlMgr
# from html.parser import HTMLParser



# url = 'https://live.dszuqiu.com/ajax/score/data'
# req = requests.get(url)

# with open("tmp.txt", 'w') as f:
#     f.write(req.text)

sql = sqlMgr('localhost', 'root', '861217', 'football')

mt = ""

class dataElement():
    def __init__(self, score = 0, rate = 0, name="", matchTime=-1, notify=False):
        self.score = score
        self.rate = rate
        self.name = name
        self.time = matchTime
        self.notify = notify
        self.updata = int(time.time())

dataRecord = {}

def notifyMsg(msg, key, newRate, oldRate, newElement):
    if newElement.time <= 0 and newRate*oldRate != 0 and newRate != oldRate:
        if not newElement.notify:
            print(msg)
            logInfo = "{}\n".format(msg)
            with open(r"buyPerDay.txt", 'a') as f:
                f.write(logInfo)
            newElement.notify = True
        sqlInfo = "'{}','{}','{}','{}','{}','{}'".format(key, newRate, oldRate, -1, int(time.time()), 0)
        sql.insert(sqlInfo, "k_checkRate", key)

    data = sql.queryByGameId("k_checkRate", key)
    if len(data) > 0:
        if newElement.time > 0:     
            sql.updateScore(key, newElement.score, "k_checkRate", int(time.time()))
        # newElement.notify = True
    
    return newElement
            
        



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
        time = -1
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
        # LowInfo = ""
        LowValue = 1.68
        if ('f_ld' in oneData) :
            dataTmp = oneData['f_ld']
            if not ('hdx' in dataTmp):
                continue

            rateTmp = dataTmp['hdx']
            if rateTmp != None:
                newRate = float(dataTmp['hdx'])


        newElement = dataElement(score_sum,newRate, name, time, notify)

        if dataRecord.__contains__(key) == False:
            dataRecord[key] = newElement
        oldElement = dataRecord[key]
        dataRecord[key] = newElement
        # if time > 0:
        #     continue

        conditionScore = bool(newElement.score == oldElement.score)
        # if "632146" in rowData:
        #     print(".")
        # conditionRate = bool(newElement.rate != oldElement.rate)

        nowTime = datetime.now().strftime('%H:%M:%S')
        # print(nowTime+ "    " +  newElement.name + "    " + str(newElement.rate) + " vs " + str(oldElement.rate))
        msg = ""
        if conditionScore:
            msg = nowTime + " " + newElement.name + " new:" + str(newElement.rate) +  " old:" + str(oldElement.rate)
            newElement = notifyMsg(msg, key, newElement.rate, oldElement.rate, newElement)
            dataRecord[key] = newElement

    if 'mt' in jsonData:
        try:
            mt = "?mt=" + str(jsonData['mt'])
        except:
            print(jsonData['mt'])
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
    
    try:
        req = requests.get(url=url , headers=headers)
        if req.status_code == 200:
            mt = doCheck(req.text)
        elif req.status_code == 304:
            print("data not modify")
    except:
        mt = ""
        print("connect err")

    nowTime = datetime.now().strftime('%H:%M:%S')
    # print(nowTime," start check. url:",url)
    # print(nowTime)
    if index % 10 == 0:
        print(".")

    time.sleep(10)

    if index % 540 == 0:
        print("[+] start clear dataRecord")
        keys = dataRecord.keys()
        for key in keys:
            oneData = dataRecord[key]
            now = int(time.time())
            if (now - oneData.updata) > 5400:
                dataRecord.pop(key)
                print("delete "+ key)
        print("[-] end clear dataRecord")

