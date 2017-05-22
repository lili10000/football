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
            self.rate = 0  
            self.rate_result = 0 
            self.type = ''

    def __init__(self, url):
        req = requests.get(url)
        s = req.text
        self.sql = sqlMgr('localhost', 'root', '861217', 'football')
        self.soup = BeautifulSoup(s)

    def getData(self):
        index = 0
        for tag in self.soup.find_all('div', class_="vMatch2_indexList_item_main") :
            data = self.gameData()

            

            for teamInfo in tag.find_all('div', class_="team_info"): 
                for team in teamInfo.find_all('span'): 
                    if index %2 == 0:
                        data.main = team.string
                    else :
                        data.client = team.string
                    index += 1
                for gameType in teamInfo.find_all('i'): 
                    tmp = gameType.string.lower()
                    data.type = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", tmp)
                    

            for score in tag.find_all('span', class_="socre_a"):
                scoreTmp = score.string[:1].lower()
                data.main_score = int(scoreTmp)

                scoreTmp = score.string[4:].lower()
                data.client_score = int(scoreTmp)
            for rate in tag.find_all('span', class_="score_r"):
                data.rate = int(rate.string.lower())

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
            self.sql.insert(input, "k_all")



timeStart = datetime.strptime("2014-01-01",'%Y-%m-%d')
timeEnd = datetime.strptime("2014-12-31",'%Y-%m-%d')
startUnix = time.mktime(timeStart.timetuple())
endUnix = time.mktime(timeEnd.timetuple())
while (startUnix < endUnix) :
    date = time.strftime('%Y-%m-%d', time.localtime(startUnix))
    url = 'https://vipc.cn/jczq/singles/'+date+'#start'
    html =  parser(url)
    html.getData()
    
    startUnix += 3600 * 24


print("end")


