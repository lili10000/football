# coding:utf-8  
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from db.mysql import sqlMgr


# recordName = "tmp.txt"
# url = 'https://www.dszuqiu.com/diary/20181124'
# req = requests.get(url) 
# s = req.text
# with open(recordName, 'w',encoding='utf-8') as f:
#     f.write(req.text)
key = "k_rate_check"
sql = sqlMgr('localhost', 'root', '861217', 'football')

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
# date = time.strftime('%Y%m%d', time.localtime(time.time()+24*60*60))

check = True
check = False

win_sum = 0
lost_sum = 0
game_sum = 0
buy_main_win = 0
buy_main_lost = 0
buy_client_win = 0
buy_client_lost = 0

rate_compare = 0.5
main_rang = 0.5
rate_max = 1.5

loopSize = 7
if check:
    loopSize = 30

for index in range(loopSize):
    tmp = -1
    if check:
        tmp = index + 1
    date = time.strftime('%Y%m%d', time.localtime(time.time() - tmp*24*60*60))
    
    url = 'https://www.dszuqiu.com/diary/' + date
    url = 'https://www.dszuqiu.com/diary/p.' + str(index + 1) 
    if check:
        url = 'https://www.dszuqiu.com/diary/'+ date  
    # print('start:   ', url)
    req = requests.get(url) 
    data = req.text
    soup = BeautifulSoup(data)
    table = soup.find('table', class_="live-list-table diary-table")
    tbody = table.find('tbody')
    time.sleep(5)

    buySize = 0

    buy_client_win_tmp = 0
    buy_client_lost_tmp = 0
    buy_main_win_tmp = 0
    buy_main_lost_tmp = 0

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
        
        type_game = ''


        for td in tr.find_all('td'):
            # for a in td.find_all('a', target="_blank"):
            type_game = clearStr(td.text)
            break
        
        if '欧' in type_game:
            continue

        for td in tr.find_all('td', class_="text-left"):
            for a in td.find_all('a', target="_blank"):
                client = clearStr(a.text)
            for leagueRank in td.find_all('span', class_="leagueRank"):
                leagueRank_client = int(clearStr(leagueRank.text))
            
        if leagueRank_main == -10:
            continue
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

        try:
            rate = float(rate)
        except Exception as e:
            # print("err:"+ repr(e)+" rate:" + rate)
            continue

        tmp = leagueRank_main - leagueRank_client
        buyTmp = ""
        if tmp > 0 and rate <= -0.5:
            buyTmp = "  买  " + main 
        elif tmp < 0 and rate > 0:
            buyTmp = "  买  " + client 
        else:
            continue  

        print(index+1, main, "vs", client,buyTmp," rate:",rate)

    # print(date,"buy_client   win:",buy_client_win_tmp,"  lost",buy_client_lost_tmp)
if check :
    print("win_sum:",win_sum,"lost_sum",lost_sum)  
    print("buy_main     win:",buy_main_win,"    lost:",buy_main_lost)    
    print("buy_client   win:",buy_client_win,"  lost",buy_client_lost)      





