# encoding=utf8
import json
import re
import threading
import time
from datetime import datetime

import requests

# import ctypes
# import itchat
# from check_strategy import checkStartegy
# from db.mysql import sqlMgr


def clearStr(str):
    str = str.replace(" ", "")
    str = str.replace("\n", "")
    return str


class dataElement():
    def __init__(self, score=-1, rate=0, name="", matchTime=0, notify=False, matchType="", initScore=-1, inithalfScore=-1, nowRate=-1, hostScore=0, guestScore=0):
        self.score = score
        self.rate = rate
        self.name = name
        self.time = matchTime
        self.notify = notify
        self.updata = int(time.time())
        self.type = matchType
        self.initScore = initScore
        self.inithalfScore = inithalfScore
        self.nowRate = nowRate

        self.haveScore = 0
        self.timestamp = int(time.time())

        self.buyBig = False
        self.buySmall = False

        # self.mainRate = mainRate
        # self.clientRate = clientRate
        self.scoreTime = 0


weixin = True
weixin = False


# def notifyMsg(msg):
def notifyMsg(msg, userName):
    #itchat.send(msg,toUserName = userName)
    return


class dataCheck():
    def __init__(self, weixin):
        self.dataRecord = {}
        self.DBSave = {}
        self.mt = ""
        self.lowValue = 1.68
        self.headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
                        'accept-encoding': 'gzip, deflate',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                        }
        self.index = 0
        self.timeCmp = 85

        # self.scoreStatic = {}
        # self.strategy = checkStartegy()

        # self.weixin = weixin
        self.userName = ''

        self.buyBigWin = 0
        self.buyBigLost = 0
        self.buySmallWin = 0
        self.buySmallLost = 0

        self.timeSave = 0

        # self.sql = sqlMgr('localhost', 'root', '861217', 'football')

        # self.keyGame = self.sql.queryByTypeAll('k_namerate')

        # if self.weixin:
        #     itchat.auto_login(hotReload=True)
        #     users = itchat.search_friends(name='在路上')
        #     self.userName = users[0]['UserName']

    def startCheck(self):

        url = 'https://live.dszuqiu.com/ajax/score/data' + self.mt

        try:
            req = requests.get(url=url, headers=self.headers)
            if req.status_code == 200:
                self.doCheck(req.text)
            # elif req.status_code == 304:
            #    print("data not modify")
        except Exception as e:
            print("connect err:" + repr(e))
            return

        nowTime = datetime.now().strftime('%H:%M:%S')
        # print(nowTime," start check. url:",url)
        now = int(time.time())
        if now > self.timeSave + (15*60):
            self.timeSave = now
            # self.keyGame = self.sql.queryByTypeAll('k_namerate')
            # print(datetime.now().strftime('%H:%M:%S'), "saveDataSize:", len(self.DBSave), "buyBigWin:", self.buyBigWin,
            #       "buyBigLost:", self.buyBigLost, "buySmallWin:", self.buySmallWin, "buySmallLost:", self.buySmallLost)

        self.index += 1
        if self.index % 540 == 0:
            print("[+] start clear dataRecord")
            deleteKeys = []
            for key in self.dataRecord:
                oneData = self.dataRecord[key]
                now = int(time.time())
                if (now - oneData.updata) > 5400:
                    deleteKeys.append(key)

            print("delete size:", len(deleteKeys))
            for key in deleteKeys:
                self.dataRecord.pop(key)
                # print("delete "+ key)
            print("[-] end clear dataRecord")

        # if self.index % 60 == 0:

    def getInitRate(self, oneData, key):
        initRate = -1
        if ('sd' in oneData):
            if ('f' in oneData['sd']):
                if ('hdx' in oneData['sd']['f']):
                    tmpStr = oneData['sd']['f']['hdx']
                    if isinstance(tmpStr, str):
                        initRate = float(tmpStr)

        # if self.dataRecord.__contains__(key):
        #     if self.dataRecord[key].initScore != -1:
        #         initRate = self.dataRecord[key].initScore
        return initRate

    def getInitHalfRate(self, oneData, key):
        initRate = -1
        if ('sd' in oneData):
            if ('h' in oneData['sd']):
                if ('hdx' in oneData['sd']['h']):
                    tmpStr = oneData['sd']['h']['hdx']
                    if isinstance(tmpStr, str):
                        initRate = float(tmpStr)
        # if self.dataRecord.__contains__(key):
        #     if self.dataRecord[key].inithalfScore != -1:
        #         initRate = self.dataRecord[key].inithalfScore
        return initRate

    def getNowRate(self, oneData, key):
        initRate = -1
        if ('f_ld' in oneData):
            if ('f' in oneData['sd']):
                if ('hdx' in oneData['sd']['f']):
                    tmpStr = oneData['sd']['f']['hdx']
                    if isinstance(tmpStr, str):
                        initRate = float(tmpStr)
        return initRate

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
            # name += "A " + host + " vs B " + guest  + " C"
            name += host + " vs " + guest
        if self.dataRecord.__contains__(key):
            name = self.dataRecord[key].name
        return name

    def getScoreSum(self, oneData, key):
        score_sum = -2
        dataKey = 'rd'
        host_score = -1
        guest_score = -1
        if self.dataRecord.__contains__(key):
            score_sum = self.dataRecord[key].score

        if (dataKey in oneData):
            host_score = int(oneData[dataKey]['hg'])
            guest_score = int(oneData[dataKey]['gg'])
            score_sum = host_score + guest_score
        return score_sum, host_score, guest_score

    def getRate(self, oneData, key):
        newRate = 0
        mainRate = 0
        clientRate = 0
        if self.dataRecord.__contains__(key):
            newRate = self.dataRecord[key].rate

        LowInfo = ""
        if ('f_ld' in oneData):
            if ('hdx' in oneData['f_ld']):
                rateTmp = oneData['f_ld']['hdx']
                if rateTmp != None:
                    newRate = float(oneData['f_ld']['hdx'])
            if ('hdxsp' in oneData['f_ld']):
                rateTmp = oneData['f_ld']['hdxsp']
                if rateTmp != None:
                    mainRate = float(rateTmp)
            if ('gdxsp' in oneData['f_ld']):
                rateTmp = oneData['f_ld']['gdxsp']
                if rateTmp != None:
                    clientRate = float(rateTmp)
        return newRate, mainRate, clientRate

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

        now = int(time.time())

        if newElement.time != 45 or newElement.score < 0:
            return msg

        if newElement.notify == True or newElement.score > 3 or newElement.initScore == -1:
            return msg

        if (newElement.initScore - newElement.inithalfScore) - (newElement.nowRate - newElement.score) >= 0.5:
            msg = nowTime + " 大 " + newElement.name
        elif (newElement.initScore - newElement.inithalfScore) - (newElement.nowRate - newElement.score) <= -0.5:
            msg = nowTime + " 小 " + newElement.name
        return msg

    def sendMsg(self, key, newElement, msg):
        if msg != "" and newElement.notify == False:
            print(msg)
            # t = threading.Thread(target=notifyMsg, args=(msg, self.userName,))
            # t =threading.Thread(target=notifyMsg,args=(msg,))
            # t.start()
            newElement.notify = True
            self.dataRecord[key] = newElement

    def doCheck(self, rowData):
        try:
            jsonData = json.loads(rowData)
        except Exception as e:
            print("err:" + repr(e))
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
            newRate, mainRate, clientRate = self.getRate(oneData, key)
            timeNow = self.getTime(oneData, key)
            notify = self.getNotify(oneData, key)
            initRate = self.getInitRate(oneData, key)
            initHlafRate = self.getInitHalfRate(oneData, key)
            # initRate = self.getInitRate(oneData, key)
            # nowRate = self.getNowRate(oneData, key)

            # param = self.getParam(oneData, key)

            newElement = dataElement(score_sum, newRate, name, timeNow, notify, matchType,
                                     initRate, initHlafRate, newRate, host_score, guest_score)
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
