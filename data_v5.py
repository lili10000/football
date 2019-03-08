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

checkFlag = False
whiteList = {}
whiteList["中超"] = 3
whiteList["中超"] = 3

sql = sqlMgr('localhost', 'root', '861217', 'football')

urlTmp = "http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=广东&isp=电信"
req = requests.get(urlTmp)
s = req.text
ipList = s.split('<br>')
ipList.pop(0)
ipList.pop(0)
ipList.pop(len(ipList)-1)

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
        # urlTmp = "http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=广东&isp=电信"
        # req = requests.get(urlTmp)
        # s = req.text
        # ipList = s.split('<br>')
        # ipList.pop(0)
        # ipList.pop(0)
        # ipList.pop(len(ipList)-1)

         
        def addIp(ipStr):
            proxies =[]
            proxies.append({'http': ipStr,'https': ipStr})
            return proxies

        ipChoice = random.choice(ipList)

        try:
            req = requests.get(url,proxies=random.choice(addIp(ipChoice)),timeout=5)
        except:
            ipList.remove(ipChoice)
            print("remove ip, restSize:", len(ipList))
            raise Exception()
        


        s = req.text
        if len(s) < 1000:
            raise Exception()


        self.sql = sql
        self.soup = BeautifulSoup(s)
        self.url = url
        self.main = []
        self.client = []
        self.score = []
        self.param = []

    def getData(self, key):
        for title in self.soup.find_all('title') :
            if title.string.find('404') != -1:
                return False

        type_game = ""

        if checkFlag:
            for tr  in self.soup.find_all('tr', class_='page-1'):
                td = tr.find('td', class_="bg1")
                if td == None:
                    continue
                type_game = td.text
                td = td.findNextSibling('td')
                td = td.findNextSibling('td')
                gameTime = td.text


                main = ""
                client = ""
                for td in tr.find_all('td', class_="text-right BR0"):
                    for a in td.find_all('a', target="_blank"):
                        main = clearStr(a.text)

                for td in tr.find_all('td', class_="text-left"):
                    a = td.find('a', target="_blank")
                    client = clearStr(a.text)
                    break

                

                def checkBuy(teamName):
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
                    for index in range(3):
                        key = values[index]
                        if result[key] == -1:
                            lostSum += 1
                    
                    if lostSum == 3:
                        return True
                    return False

                if main != "" and checkBuy(main):
                    print("buy ",main, ' game info:   ', gameTime, main, client)
                elif client != "" and checkBuy(client):
                    print("buy ",client, ' game info:   ', gameTime, main, client)



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
            self.sql.insert(input, key)



index = 1
end = 40
key = "k_corner"
gameCode = []
# gameCode.append(2) #中超
gameCode.append(187) #法乙
# gameCode.append(35) #英超
# gameCode.append(36) #西甲
# gameCode.append(37) #意甲
# gameCode.append(39) #法甲

# key = "k_163_15_16"
# key = "k_163_14_15"
# key = "k_163_16_17"

gameIndex = 0

while index < end:
    gameIndex = 0
    while gameIndex < len(gameCode) :
        if end == 2:
            checkFlag = True 
        url = "https://www.dszuqiu.com/league/"+str(gameCode[gameIndex]) + "/p.1"
        url = url.replace("p.1", "p."+ str(index) )
        # time.sleep(5 + random.randint(0,5))
        # url = url.replace("indexType=0", "indexType=1")
        print(url)
        
        try:
            html =  parser(url)
            
        except:
            # time.sleep(10)
            print ("connect err")
            continue

        try:   
            if html.getData(key) == False :
                break
        except:
            print ("error :")
        # time.sleep(1)
        index += 1 
        gameIndex += 1
    
            

