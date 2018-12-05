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

check = True
check = False

url = 'https://www.dszuqiu.com/diary'
if check:
    url = 'https://www.dszuqiu.com/diary/20181204'
    
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
        main_score = -1
        client_score = -1
        if check:
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
            
        if leagueRank_main == -10:
            continue

        rank = 1 + index
        rank = 1
        tmp = leagueRank_main - leagueRank_client
        rateValid = 0
        if  tmp <= -10:
            rateValid = -0.75
        elif tmp <= -5:
            rateValid = -0.5
        elif tmp <= 0:
            rateValid = -0.25
        elif tmp <= 5:
            rateValid = 0.25
        elif tmp <= 10:
            rateValid = 0.5  
        else:
            rateValid = 0.75

        rateValid -= 0.25


        game_sum += 1
        rate = 0
        
        tds = tr.find_all('td', class_="text-center yellowTd BR0")
        if check :
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


        rateTmp = 0
        try:
            rate = float(rate)
            rateTmp = rateValid - rate
            if abs(rateTmp) < 0.5:
                continue
            if abs(rate) > 1.25:
                continue
        except Exception as e:
            # print("err:"+ repr(e)+" rate:" + rate)
            continue



        buyTmp = ""
        if rateTmp >= 0.5:
            buyTmp = "  买  " + client 
        elif rateTmp <= -0.5:
            buyTmp = "  买  " + main 

        if check == False:
            print(main, "vs", client,buyTmp," rate:",rate)

        if check :
            main_win = True
            result = False
            if main_score - client_score + rate < 0:
                main_win = False 
            elif main_score - client_score + rate == 0:
                continue
                
            if rateTmp >= 0.5 and main_win == False:
                win_sum += 1
                result = True
            elif rateTmp <= -0.5 and main_win == True:
                win_sum += 1
                result = True
            else:
                lost_sum += 1
        
            if result :
                result = "赢"
            else:
                result = "输"

            print(main, "vs", client,buyTmp," rate:",rate,result)

    if check :
        print("win_sum:",win_sum,"lost_sum",lost_sum)        






