# encoding=utf8
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from db.mysql import sqlMgr
import random
import ssl
import os
import _thread
from commend import commend
from tool import ipTool




def addOutputInfo(key, info, outputInfo):
    timeArray= time.strptime('20'+ key, "%Y/%m/%d %H:%M")
    key = int(time.mktime(timeArray))
    if outputInfo.__contains__(key) == False:
        outputInfo[key] = []
    outputInfo[key].append(info)

# def getIpList():
#     urlTmp = "http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp=电信"
#     req = requests.get(urlTmp)
#     s = req.text
#     ips = s.split('<br>')
#     if len(ips) == 0:
#         time.sleep(3)
#         return ips
#     ips.pop(0)
#     if len(ips) == 0:
#         time.sleep(3)
#         return ips
#     ips.pop(0)
#     if len(ips) == 0:
#         time.sleep(3)
#         return ips
#     ips.pop(len(ips)-1)
#     print("get ips size:", len(ips))
#     if len(ips) == 0:
#         time.sleep(3)
#         return ips
    
#     return ips

def writeFile(info):
    # with open(r"result.txt", 'a') as f:
    #     f.write(info + "\n")
        # print(info)
    return




def clearStr(str):
    str = str.replace(" ", "")
    str = str.replace("\n", "")
    return str

def longTime(timeStr):
    timeArray= time.strptime('20'+ timeStr, "%Y/%m/%d %H:%M")
    gameTime = int(time.mktime(timeArray))
    now = int(time.time()) 
    if gameTime - now > 60*60*24:
        return True
    return False
def getTime(timeStr):
    timeArray= time.strptime('20'+ timeStr, "%Y/%m/%d %H:%M")
    return int(time.mktime(timeArray))

class parser:
    class gameData:
        def __init__(self):    
            self.main = ''     
            self.client = ''     
            self.main_score = 0  
            self.client_score = 0   
            self.result = 0  
            self.rate_result = 0 
            self.type = ''
            self.rate = float(0)
            self.win_rate = float(0)
            self.lost_rate = float(0)
            self.time = 0



    def __init__(self, url, ipList, sql):

        self.sql = sql
        self.soup = BeautifulSoup(self.getHtmlText(url, ipList))
        self.url = url
        self.main = []
        self.client = []
        self.score = []
        self.param = []

        self.commend = commend()

    def getHtmlText(self, url, ipList):

        def addIp(ipStr):
            proxies =[]
            proxies.append({'http': ipStr,'https': ipStr})
            return proxies


        ipChoice = random.choice(ipList)

        try:
            req = requests.get(url,proxies=random.choice(addIp(ipChoice)),timeout=3)
        except:
            ipList.remove(ipChoice)
            # print("remove ip, restSize:", len(ipList))
            raise Exception()
        
        s = req.text
        if len(s) < 1000:
            ipList.remove(ipChoice)
            # print("remove ip, restSize:", len(ipList))
            raise Exception()
        return s

    def getData(self, key, cmd, outputInfo, mainFlag):
        for title in self.soup.find_all('title') :
            if title.string.find('404') != -1:
                return False

        type_game = ""
        checkFlag = True
        if checkFlag:
            for tr  in self.soup.find_all('tr', class_='page-1'):
                td = tr.find('td', class_="bg1")
                if td == None:
                    continue
                type_game = td.text
                td = td.findNextSibling('td')
                td = td.findNextSibling('td')
                gameTime = td.text

                if longTime(gameTime):
                    continue

                main = ""
                client = ""

                for td in tr.find_all('td', class_="text-right BR0"):
                    for a in td.find_all('a', target="_blank"):
                        main = clearStr(a.text)

                for td in tr.find_all('td', class_="text-left"):
                    a = td.find('a', target="_blank")
                    client = clearStr(a.text)
                    break


                def checkBuy(teamName, cmd):
                    # if teamName == "":
                    #     teamName = teamName
                    # else:
                    #     # print(teamName)
                    data = self.sql.queryTeamData(type_game, teamName, 'k_corner')
                    result = {}
                    for one in data:
                        main = one[0]
                        client = one[1]
                        main_score = one[2]
                        client_score = one[3]
                        rate = float(one[4])
                        gameTime = one[9]

                        key = gameTime
                        if main_score - client_score > 0:
                            if result.__contains__(key) == False:
                                result[key] = {}
                            if main == teamName:
                                result[key] = 1
                            elif client == teamName:
                                result[key] = -1

                        elif main_score - client_score < 0:
                            if result.__contains__(key) == False:
                                result[key] = {}
                            if main == teamName:
                                result[key] = -1
                            elif client == teamName:
                                result[key] = 1
                        else:
                            if result.__contains__(key) == False:
                                result[key] = {}
                            if main == teamName:
                                result[key] = 0
                            elif client == teamName:
                                result[key] = 0
                    # keys = result.keys()
                    values = list(result.keys())
                    values.sort(reverse = True)


                    def chechResult(gameTmp):
                        if gameTmp == -1 :
                            return 1
                        return 0

                    lostSum = 0
                    checkSum = cmd[1]

                    for index in range(checkSum):
                        key = values[index]
                        if result[key] == -1:
                            lostSum += 1
                    
                    if lostSum == checkSum :
                        return True
                    return False

                buyInfo = cmd[3]
                if main != "" and mainFlag == 1 and checkBuy(main, cmd):
                    addInfo = "【" + buyInfo + "】"
                    infoTmp = "{} {} {} game info: {} {} {}".format(gameTime, type_game,addInfo,  main, client, cmd[4])
                    addOutputInfo(gameTime, infoTmp,outputInfo)
                    self.commend.add(main, getTime(gameTime), buyInfo)

                elif client != "" and mainFlag == -1 and checkBuy(client, cmd):
                    if "胜" in buyInfo:
                        buyInfo = buyInfo.replace("胜", "输")
                    elif "输" in buyInfo:
                        buyInfo = buyInfo.replace("输", "胜")

                    addInfo = "【" + buyInfo + "】"
                    infoTmp = "{} {} {} game info: {} {} {}".format(gameTime, type_game,addInfo,  main, client, cmd[4])
                    addOutputInfo(gameTime, infoTmp, outputInfo)
                    self.commend.add(main, getTime(gameTime), buyInfo)
                    
        for tr in self.soup.find_all('tr') :
            td = tr.find('td', class_="bg1")
            if td == None:
                continue
            type_game = td.text

            td = td.findNextSibling('td')
            td = td.findNextSibling('td')
            timeArray= time.strptime('20'+ td.text, "%Y/%m/%d %H:%M")
            gameTime = int(time.mktime(timeArray))



            td = tr.find('td', class_="BR0 text-center red-color PL0 PR0")
            if td == None:
                continue
            score = td.text

            score = score.replace(" ", "")
            scoreTmp = score.split(':')

            if int(scoreTmp[0]) < 0:
                continue
            main_score = int(scoreTmp[0])

            if int(scoreTmp[1]) < 0:
                continue
            client_score = int(scoreTmp[1])

            # print(type_game)
            main = ""
            client = ""
            for td in tr.find_all('td', class_="text-right BR0"):
                for a in td.find_all('a', target="_blank"):
                    main = clearStr(a.text)

            for td in tr.find_all('td', class_="text-left"):
                for a in td.find_all('a', target="_blank"):
                    client = clearStr(a.text)


            rate = 0
            scoreRate = 0
            cornerRate = 0
            tds = tr.find_all('td', class_="text-center")
            for tdTmp in tds :
                a = tdTmp.find('a', target="_blank")
                if a == None:
                    continue
                tmp = a.text
                tmp = tmp.replace(" ", "")
                tmp = tmp.replace("+", "")
                sliceTmp = tmp.split('/')
                rate = clearStr(sliceTmp[0])
                scoreRate = clearStr(sliceTmp[1])
                cornerRate = clearStr(sliceTmp[2])
                break


            tds = tr.find_all('td', class_="text-center blue-color")
            if tds == None :
                continue
            # print(len(tds))
            if len(tds) != 2 :
                continue
            td = tds[1]

            tmp = td.text
            tmp = tmp.replace(" ", "")
            cornerTmp = tmp.split(':')
            main_corner = int(cornerTmp[0])
            client_corner = int(cornerTmp[1])

            input = "'"+ main + "','" + client +"','" + str(main_score) +"','" + str(client_score) + "','"  + str(rate) + "','"+ type_game +"'"
            input += ",'"+  str(main_corner) + "','" + str(client_corner)+ "','" + str(client_corner + main_corner)+ "','" + str(gameTime) +"'" 
            input += ",'"+  main + "_" + str(gameTime) + "'" 
            input += ",'{}','{}'".format(scoreRate, cornerRate)
            self.sql.insert(input, "k_corner")
            self.commend.check(main, gameTime, main_score, client_score, rate, scoreRate, client_corner + main_corner, cornerRate)



def working(tableName):
    sql = sqlMgr('localhost', 'root', '861217', 'football')
    ipObj = ipTool()
    ipList = ipObj.getIpList()
    index = 1
    end = 2
    # if checkFlag:
    #     end = 2
    outputInfo = {}
    gameCode = []
    gameCode = sql.queryByTypeAll(tableName)
    # 买预备=========================
    gameIndex = 0

    while index < end:
        gameIndex = 0
        while gameIndex < len(gameCode) :
            url = "https://www.dszuqiu.com/league/"+str(gameCode[gameIndex][0]) + "/p.1"
            url = url.replace("p.1", "p."+ str(index) )
            
            try:
                html =  parser(url, ipList, sql)
                if len(ipList) < 2:
                    ipList = ipObj.getIpList()
            except:
                # time.sleep(10)
                if len(ipList) < 2:
                    ipList = ipObj.getIpList()
                # print ("connect err")
                continue

            # print( index, gameCode[gameIndex][2])
            try:   
                if html.getData("k_corner", gameCode[gameIndex], outputInfo, gameCode[gameIndex][5]) == False :
                    break
            except:
                if len(ipList) < 2:
                    ipList = ipObj.getIpList()
                # print ("error :")
            # time.sleep(1)
            
            gameIndex += 1
        index += 1

        values = list(outputInfo.keys())
        values.sort()

        for value in values:
            for tmp in outputInfo[value]:
                writeFile(tmp)
        
        outputInfo.clear()
        info = "================================"
        writeFile(info)
        # print(tableName, " size:", len(outputInfo))

try:
    os.remove(r"result.txt")
except :
    pass


def doDayWork():
    print("start do doDayWork")
    
    _thread.start_new_thread(working,("k_rateBuy",))
    # _thread.start_new_thread(working,("k_compBuy",))
    _thread.start_new_thread(working,("k_scoreBuy",))
    working("k_cornerBuy")
    # working("k_rateBuy")
    print("end do doDayWork")


# doDayWork()
# working("k_cornerBuy")