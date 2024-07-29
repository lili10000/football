# encoding=utf8
import requests
import time
from datetime import datetime
import json

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def clearStr(str):
    str = str.replace(" ", "")
    str = str.replace("\n", "")
    return str

class dataElement():
    def __init__(self, score = 0, rate = 0, name="", matchTime=0, notify=False, matchType="", initRate=-1, hostScore=0, guestScore=0, cornerSum=0):
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
        self.cornerSum = cornerSum


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

        self.session = requests.session()
        self.session.keep_alive =False
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        self.scoreStatic = {}


      

    def notifyMsg(self, msg, key, newRate, oldRate, newElement):

        if not newElement.notify:
            print(msg)
            newElement.notify = True
        return newElement

    def startCheck(self):
        
        url = 'https://live.dszuqiu.com/ajax/score/data' + self.mt

        try:
            req = self.session.get(url=url , headers=self.headers)
            if req.status_code == 200:
                self.doCheck(req.text)
            # elif req.status_code == 304:
             #   print("data not modify")
        except Exception as e:
            print("connect err:"+ repr(e))
            return
       
        
        nowTime = datetime.now().strftime('%H:%M:%S')
        # print(nowTime," start check. url:",url)
        if index % 10 == 0:
            print(".")

        time.sleep(10)

        if index % 540 == 0:
            print("[+] start clear dataRecord")
            keys = self.dataRecord.keys()
            deletKeys = []
            for key in keys:
                oneData = self.dataRecord[key]
                now = int(time.time())
                if (now - oneData.updata) > 5400:
                    deletKeys.append(key)
                    # dataRecord.pop(key)
                    print("delete "+ key)

            for key in deletKeys:
                self.dataRecord.pop(key)
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
    
    def getCornerSum(self, oneData, key):
        corner_sum = -1
        dataKey = 'rd'
        host_corner = 0
        guest_corner = 0
        if self.dataRecord.__contains__(key):
            corner_sum = self.dataRecord[key].cornerSum

        if (dataKey in oneData):
            host_score = int(oneData[dataKey]['hc'])
            guest_score = int(oneData[dataKey]['gc'])
            corner_sum = host_score + guest_score
        return corner_sum

    def getRate(self, oneData, key):
        newRate = 0     
        if self.dataRecord.__contains__(key):
            newRate = self.dataRecord[key].rate

        LowInfo = ""
        if ('f_ld' in oneData) :
            if ('hrf' in oneData['f_ld']): # 让球
                rateTmp = oneData['f_ld']['hrf']
                if rateTmp != None:
                    newRate = float(oneData['f_ld']['hrf'])
            
            # if ('hdx' in oneData['f_ld']): #大小
            #     rateTmp = oneData['f_ld']['hdx']
            #     if rateTmp != None:
            #         newRate = float(oneData['f_ld']['hdx'])
        return newRate


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

    
        # hostBig, guestBig = self.checkParam(newElement.param)
        
        conditionScore = False
        #if newElement.time < 30   or (newElement.hostScore - newElement.guestScore) != 0  or newElement.score == -1  or \
        #    (newElement.hostScore + newElement.guestScore) != newElement.score or newElement.time > 75 :
        #    return

        if newElement.time > 55  or  newElement.time < 45 :
            return
        
        if(newElement.score > 1 and newElement.cornerSum > 4 ):
            conditionScore = True


        msg = ""

        if conditionScore:
            msg += " " + str(newElement.time) + " " + newElement.name
            newElement = self.notifyMsg(msg, key, newElement.rate, oldElement.rate, newElement)
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
            try:
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
                cornerSum = self.getCornerSum(oneData, key)
                
                newElement = dataElement(score_sum,newRate, name, timeNow, notify,matchType,initRate, host_score, guest_score,cornerSum)

                self.getNotifyMsg(oneData, key, newElement)
            except Exception as e:
                continue

        if 'mt' in jsonData:
            self.mt = "?mt=" + jsonData['mt']


index = 0
checkImpl = dataCheck()
while(True):
    index += 1
    
    checkImpl.startCheck()
    time.sleep(10)

    
