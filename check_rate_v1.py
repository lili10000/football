# encoding=utf8
import requests
import re
import time
import threading
from datetime import datetime
import json
import ctypes
import itchat
from check_strategy import checkStartegy


def clearStr(str):
    str = str.replace(" ", "")
    str = str.replace("\n", "")
    return str

class dataElement():
    def __init__(self, score = 0, rate = 0, name="", matchTime=0, notify=False, matchType=""):
        self.score = score
        self.rate = rate
        self.name = name
        self.time = matchTime
        self.notify = notify
        self.updata = int(time.time())
        self.type = matchType

# def notifyMsg(msg):
def notifyMsg(msg, userName):
    itchat.send(msg,toUserName = userName)
    return

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
        self.timeCmp = 85

        self.scoreStatic = {}
        self.strategy = checkStartegy()

        itchat.auto_login(hotReload=True)
        users = itchat.search_friends(name='在路上')
        self.userName = users[0]['UserName']

    def startCheck(self):
        
        url = 'https://live.dszuqiu.com/ajax/score/data' + self.mt

        try:
            req = requests.get(url=url , headers=self.headers)
            if req.status_code == 200:
                self.doCheck(req.text)
            elif req.status_code == 304:
                print("data not modify")
        except Exception as e:
            print("connect err:"+ repr(e))
            return
       
        
        nowTime = datetime.now().strftime('%H:%M:%S')
        # print(nowTime," start check. url:",url)
        print(nowTime)

        self.index += 1
        if self.index % 540 == 0:
            print("[+] start clear dataRecord")
            deleteKeys = []
            for key in self.dataRecord:
                oneData = self.dataRecord[key]
                now = int(time.time())
                if (now - oneData.updata) > 5400:
                    deleteKeys.append(key)
                    
            for key in deleteKeys:
                self.dataRecord.pop(key)
                print("delete "+ key)
            print("[-] end clear dataRecord")

        # if self.index % 60 == 0:


    def getType(self, oneData, key):
        matchType = ""
        if ('league' in oneData):
            matchType += oneData['league']['n'] + '  '
        if self.dataRecord.__contains__(key):
            matchType = self.dataRecord[key].type
        matchType = clearStr(matchType)
        return matchType

    def getName(self, oneData, key):
        name = ""
        if ('league' in oneData):
            name += oneData['league']['n'] + '  '
            
        if ('host' in oneData): 
            host = oneData['host']['n']
            guest = oneData['guest']['n']
            name += host + " vs " + guest
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
            if ('hdx' in oneData['f_ld']):
                rateTmp = oneData['f_ld']['hdx']
                if rateTmp != None:
                    newRate = float(oneData['f_ld']['hdx'])
        return newRate

    def checkLowRate(self,oneData, key):
        LowInfo = ""
        timeNow = self.dataRecord[key].time
        score = self.dataRecord[key].score
        if timeNow <70 or  timeNow >= 80 and score >3:
            return LowInfo

        if ('f_ld' in oneData) :
            if ('hdxsp' in oneData['f_ld']):
                rateTmp = oneData['f_ld']['hdxsp']
                if rateTmp != None and float(rateTmp) < self.lowValue:
                    LowInfo = " 主队赔率:" +rateTmp
            if ('gdxsp' in oneData['f_ld']):
                rateTmp = oneData['f_ld']['gdxsp']
                if rateTmp != None and float(rateTmp) < self.lowValue:
                    LowInfo = " 客队赔率:" +rateTmp


        # if LowInfo != "" :
        #     score = self.dataRecord[key].score
        #     name = self.dataRecord[key].name
        #     if score == -1:
        #         return LowInfo

            # if self.scoreStatic.__contains__(score) == False :
            #     self.scoreStatic[score] = {}
            # self.scoreStatic[score][key] = name
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

        nowTime = datetime.now().strftime('%H:%M:%S')

        if newElement.time < 20 and self.dataRecord[key].rate < 1 and self.dataRecord[key].rate > 0:
            msg = nowTime +" " + newElement.name + " rate <= 1"
            return msg
        if newElement.time >= self.timeCmp:
            return msg

        
        retnStr = self.strategy.check(type=newElement.type, score=newElement.score, time=newElement.time)
        if retnStr != None:
            if retnStr == "":
                return retnStr
            msg = nowTime + " " + newElement.name + "   "+retnStr
            return msg

        conditionScore = bool(newElement.score == oldElement.score)
        conditionRate = bool((abs(newElement.rate - oldElement.rate) >= 0.5)and oldElement.rate != 0)

        if conditionScore and  conditionRate:
            msg = nowTime + " " + newElement.name + " new:" + str(newElement.rate) +  " old:" + str(oldElement.rate)

        LowInfo = self.checkLowRate(oneData, key)
        if LowInfo != "":
            msg = nowTime + " " + newElement.name + " rate <" + str(self.lowValue)  + LowInfo
        return msg

    def sendMsg(self, key, newElement, msg):
        if msg != "" and newElement.notify == False:
            print(msg)
            t =threading.Thread(target=notifyMsg,args=(msg,self.userName,))
            # t =threading.Thread(target=notifyMsg,args=(msg,))
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
            matchType = self.getType(oneData, key)
            name = self.getName(oneData, key)
            score_sum = self.getScoreSum(oneData, key)
            newRate = self.getRate(oneData, key)
            timeNow = self.getTime(oneData, key)
            notify = self.getNotify(oneData, key)

            newElement = dataElement(score_sum,newRate, name, timeNow, notify,matchType)
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

    
