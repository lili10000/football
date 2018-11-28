# coding:utf-8  
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser

# recordName = "tmp.txt"
# url = 'https://www.dszuqiu.com/diary/20181124'
# req = requests.get(url) 
# s = req.text
# with open(recordName, 'w',encoding='utf-8') as f:
#     f.write(req.text)

def clearStr(str):
    str = str.replace(" ", "")
    str = str.replace("[", "")
    str = str.replace("]", "")
    str = str.replace("\n", "")
    return str

# recordFile = {}


# data = ""
# with open(recordName, 'r',encoding='utf-8') as f:
#     data = f.read()

url = 'https://www.dszuqiu.com/diary'
req = requests.get(url) 
data = req.text
soup = BeautifulSoup(data)
table = soup.find('table', class_="live-list-table diary-table")
tbody = table.find('tbody')

for index in range(1):
    win_sum = 0
    lost_sum = 0
    game_sum = 0
    for tr in soup.find_all('tr') :

        # td = tr.find('td', class_="BR0 text-center red-color PL0 PR0")
        # if td == None:
        #     continue
        # score = td.text

        # score = score.replace(" ", "")
        # scoreTmp = score.split(':')

        # if int(scoreTmp[0]) < 0:
        #     continue
        # main_score = int(scoreTmp[0])

        # if int(scoreTmp[1]) < 0:
        #     continue
        # client_score = int(scoreTmp[1])

        
        main = ""
        client = ""
        leagueRank_main = -10
        leagueRank_client = -10
        
        for td in tr.find_all('td', class_="text-right BR0"):
            for a in td.find_all('a', target="_blank"):
                main = clearStr(a.text)
            for leagueRank in td.find_all('span', class_="leagueRank"):
                leagueRank_main = int(clearStr(leagueRank.text))
            

        for td in tr.find_all('td', class_="text-left"):
            for a in td.find_all('a', target="_blank"):
                client = clearStr(a.text)
            for leagueRank in td.find_all('span', class_="leagueRank"):
                leagueRank_client = int(clearStr(leagueRank.text))
            

        rank = 1 + index
        rank = 1
        tmp = leagueRank_main - leagueRank_client
        if  tmp < rank:
            continue

        game_sum += 1
        rate = 0
        tds = tr.find_all('td', class_="text-center yellowTd BR0")
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

        compareRate = float(-1 + 0.25*index)
        if rate != '0.25':
            continue
        
        print(main, "vs", client," rate:",rate)



