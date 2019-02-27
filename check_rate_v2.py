# encoding=utf8
import requests
import re
import time
import threading
from datetime import datetime
import json
import ctypes
# import itchat
from check_strategy import checkStartegy



def clearStr(str):
    str = str.replace(" ", "")
    str = str.replace("\n", "")
    return str

class dataElement():
    def __init__(self, score = 0, rate = 0, name="", matchTime=0, notify=False, matchType="", initRate=-1, hostScore=0, guestScore=0, param={}):
        self.score = score
        self.rate = rate
        self.name = name
        self.time = matchTime
        self.notify = notify
        self.updata = int(time.time())
        self.type = matchType
        self.initRate = initRate
        self.hostScore = hostScore
        self.guestScore = guestScore
        self.param = param

weixin = True
weixin = False


# def notifyMsg(msg):
def notifyMsg(msg, userName):
    #itchat.send(msg,toUserName = userName)
    return

class dataCheck():
    def __init__(self, weixin):
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

        self.weixin = weixin
        self.userName = ''

        if self.weixin:
            itchat.auto_login(hotReload=True)
            users = itchat.search_friends(name='在路上')
            self.userName = users[0]['UserName']

    def startCheck(self):
        
        url = 'https://live.dszuqiu.com/ajax/score/data' + self.mt

        try:
            req = requests.get(url=url , headers=self.headers)
            if req.status_code == 200:
                self.doCheck(req.text)
            # elif req.status_code == 304:
             #   print("data not modify")
        except Exception as e:
            print("connect err:"+ repr(e))
            return
       
        
        nowTime = datetime.now().strftime('%H:%M:%S')
        # print(nowTime," start check. url:",url)
        if time.time() % (60*10) == 0 :
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
            
            print("delete size"+ len(deleteKeys))
            for key in deleteKeys:
                self.dataRecord.pop(key)
                # print("delete "+ key)
            print("[-] end clear dataRecord")

        # if self.index % 60 == 0:

    def getInitRate(self, oneData, key):
        initRate = -1
        if ('sd' in oneData):
            if ('f' in oneData['sd']):
                if ('hrf' in oneData['sd']['f']):
                    tmpStr = oneData['sd']['f']['hrf']
                    if isinstance(tmpStr, str):
                        initRate = float(tmpStr)
        if self.dataRecord.__contains__(key):
            if self.dataRecord[key].initRate != -1:
                initRate = self.dataRecord[key].initRate
        return initRate



    def getParam(self, oneData, key):
        param = {}
        if ('plus' in oneData):
            def getData(key, param):
                if(key in oneData['plus']):
                    param[key] = int(oneData['plus'][key])
                return param
            
            param = getData('ha', param)            
            param = getData('hd', param)            
            param = getData('hqq', param)            
            param = getData('hsf', param)    
            param = getData('hso', param)

            param = getData('ga', param)
            param = getData('gd', param)
            param = getData('gqq', param)
            param = getData('gsf', param)
            param = getData('gso', param)
            return param

        if self.dataRecord.__contains__(key):
            if self.dataRecord[key].param != {}:
                param = self.dataRecord[key].param
        return param

    def checkParam(self, param):
        hostBig = True
        guestBig = True

        def dataCompare(hostKey, guestKey,hostBig, guestBig):
            if param.__contains__(hostKey) and param.__contains__(guestKey):
                if param[hostKey] > param[guestKey]:
                    guestBig = False
                elif param[hostKey] < param[guestKey]:
                    hostBig = False
                else:
                    guestBig = False
                    hostBig = False
            return hostBig, guestBig
        hostBig, guestBig = dataCompare('ha','ga',hostBig, guestBig)
        hostBig, guestBig = dataCompare('hd','gd',hostBig, guestBig)
        hostBig, guestBig = dataCompare('hqq','gqq',hostBig, guestBig)
        hostBig, guestBig = dataCompare('hsf','gsf',hostBig, guestBig)
        hostBig, guestBig = dataCompare('hso','gso',hostBig, guestBig)
        return hostBig,guestBig

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
            name += "A " + host + " vs B " + guest  + " C"
        if self.dataRecord.__contains__(key):
            name = self.dataRecord[key].name
        return name

    def getScoreSum(self, oneData, key):
        score_sum = -1
        dataKey = 'rd'
        host_score = 0
        guest_score = 0
        if self.dataRecord.__contains__(key):
            score_sum = self.dataRecord[key].score

        if (dataKey in oneData):
            host_score = int(oneData[dataKey]['hg'])
            guest_score = int(oneData[dataKey]['gg'])
            score_sum = host_score + guest_score
        return score_sum, host_score, guest_score
    

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
        # if timeNow <70 or  timeNow >= 80 and score >3:
        #     return LowInfo

        if ('f_ld' in oneData) :
            print(oneData)
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

        if newElement.time > 52 or newElement.time < 35:
            return msg
        if newElement.time < 37 and newElement.notify == False:
            newElement.notify = True
            rateDiv = newElement.rate - newElement.score
            condition = (rateDiv == 1.5 and newElement.score == 1)
            condition = condition or (rateDiv == 1.25 and newElement.score == 0)
            # condition = condition or (rateDiv == 2.5 and newElement.score == 0)

            if condition:
                msg = nowTime +" " + newElement.name + "    score:"+ str(newElement.score) + " 小"

            condition = (rateDiv == 1.75 and newElement.score == 1)
            if condition:
                msg = nowTime +" " + newElement.name + "    score:"+ str(newElement.score) + " 大"

        return msg
        # hostBig, guestBig = self.checkParam(newElement.param)

        # if newElement.time <= 45:
        #     if (newElement.initRate <= -0.5 and newElement.guestScore > 0 and hostBig) or \
        #     (newElement.initRate >= 0.5 and newElement.hostScore > 0 and guestBig):
        #         msg = nowTime +" " + newElement.name

        # return msg

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
            # print(oneData)
            if ('id' in oneData) == False: 
                continue
            key = oneData['id']
            matchType = self.getType(oneData, key)
            name = self.getName(oneData, key)
            score_sum, host_score, guest_score = self.getScoreSum(oneData, key)
            newRate = self.getRate(oneData, key)
            timeNow = self.getTime(oneData, key)
            notify = self.getNotify(oneData, key)
            initRate = self.getInitRate(oneData, key)
            param = self.getParam(oneData, key)

            newElement = dataElement(score_sum,newRate, name, timeNow, notify,matchType,initRate, host_score, guest_score,param)
            msg = self.getNotifyMsg(oneData, key, newElement)
            self.sendMsg(key, newElement, msg)

        if 'mt' in jsonData:
            self.mt = "?mt=" + jsonData['mt']


index = 0
checkImpl = dataCheck(weixin)
while(True):
    index += 1
    
    checkImpl.startCheck()
    time.sleep(10)

    
