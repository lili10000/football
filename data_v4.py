# encoding=utf8
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from db.mysql import sqlMgr



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



    def __init__(self, url):
        req = requests.get(url)
        s = req.text
        self.sql = sqlMgr('localhost', 'root', '861217', 'football')
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
        for h1 in self.soup.find_all('h1') :
            for span in h1.find_all('span') :
                type_game = span.text

        index = 0
        for tag in self.soup.find_all('table', class_="tabList titTwoRow") :

            for main in tag.find_all('td', class_="texRight") :
                self.main.append(main.a.get('title'))
            for client in tag.find_all('td', class_="texLeft") :
                self.client.append(client.a.get('title'))
            for score in tag.find_all('td') :
                if score.get('hostid') == None :
                    continue
                self.score.append(score.text)
            for param in tag.find_all('span') :
                self.param.append(param.text)


            for index in range(len(self.main)) :
                data = self.gameData()

                if len(self.score) != len(self.main):
                    break
                
                # scoreStr = (self.score[index])
                if self.score[index].find(':') == -1 :
                    continue

                scoreTmp = (self.score[index]).split(':'); 

                if int(scoreTmp[0]) < 0:
                    continue
                data.main_score = int(scoreTmp[0])

                if int(scoreTmp[1]) < 0:
                    continue

                data.client_score = int(scoreTmp[1])

                data.main = self.main[index]
                data.client = self.client[index]
                data.type = type_game
                if len(self.param[index*3]) == 0 or self.param[index*3] == "-"or self.param[index*3 + 1] == "-"or self.param[index*3 + 2] == "-" :
                    continue
                data.win_rate = self.param[index*3 + 0]
                data.rate = float(self.param[index*3 + 1])
                data.lost_rate = self.param[index*3 + 2]

                if data.main_score > data.client_score :
                    data.result = 1
                elif  data.main_score == data.client_score :
                    data.result = 0
                else :
                    data.result = -1
            
                if data.main_score + data.rate > data.client_score :
                    data.rate_result = 1
                elif  data.main_score + data.rate == data.client_score :
                    data.rate_result = 0
                else :
                    data.rate_result = -1

                input = "'"+ data.main + "','" + data.client +"','" + str(data.main_score) +"','" + str(data.client_score) + "','" + str(data.result)+ "','" + str(data.rate_result)+ "','" + str(data.rate) + "','" + str(data.type)+"'"
                input += ",'"+  str(data.win_rate) + "','" + str(data.lost_rate)+"'"

                self.sql.insert(input, key)



index = 1
end = 9
key = "k_163"
# key = "k_163_15_16"
# key = "k_163_14_15"
# key = "k_163_16_17"
while (index < end) :
    
    url = "http://saishi.caipiao.163.com/89/13403.html?weekId=1&groupId=&roundId=39675&indexType=0&guestTeamId="
    url = url.replace("weekId=1", "weekId="+ str(index) )
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
        

