# encoding=utf8
import requests
import re
import time
import threading
from datetime import datetime
import json
import ctypes




class dataElement():
    def __init__(self, score = 0, rate = 0, name="", matchTime=0, notify=False):
        self.score = score
        self.rate = rate
        self.name = name
        self.time = matchTime
        self.notify = notify
        self.updata = int(time.time())

def notifyMsg(msg):
    ctypes.windll.user32.MessageBoxA(0, msg.encode('gb2312'),u'赔率异常'.encode('gb2312'),0)

class dataCheck():
    def __init__(self):
        self.dataRecord = {}
        self.mt = ""
        self.lowValue = 1.68
        self.headers = {'accept':'application/json, text/javascript, */*; q=0.01',\
                'accept-encoding':'gzip, deflate',\
                'accept-language': 'zh-CN,zh;q=0.9', \
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }
        self.index = 0
        self.timeCmp = 80

    def startCheck(self):
        
        url = 'https://live.dszuqiu.com/ajax/score/data' + self.mt
        req = requests.get(url=url , headers=self.headers)
        if req.status_code == 200:
            self.doCheck(req.text)
        elif req.status_code == 304:
            print("data not modify")
        nowTime = datetime.now().strftime('%H:%M:%S')
        print(nowTime," start check. url:",url)

        self.index += 1
        if self.index % 540 == 0:
            print("[+] start clear dataRecord")
            for key in self.dataRecord:
                oneData = self.dataRecord[key]
                now = int(time.time())
                if (now - oneData.updata) > 5400:
                    self.dataRecord.pop(key)
                    print("delete "+ key)
            print("[-] end clear dataRecord")



    def getName(self, oneData, key):
        name = ""
        if ('host' in oneData): 
            host = oneData['host']['n']
            guest = oneData['guest']['n']
            name = host + " vs " + guest
        if self.dataRecord.__contains__(key):
            name = self.dataRecord[key].name
        return name

    def getScoreSum(self, oneData, key):
        score_sum = -1
        dataKey = 'rd'

        if self.dataRecord.__contains__(key):
            score_sum = self.dataRecord[key].score

        if (dataKey in oneData):
            host_score = int(oneData[dataKey]['hg'])
            guest_score = int(oneData[dataKey]['gg'])
            score_sum = host_score + guest_score
        return score_sum

    def getRate(self, oneData, key):
        newRate = 0     
        if self.dataRecord.__contains__(key):
            newRate = self.dataRecord[key].rate

        LowInfo = ""
        if ('f_ld' in oneData) :
            rateTmp = oneData['f_ld']['hdx']
            if rateTmp != None:
                newRate = float(oneData['f_ld']['hdx'])
        return newRate


    def checkLowRate(self,oneData, key):
        LowInfo = ""
        if ('f_ld' in oneData) :
            rateTmp = oneData['f_ld']['hdxsp']
            if rateTmp != None and float(rateTmp) < self.lowValue:
                LowInfo = " 主队赔率:" +rateTmp
            rateTmp = oneData['f_ld']['gdxsp']
            if rateTmp != None and float(rateTmp) < self.lowValue:
                LowInfo = " 客队赔率:" +rateTmp
        return LowInfo

    def getTime(self, oneData, key):
        timeNow = 0   
        if self.dataRecord.__contains__(key):
            timeNow = self.dataRecord[key].time
        if ('events_graph' in oneData):
            timeNow = int(oneData['events_graph']['status'])
        return timeNow

    def getNotify(self, oneData, key):
        notify = False   
        if self.dataRecord.__contains__(key):
            notify = self.dataRecord[key].notify
        return notify

    def getNotifyMsg(self, oneData, key, newElement):
        msg = ""
        if self.dataRecord.__contains__(key) == False:
            self.dataRecord[key] = newElement
        oldElement = self.dataRecord[key]
        self.dataRecord[key] = newElement
        if newElement.time >= self.timeCmp:
            return msg

        conditionScore = bool(newElement.score == oldElement.score)
        conditionRate = bool(newElement.rate >= oldElement.rate + 0.5)

        nowTime = datetime.now().strftime('%H:%M:%S')
        # print(nowTime+ "    " +  newElement.name + "    " + str(newElement.rate) + " vs " + str(oldElement.rate))
        
        if conditionScore and  conditionRate:
            msg = nowTime + " " + newElement.name + " new:" + str(newElement.rate) +  " old:" + str(oldElement.rate)
        
        LowInfo = self.checkLowRate(oneData, key)
        if LowInfo != "":
            msg = nowTime + " " + newElement.name + " rate <" + str(self.lowValue)  + LowInfo
        return msg

    def sendMsg(self, key, newElement, msg):
        if msg != "" and newElement.notify == False:
            print(msg)
            t =threading.Thread(target=notifyMsg,args=(msg,))
            t.start()
            newElement.notify = True
            self.dataRecord[key] = newElement

    def doCheck(self, rowData):
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
            name = self.getName(oneData, key)
            score_sum = self.getScoreSum(oneData, key)
            newRate = self.getRate(oneData, key)
            timeNow = self.getTime(oneData, key)
            notify = self.getNotify(oneData, key)

            newElement = dataElement(score_sum,newRate, name, timeNow, notify)
            msg = self.getNotifyMsg(oneData, key, newElement)
            self.sendMsg(key, newElement, msg)

        if 'mt' in jsonData:
            self.mt = "?mt=" + jsonData['mt']


index = 0
checkImpl = dataCheck()
while(True):
    index += 1
    
    checkImpl.startCheck()
    time.sleep(10)

    