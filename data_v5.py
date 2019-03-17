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

checkFlag = True
# checkFlag = False


whiteList = {}
whiteList["意乙"] = 2
# whiteList["法乙"] = 4
whiteList["巴甲"] = 2
whiteList["法甲"] = 2
whiteList["西甲"] = 2
whiteList["苏超"] = 2
whiteList["荷乙"] = 2
whiteList["德甲"] = 4
whiteList["韩k联"] = 2
whiteList["波兰甲"] = 4
whiteList["马来超"] = 4
whiteList["泰超"] = 4
whiteList["伊朗超"] = 2
whiteList["俄超"] = 2
whiteList["土超"] = 2
whiteList["阿甲"] = 2





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
        self.soup = BeautifulSoup(self.getHtmlText())
        self.url = url
        self.main = []
        self.client = []
        self.score = []
        self.param = []



    def getHtmlText(self):

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
                    checkSum = 3
                    if whiteList.__contains__(teamName):
                        checkSum = whiteList[teamName]

                    for index in range(checkSum):
                        key = values[index]
                        if result[key] == -1:
                            lostSum += 1
                    
                    if lostSum == checkSum :
                        return True
                    return False

                addInfo = "【" + cmd + "】"



                if main != "" and checkBuy(main, cmd):
                    infoTmp = type_game + " " + addInfo + "   <" + main + "> game info:   " + str(gameTime) + " " + main + " " + client
                    addOutputInfo(gameTime, infoTmp)
                    # print(addInfo, "<",main, '> game info:   ', gameTime, main, client)
                elif client != "" and checkBuy(client, cmd):
                    infoTmp = type_game + " " + addInfo + "   <" + client + "> game info:   " + str(gameTime) + " " + main + " " + client
                    addOutputInfo(gameTime, infoTmp)
                    


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
end = 80
if checkFlag:
    end = 2



key = "k_corner"
gameCode = []

# 买小
info = "让球胜 + 小球"
gameCode.append([251, "巴甲", info]) 
gameCode.append([39,"法甲", info]) 
gameCode.append([157,"意乙", info]) 
gameCode.append([40, "荷甲", info]) 
# gameCode.append([38, "德甲", info + " + 大角"]) #
gameCode.append([654, "阿甲", info]) #
# # 买大
info = "让球胜 + 大球"
gameCode.append([251, "中超", info + " + 大角"]) 
gameCode.append([42,"英冠", info + " + 小角"]) 
gameCode.append([36,"西甲", info])

# # 买
info = "让球胜"
gameCode.append([35,"英超", info + " + 小角"]) 
# gameCode.append([649, "德乙", info])

# 买输
info = "让球输"
gameCode.append([182, "苏超", info + " + 小角"]) # 输
gameCode.append([1000, "墨春联", info + " + 小角"])
gameCode.append([430, "英甲", info])

# # 买输小
info = "让球输 + 小球"
gameCode.append([252, "美职联", info + " + 小角"]) #输小
gameCode.append([214, "巴西乙", info + " + 小角"])

# 纯大
info = "大球"
# gameCode.append([85, "韩k联", info]) #纯大
# gameCode.append([37,"意甲", info + " + 小角"])
# gameCode.append([158, "土超", info]) #
# gameCode.append([607, "墨秋联", info + " + 小角"] )
# 纯小
info = "小球"
# gameCode.append([151, "以超", info + " + 小角"]) #纯小
# gameCode.append([226, "马来超", info]) #
# gameCode.append([1810, "荷乙", info + " + 小角"]) # 纯小
# gameCode.append([653, "伊朗超", info + " + 小角"]) #
# gameCode.append([8, "俄超", info + " + 小角"]) #
# gameCode.append([187, "法乙", info + " + 小角"]) 
# gameCode.append([3,"澳超", info + " + 大角"]) 
# gameCode.append([108, "葡超", info])
# gameCode.append([460, "英乙", info])
# 买预备=========================
# 纯大

# 纯小

# 黑预备






# 黑==========
# gameCode.append([244, "波兰甲", 0]) #
# gameCode.append([402, "泰超", 4]) #输小
# gameCode.append([34,"日职联", True]) 
# gameCode.append([134, "捷甲", 0]) #
# gameCode.append([1275, "日职乙", 0]) #
# check


gameIndex = 0


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
            if html.getData(key, gameCode[gameIndex][2]) == False :
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