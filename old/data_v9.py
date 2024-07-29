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


def writeFile(info):
    # with open(r"result_v3.txt", 'a') as f:
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
        self.version = 1

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

    def getData(self, key, cmd, outputInfo):
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

                gameId = ""
                for td in tr.find_all('td', class_="text-center yellowTd BR0"):
                    for a in td.find_all('a'):
                        tmp = a.attrs['href']
                        gameIdList = tmp.split('/')
                        gameId = gameIdList[2]
                        break
                    if gameId != "":
                        break

                rateNow = ""
                for td in tr.find_all('td', class_="text-center yellowTd BR0"):
                    for a in td.find_all('a', target="_blank"):
                        rateNow = clearStr(a.text)
                        break
                    if rateNow != "":
                        break
                
                def checkBuy(teamName, cmd, mainFlag=False):
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
                        if main_score - client_score + rate > 0:
                            
                            if main == teamName:
                                if result.__contains__(key) == False:
                                    result[key] = {}
                                result[key] = 1
                            elif client == teamName:
                                if result.__contains__(key) == False:
                                    result[key] = {}
                                result[key] = -1

                        elif main_score - client_score + rate < 0:                           
                            if main == teamName:
                                if result.__contains__(key) == False:
                                    result[key] = {}
                                result[key] = -1
                            elif client == teamName:
                                if result.__contains__(key) == False:
                                    result[key] = {}
                                result[key] = 1
                        else:                            
                            if main == teamName:
                                if result.__contains__(key) == False:
                                    result[key] = {}
                                result[key] = 0
                            elif client == teamName:
                                if result.__contains__(key) == False:
                                    result[key] = {}
                                result[key] = 0
                    # keys = result.keys()
                    values = list(result.keys())
                    values.sort(reverse = True)


                    def chechResult(gameTmp):
                        if gameTmp == 1 :
                            return 1
                        return 0

                    lostSum = 0
                    winSum = 0
                    checkSum = cmd[1]


                    winFlag = False
                    lostFlag = False

                    if len(values) < checkSum:
                        return winFlag, lostFlag 

                    for index in range(checkSum):
                        key = values[index]
                        if result[key] == -1:
                            lostSum += 1
                        if result[key] == 1:
                            winSum += 1
                    


                    if winSum == checkSum:
                        winFlag = True
                    if lostSum == checkSum:
                        lostFlag = True
                    return winFlag, lostFlag


                def condition_v3(mainFlag, winFlag, lostFlag, cmd):
                    def check(mainFlag, winFlag, lostFlag, cmd):
                        if mainFlag and winFlag and cmd[5] == -1 : 
                            return True
                        elif mainFlag == False and lostFlag and cmd[5] == -1 :                    
                            return True
                        elif mainFlag == False and winFlag and cmd[5] == 1 : 
                            return True
                        return False

                    if check(mainFlag, winFlag, lostFlag, cmd) == False:
                        return
                    
                    addInfo = "【" + buyInfo + "】"
                    infoTmp = "[3] {} {} {} game info: {} {} {}".format(gameTime, type_game,addInfo,  main, client, cmd[4])
                    addOutputInfo(gameTime, infoTmp,outputInfo)
                    self.commend.add(main, getTime(gameTime), buyInfo, 3 , rate=rateNow, logInfo=infoTmp, id=gameId)


                def condition_v4(mainFlag, winFlag, lostFlag, cmd):
                    def check(mainFlag, winFlag, lostFlag, cmd):
                        if lostFlag and cmd[5] == 1 :                    
                            return True
                        elif winFlag and cmd[5] == -1 : 
                            return True
                        return False

                    if check(mainFlag, winFlag, lostFlag, cmd) == False:
                        return
                    
                    addInfo = "【" + buyInfo + "】"
                    infoTmp = "[4] {} {} {} game info: {} {} {}".format(gameTime, type_game,addInfo,  main, client, cmd[4])
                    addOutputInfo(gameTime, infoTmp,outputInfo)
                    self.commend.add(main, getTime(gameTime), buyInfo, 4 , rate=rateNow, logInfo=infoTmp, id=gameId)

                def condition_v5(mainFlag, winFlag, lostFlag, cmd):
                    def check(mainFlag, winFlag, lostFlag, cmd):
                        if mainFlag and winFlag and cmd[5] == -1 : 
                            return True                       
                        elif mainFlag == False and winFlag and cmd[5] == 1 : 
                            return True
                        return False

                    if check(mainFlag, winFlag, lostFlag, cmd) == False:
                        return
                    
                    addInfo = "【" + buyInfo + "】"
                    infoTmp = "[5] {} {} {} game info: {} {} {}".format(gameTime, type_game,addInfo,  main, client, cmd[4])
                    addOutputInfo(gameTime, infoTmp,outputInfo)
                    self.commend.add(main, getTime(gameTime), buyInfo, 5 , rate=rateNow, logInfo=infoTmp, id=gameId, game=type_game)

                buyInfo = cmd[3]
                if main != "":
                    winFlag, lostFlag = checkBuy(main, cmd, True)

                    # condition_v3(True, winFlag, lostFlag, cmd)
                    # condition_v4(True, winFlag, lostFlag, cmd)
                    condition_v5(True, winFlag, lostFlag, cmd)

                if client != "":
                    winFlag, lostFlag = checkBuy(client, cmd, False)

                    # condition_v3(False, winFlag, lostFlag, cmd)
                    # condition_v4(False, winFlag, lostFlag, cmd)
                    condition_v5(False, winFlag, lostFlag, cmd)


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
            gameId = ""
            for td in tr.find_all('td', class_="text-right BR0"):
                for a in td.find_all('a', target="_blank"):
                    main = clearStr(a.text)

            for td in tr.find_all('td', class_="text-left"):
                for a in td.find_all('a', target="_blank"):
                    client = clearStr(a.text)

            for div in tr.find_all('div', class_="statusListWrapper"):
                for a in div.find_all('a'):
                    tmp = a.attrs['href']
                    gameIdList = tmp.split('/')
                    gameId = gameIdList[2]


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
            main_corner = 0
            client_corner = 0
            if ("-" in tmp) == False:
                cornerTmp = tmp.split(':')
                main_corner = int(cornerTmp[0])
                client_corner = int(cornerTmp[1])

            idGame = main + "_" + str(gameId)

            input = "'"+ main + "','" + client +"','" + str(main_score) +"','" + str(client_score) + "','"  + str(rate) + "','"+ type_game +"'"
            input += ",'"+  str(main_corner) + "','" + str(client_corner)+ "','" + str(client_corner + main_corner)+ "','" + str(gameTime) +"'" 
            input += ",'{}','{}','{}'".format(idGame, scoreRate, cornerRate)
            self.sql.insert(input, "k_corner", idGame)
            self.commend.check(main, gameTime, main_score, client_score, rate, scoreRate, client_corner + main_corner, cornerRate, id=gameId)



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

            print( index, gameCode[gameIndex][2])
            try:   
                if html.getData("k_corner", gameCode[gameIndex], outputInfo) == False :
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

        # for value in values:
        #     for tmp in outputInfo[value]:
        #         writeFile(tmp)
        
        # outputInfo.clear()
        # info = "================================"
        # writeFile(info)
        # print(tableName, " size:", len(outputInfo))

# try:
#     os.remove(r"result_v3.txt")
# except :
#     pass


def doDayWork():
    print("start do doDayWork")
    
    # _thread.start_new_thread(working,("k_rateBuy_v3",))
    # _thread.start_new_thread(working,("k_compBuy",))
    # _thread.start_new_thread(working,("k_scoreBuy_v2",))
    working("k_rateBuy_v3")
    print("end do doDayWork")


# doDayWork()
# working("k_cornerBuy")
# working("k_rateBuy_v3")