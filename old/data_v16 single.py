# encoding=utf8
import json
import time
from datetime import datetime

# import jpush as jpush
import requests

# app_key = "e52d41ac94ff8efa72fb225b"
# master_secret = "d3db9b965b618f538c4276c9"
# _jpush = jpush.JPush(app_key, master_secret)
# push = _jpush.create_push()
# push.audience = jpush.all_
# push.platform = jpush.all_


def clearStr(str):
    str = str.replace(" ", "")
    str = str.replace("\n", "")
    return str


class dataElement():
    def __init__(self, score=0, rate=0, name="", matchTime=0, notify=False, matchType="", initRate=-1, hostScore=0, guestScore=0, param={}, initCorner=-1):
        self.score = score
        self.rate = rate
        self.name = name
        self.time = matchTime
        self.notify = notify
        self.updata = int(time.time())
        self.type = matchType
        self.initRate = initRate
        self.initCorner = initCorner
        self.hostScore = hostScore
        self.guestScore = guestScore
        self.param = param


weixin = True
weixin = False


class dataCheck():
    def __init__(self, weixin):
        self.dataRecord = {}
        self.mt = ""
        self.lowValue = 1.68
        self.headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
                        'accept-encoding': 'gzip, deflate',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                        }
        self.index = 0
        self.timeCmp = 85

        self.scoreStatic = {}
        # self.strategy = checkStartegy()

        self.weixin = weixin
        self.userName = ''
        self.session = requests.session()
        # self.sql = sqlMgr('localhost', 'root', '861217', 'football')

    def notifyMsg(self, msg, key, newRate, oldRate, newElement):

        if not newElement.notify:
            print(msg)
            newElement.notify = True
            try:
                # logInfo = "{}\n".format(msg)
                # with open(r"buyPerDay.txt", 'a') as f:
                #     f.write(logInfo)
                # push.notification = jpush.notification(alert=msg)
                # push.send()
                url = 'http://47.115.122.26:4000/foot_data/send_data?data=' + msg
                self.session.get(url=url)

            except Exception as e:
                print("Exception:", repr(e))
        return newElement

    def startCheck(self):

        url = 'https://live.dszuqiu.com/ajax/score/data' + self.mt

        try:
            req = self.session.get(url=url, headers=self.headers)
            if req.status_code == 200:
                self.doCheck(req.text)
            # elif req.status_code == 304:
             #   print("data not modify")
        except Exception as e:
            print("connect err:" + repr(e))
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
                    print("delete " + key)

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

    def getInitCorner(self, oneData, key):
        initRate = -1
        if ('sd' in oneData):
            if ('f' in oneData['sd']):
                if ('hcb' in oneData['sd']['f']):
                    tmpStr = oneData['sd']['f']['hcb']
                    if isinstance(tmpStr, str):
                        initRate = float(tmpStr)
        if self.dataRecord.__contains__(key):
            if self.dataRecord[key].initCorner != -1:
                initRate = self.dataRecord[key].initCorner
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
        hostBig = False
        AttCount = 0

        if param.__contains__('hso') and param.__contains__('gso'):
            AttCount = param['hso'] + param['gso']

        if AttCount > 2:
            hostBig = True

        return hostBig

    #     hostBig, guestBig = dataCompare('ha', 'ga', hostBig, guestBig)  # 进攻
    #     hostBig, guestBig = dataCompare('hd', 'gd', hostBig, guestBig)  # 危险进攻
    #     hostBig, guestBig = dataCompareV2('hqq', 'gqq', hostBig, guestBig)
    #     hostBig, guestBig = dataCompare('hsf', 'gsf', hostBig, guestBig)  # 射偏
    #     hostBig, guestBig = dataCompare('hso', 'gso', hostBig, guestBig)  # 射正
    #     smallFlag = dataCompareV3('hsf', 'gsf', smallFlag, 4)  # 射偏
    #     smallFlag = dataCompareV3('hso', 'gso', smallFlag, 2)  # 射正
    #     return hostBig, guestBig, smallFlag

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
            name += "A " + host + " vs B " + guest + " C"
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
        if ('f_ld' in oneData):
            # if ('hrf' in oneData['f_ld']):  # 让球
            #     rateTmp = oneData['f_ld']['hrf']
            #     if rateTmp != None:
            #         newRate = float(oneData['f_ld']['hrf'])

            if ('hdx' in oneData['f_ld']):  # 大小
                rateTmp = oneData['f_ld']['hdx']
                if rateTmp != None:
                    newRate = float(oneData['f_ld']['hdx'])
        return newRate

    def getCorner(self, oneData, key):
        newRate = 0
        if self.dataRecord.__contains__(key):
            newRate = self.dataRecord[key].rate

        LowInfo = ""
        if ('f_ld' in oneData):
            if ('hcb' in oneData['f_ld']):  # corner
                rateTmp = oneData['f_ld']['hcb']
                if rateTmp != None:
                    newRate = float(oneData['f_ld']['hcb'])
        return newRate

    def checkLowRate(self, oneData, key):
        LowInfo = ""
        timeNow = self.dataRecord[key].time
        score = self.dataRecord[key].score
        # if timeNow <70 or  timeNow >= 80 and score >3:
        #     return LowInfo

        if ('f_ld' in oneData):
            # print(oneData)
            if ('hdxsp' in oneData['f_ld']):
                rateTmp = oneData['f_ld']['hdxsp']
                if rateTmp != None and float(rateTmp) < self.lowValue:
                    LowInfo = " 主队赔率:" + rateTmp
            if ('gdxsp' in oneData['f_ld']):
                rateTmp = oneData['f_ld']['gdxsp']
                if rateTmp != None and float(rateTmp) < self.lowValue:
                    LowInfo = " 客队赔率:" + rateTmp

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
        if oldElement.guestScore > newElement.guestScore:
            newElement.guestScore = oldElement.guestScore
        if oldElement.hostScore > newElement.hostScore:
            newElement.hostScore = oldElement.hostScore

        self.dataRecord[key] = newElement

        nowTime = datetime.now().strftime('%H:%M:%S')

        if newElement.time < 45 or newElement.time > 47 or newElement.score > 2:
            return

        big = self.checkParam(newElement.param)

        conditionScore = False
        msgType = ""

        rest = (newElement.rate - abs(newElement.initRate)) % 2
        if big and rest <= 1 and newElement.guestScore + newElement.hostScore == 1:
            conditionScore = True
            msgType = "大0.5"

        # msgType = ""
        # if big:
        #     big = True

        # if big and newElement.score < 2:
        #     conditionScore = True
        #     msgType = "单"

        if conditionScore and len(msgType) > 0:
            msg += nowTime + " " + msgType + " " + str(newElement.time) + " " + str(newElement.hostScore) + \
                ":" + str(newElement.guestScore) + " " + newElement.name
            # print(msg)
            newElement = self.notifyMsg(
                msg, key, newElement.rate, oldElement.rate, newElement)
            self.dataRecord[key] = newElement

    def doCheck(self, rowData):
        try:
            jsonData = json.loads(rowData)
        except Exception as e:
            print("err:" + repr(e)+" data:" + rowData)
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
                score_sum, host_score, guest_score = self.getScoreSum(
                    oneData, key)
                newRate = self.getRate(oneData, key)
                timeNow = self.getTime(oneData, key)
                notify = self.getNotify(oneData, key)
                initRate = self.getInitRate(oneData, key)
                initCorner = self.getInitCorner(oneData, key)
                param = self.getParam(oneData, key)

                newElement = dataElement(score_sum, newRate, name, timeNow,
                                         notify, matchType, initRate, host_score, guest_score, param, initCorner=initCorner)

                self.getNotifyMsg(oneData, key, newElement)
            except Exception as e:
                continue

        if 'mt' in jsonData:
            self.mt = "?mt=" + jsonData['mt']


index = 0
checkImpl = dataCheck(weixin)
while(True):
    index += 1

    checkImpl.startCheck()
    time.sleep(10)
