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
    str = str.replace("[", "")
    str = str.replace("]", "")
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
        self.version = 6

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

    def getData(self, key, cmd):
        for title in self.soup.find_all('title') :
            if title.string.find('404') != -1:
                return False
                    
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
            main_corner = 0
            client_corner = 0

            if ("-" in tmp) == False:
                cornerTmp = tmp.split(':')
                main_corner = int(cornerTmp[0])
                client_corner = int(cornerTmp[1])
            
            leagueRank_main = -10
            leagueRank_client = -10
        
            for td in tr.find_all('td', class_="text-right BR0"):
                for leagueRank in td.find_all('span', class_="leagueRank"):
                    leagueRank_main = int(clearStr(leagueRank.text))

            for td in tr.find_all('td', class_="text-left"):
                for leagueRank in td.find_all('span', class_="leagueRank"):
                    leagueRank_client = int(clearStr(leagueRank.text))
            
            input = "'{}','{}','{}','{}','{}','{}','{}'".format(gameId, main, client, main_score, client_score, rate, scoreRate)
            input += ",'{}','{}','{}','{}'".format(leagueRank_main, leagueRank_client, type_game, gameTime)
            self.sql.insert(input, "k_baseAnaylse")

            
def working(tableName):
    sql = sqlMgr('localhost', 'root', '861217', 'football')
    ipObj = ipTool()
    ipList = ipObj.getIpList()
    index = 1
    end = 40

    gameCode = []
    gameCodeAll = sql.queryByTypeAll("k_gameDic_v2")

    for code in  gameCodeAll:
        dataRecv = sql.queryCount(tableName, code[1])
        gameCount = dataRecv[0][0]
        if  gameCount < end*9:
            gameCode.append(code)

    if type == 1:
       gameCode = gameCodeAll  
       end = 2

    if len(gameCode) == 0 :
        return
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

            print( index, gameCode[gameIndex][1])
            try:   
                if html.getData(tableName, gameCode[gameIndex]) == False :
                    break
            except:
                if len(ipList) < 2:
                    ipList = ipObj.getIpList()
                # print ("error :")
            # time.sleep(1)
            
            gameIndex += 1
        index += 1




working("k_baseAnaylse")



