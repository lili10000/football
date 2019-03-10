# encoding=utf8
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from db.mysql import sqlMgr
import random

sql = sqlMgr('localhost', 'root', '861217', 'football')

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
        req = requests.get(url)
        s = req.text
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
# gameCode.append(430) #英甲 黑
# gameCode.append(42) #英冠
# gameCode.append(108) #葡超  黑
# gameCode.append(34) #日职联  黑
# gameCode.append(35) #英超
# gameCode.append(36) #西甲
# gameCode.append(38) #德甲
# gameCode.append(37) #意甲
# gameCode.append(39) #法甲

# key = "k_163_15_16"
# key = "k_163_14_15"
# key = "k_163_16_17"
for code in gameCode :
    while index < end:

        url = "https://www.dszuqiu.com/league/"+str(code) + "/p.1"
        url = url.replace("p.1", "p."+ str(index) )
        time.sleep(5 + random.randint(0,5))
        # url = url.replace("indexType=0", "indexType=1")
        print(url)
        
        try:
            html =  parser(url)
        except:
            time.sleep(10)
            print ("connect err")
            continue

        try:   
            if html.getData(key) == False :
                break
        except:
            print ("error :")
        # time.sleep(1)
        index += 1
        

