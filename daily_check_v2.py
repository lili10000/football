# encoding=utf8
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser
# from db.mysql import sqlMgr


def clearStr(str):
    str = str.replace(" ", "")
    str = str.replace("[", "")
    str = str.replace("]", "")
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
            self.rate = 0  
            self.rate_result = 0 
            self.type = ''

    def __init__(self, url):
        req = requests.get(url)
        s = req.text
        # self.sql = sqlMgr('localhost', 'root', '861217', 'football')
        self.soup = BeautifulSoup(s)

    def getData(self):
        index = 0
        for a in self.soup.find_all('a', class_="vMod_matchAnalysisCard") :
            gameType = a['title']

            rate = a.find('span', class_='info_r').text
            forecast = a.find('div', class_='vMod_matchAnalysisCard_bottom').text

            main_rank = -1
            client_rank = -1
            for team in a.find_all('div', class_='team'): 
                info = team.find('i').text

                if '主' in info:
                    main_rank = re.findall("\d+",info)[0]
                if '客' in info:
                    client_rank = re.findall("\d+",info)[0]


            if main_rank == -1 or client_rank == -1:
                continue

            if '胜' in forecast and float(rate) >= 0 and int(main_rank) > int(client_rank):
            # if '胜' in forecast and float(rate) >= 0 :
                print(gameType, "买主")
            elif '负' in forecast and float(rate) < 0 and int(main_rank) < int(client_rank):
            # elif '负' in forecast and float(rate) < 0 :
                print(gameType, "买客")
               



date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
url = 'https://vipc.cn/jczq/singles/'+date+'#start'
html =  parser(url)
html.getData()



