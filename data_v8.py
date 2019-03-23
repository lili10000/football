# encoding=utf8
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from db.mysql import sqlMgr
import random
import ssl

outputInfo = {}



sql = sqlMgr('localhost', 'root', '861217', 'football')


def addOutputInfo(key, info):
    timeArray= time.strptime('20'+ key, "%Y/%m/%d %H:%M")
    key = int(time.mktime(timeArray))
    if outputInfo.__contains__(key) == False:
        outputInfo[key] = []
    outputInfo[key].append(info)

def getIpList():
    urlTmp = "http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp=电信"
    req = requests.get(urlTmp)
    s = req.text
    ips = s.split('<br>')
    ips.pop(0)
    ips.pop(0)
    ips.pop(len(ips)-1)
    print("get ips size:", len(ips))
    return ips

ipList = []
ipList = getIpList()

def clearStr(str):
    str = str.replace(" ", "")
    str = str.replace("\n", "")
    return str

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



    def __init__(self, url):

        self.sql = sql
        self.soup = BeautifulSoup(self.getHtmlText(url))
        self.url = url
        self.main = []
        self.client = []
        self.score = []
        self.param = []

    def getHtmlText(self, url):

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

        type_game = ""

                 
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
            tds = tr.find_all('td', class_="text-center")
            for tdTmp in tds :
                a = tdTmp.find('a', target="_blank")
                if a == None:
                    continue
                tmp = a.text
                tmp = tmp.replace(" ", "")
                tmp = tmp.replace("+", "")
                sliceTmp = tmp.split('/')
                rate = sliceTmp[0]
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
            self.sql.insert(input, "k_corner")


key = "k_gameDic"

def working(tableName, type = 0):
    index = 1
    end = 40
    
    gameCode = []
    gameCodeAll = sql.queryByTypeAll(key)

    for code in  gameCodeAll:
        dataRecv = sql.queryCount(tableName, code[1])
        gameCount = dataRecv[0][0]
        if  gameCount == 0:
            gameCode.append(code)

    if type == 1:
       gameCode = gameCodeAll  
       end = 2 

    if len(gameCode) == 0 :
        return

    # 买预备=========================
    gameIndex = 0
    global ipList
    while index < end:
        gameIndex = 0
        while gameIndex < len(gameCode) :
            url = "https://www.dszuqiu.com/league/"+str(gameCode[gameIndex][0]) + "/p.1"
            url = url.replace("p.1", "p."+ str(index) )
            
            try:
                html =  parser(url)
                if len(ipList) < 2:
                    ipList = getIpList()
            except:
                # time.sleep(10)
                if len(ipList) < 2:
                    ipList = getIpList()
                # print ("connect err")
                continue

            print( index, gameCode[gameIndex][1])
            try:   
                if html.getData(key, gameCode[gameIndex]) == False :
                    break
            except:
                if len(ipList) < 2:
                    ipList = getIpList()
                # print ("error :")
            # time.sleep(1)
            
            gameIndex += 1
        index += 1

        values = list(outputInfo.keys())
        values.sort()
        for value in values:
            for tmp in outputInfo[value]:
                print(tmp)
        
        outputInfo.clear()
        # print("================================")



# working("k_corner", 1)
working("k_corner")

            
