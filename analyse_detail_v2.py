# -*- coding: utf-8 -*-
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from db.mysql import sqlMgr
import random
import ssl
import os
import _thread
from commend import commend
from tool import ipTool
import chardet
from common import gameData
import json
import queue
import cal_rank_today

def addOutputInfo(key, info, outputInfo):
    timeArray= time.strptime('20'+ key, "%Y/%m/%d %H:%M")
    key = int(time.mktime(timeArray))
    if outputInfo.__contains__(key) == False:
        outputInfo[key] = []
    outputInfo[key].append(info)


def writeFile(info):
    # with open(r"result_v3.txt", 'a') as f:
    #     f.write(info + "\n")
        # print(info)
    return 

def clearStr(str):
    str = str.replace(" ", "")
    str = str.replace("/", "")
    str = str.replace("\n", "")
    str = str.replace("[", "")
    str = str.replace("]", "")
    return str

def delNum(str):
    info = filter(lambda x:x not in '0123456789', str)
    info = list(info)
    info = "".join(info)
    return info


def longTime(timeStr):
    timeArray= time.strptime('20'+ timeStr, "%Y/%m/%d %H:%M")
    gameTime = int(time.mktime(timeArray))
    now = int(time.time()) 
    if gameTime - now > 60*60*24:
        return True
    return False
def getTime(timeStr):
    timeArray= time.strptime(timeStr, "%Y-%m-%d %H:%M")
    return int(time.mktime(timeArray))


def getHtmlText(url, ipList):

    def addIp(ipStr):
        proxies =[]
        proxies.append({'http': ipStr,'https': ipStr})
        return proxies

    ipChoice = random.choice(ipList)
    content =""
    try:
        req = requests.get(url,proxies=random.choice(addIp(ipChoice)),timeout=5)
        # req = requests.get(url)
        s = req.content.decode('gbk')

    except Exception as e:
        # print(e)

        ipList.remove(ipChoice)
        raise Exception()
    
    if len(s) < 100:
        ipList.remove(ipChoice)
        raise Exception()
    return s

class parser:
    def __init__(self, url, ipList, sql):

        self.sql = sql
        # self.soup = BeautifulSoup(self.getHtmlText(url, ipList), from_encoding="gb18030")
        self.soup = BeautifulSoup(getHtmlText(url, ipList))
        self.url = url
        self.main = []
        self.client = []
        self.score = []
        self.param = []

        self.commend = commend()
        self.version = 6





    def getData(self, id):
        for title in self.soup.find_all('title') :
            if title.string.find('404') != -1:
                return [None, None, None]
        
        dataList = []

        # print (self.soup.text)
        content = self.soup.find('div', class_="M_box")
        div = content.find('div', class_="M_sub_title")
        teamInfo = []

        gameInfo = gameData()
        for tmp in div.find_all('div', class_="team_name"):
            team = tmp.next_element
            span = tmp.find('span')
            info = span.text
            rank = info[-2:-1]
            teamInfo.append([team, rank])
        
        gameInfo.main = teamInfo[0][0]
        gameInfo.main_rank = teamInfo[0][1]

        gameInfo.client = teamInfo[1][0]
        gameInfo.client_rank = teamInfo[1][1]

        # 历史战绩
        span = self.soup.find('span', class_="f16")
        em = span.find('em', class_="red").text
        gameInfo.his_2_win=int(em[:-1])
        em = span.find('em', class_="green").text
        gameInfo.his_2_ping=int(em[:-1])
        em = span.find('em', class_="blue").text
        gameInfo.his_2_lost=int(em[:-1])

        # 近10场 主队战绩
        div = self.soup.find('div', class_="team_a", id='team_zhanji_1')
        div = div.find('div', class_="bottom_info")
        
        span = div.find('span', class_="mar_left20")
        info = span.find('span', class_="ying").text
        gameInfo.his_main_all_win=int(info[:-1])
        info = span.find('span', class_="ping").text
        gameInfo.his_main_all_ping=int(info[:-1])
        info = span.find('span', class_="shu").text
        gameInfo.his_main_all_lost=int(info[:-1])

        span = span.nextSibling
        info = span.find('span', class_="ying").text
        gameInfo.his_main_all_score=int(info[:-1])
        info = span.find('span', class_="shu").text
        gameInfo.his_main_all_score_lost=int(info[:-1])

        # 近10场 客队战绩
        div = self.soup.find('div', class_="team_b", id='team_zhanji_0')
        div = div.find('div', class_="bottom_info")
        
        span = div.find('span', class_="mar_left20")
        info = span.find('span', class_="ying").text
        gameInfo.his_client_all_win=int(info[:-1])
        info = span.find('span', class_="ping").text
        gameInfo.his_client_all_ping=int(info[:-1])
        info = span.find('span', class_="shu").text
        gameInfo.his_client_all_lost=int(info[:-1])

        span = span.nextSibling
        info = span.find('span', class_="ying").text
        gameInfo.his_client_all_score=int(info[:-1])
        info = span.find('span', class_="shu").text
        gameInfo.his_client_all_score_lost=int(info[:-1])


        # 近10场 主队主场战绩
        div = self.soup.find('div', class_="team_a", id='team_zhanji2_1')
        div = div.find('div', class_="bottom_info")
        
        span = div.find('span', class_="mar_left20")
        info = span.find('span', class_="ying").text
        gameInfo.his_main_1_win=int(info[:-1])
        info = span.find('span', class_="ping").text
        gameInfo.his_main_1_ping=int(info[:-1])
        info = span.find('span', class_="shu").text
        gameInfo.his_main_1_lost=int(info[:-1])

        span = span.nextSibling
        info = span.find('span', class_="ying").text
        gameInfo.his_main_1_score=int(info[:-1])
        info = span.find('span', class_="shu").text
        gameInfo.his_main_1_score_lost=int(info[:-1])

        # 近10场 客队客场战绩
        div = self.soup.find('div', class_="team_b", id='team_zhanji2_0')
        div = div.find('div', class_="bottom_info")
        
        span = div.find('span', class_="mar_left20")
        info = span.find('span', class_="ying").text
        gameInfo.his_client_1_win=int(info[:-1])
        info = span.find('span', class_="ping").text
        gameInfo.his_client_1_ping=int(info[:-1])
        info = span.find('span', class_="shu").text
        gameInfo.his_client_1_lost=int(info[:-1])

        span = span.nextSibling
        info = span.find('span', class_="ying").text
        gameInfo.his_client_1_score=int(info[:-1])
        info = span.find('span', class_="shu").text
        gameInfo.his_client_1_score_lost=int(info[:-1])


        for divMain in self.soup.find_all('div', class_="M_box integral"):
            title = divMain.find('div', class_='M_title').text
            if ('平均数据' in title) == False:
                continue

            for div in divMain.find_all('div', class_="team_a"):
                #主队平均入球
                tr =  div.find('tr', class_="tr1")
                if tr == None:
                    continue

                tmp = []
                for td in tr.find_all('td'):
                    tmp.append(td.text)
                gameInfo.his_main_all_socre = float(tmp[1][:-1])
                gameInfo.his_main_main_socre = float(tmp[2][:-1])
                gameInfo.his_main_client_socre = float(tmp[3][:-1])

                #主队平均丢球
                tr =  div.find('tr', class_="tr2")
                tmp = []
                for td in tr.find_all('td'):
                    tmp.append(td.text)
                gameInfo.his_main_all_socre_lost = float(tmp[1][:-1])
                gameInfo.his_main_main_socre_lost = float(tmp[2][:-1])
                gameInfo.his_main_client_socre_lost = float(tmp[3][:-1])
                break
        
            for div in divMain.find_all('div', class_="team_b"):
                #客队平均入球
                tr =  div.find('tr', class_="tr1")
                if tr == None:
                    continue

                tmp = []
                for td in tr.find_all('td'):
                    tmp.append(td.text)
                gameInfo.his_client_all_socre = float(tmp[1][:-1])
                gameInfo.his_client_main_socre = float(tmp[2][:-1])
                gameInfo.his_client_client_socre = float(tmp[3][:-1])

                #客队平均丢球
                tr =  div.find('tr', class_="tr2")
                tmp = []
                for td in tr.find_all('td'):
                    tmp.append(td.text)
                gameInfo.his_client_all_socre_lost = float(tmp[1][:-1])
                gameInfo.his_client_main_socre_lost = float(tmp[2][:-1])
                gameInfo.his_client_client_socre_lost = float(tmp[3][:-1])
                break
            
        div = self.soup.find('div', id='odds_hd_ls')
        a = div.find('a', class_='hd_name').text
        tmp = a.split('第')
        # gameInfo.type = tmp[0][5:]
        gameInfo.type = delNum(tmp[0])

        tmp = self.soup.find('p', class_='game_time').text
        tmp = getTime(tmp[4:])
        gameInfo.time = tmp

        tmp = self.soup.find('p', class_='odds_hd_bf').text
        tmp = tmp.split(':')
        if len(tmp) == 2:
            gameInfo.main_score = int(tmp[0])
            gameInfo.client_score = int(tmp[1])
        
        overdict = gameInfo.__dict__
        result=json.dumps(overdict)

        input = "'{}','{}','{}'".format(id, gameInfo.type,result)
        self.sql.insert(input, "k_gameInfoDetail", id)


        
            

def threadFun(channel):
    ipObj = ipTool()
    # ipList = ipObj.getIpList()
    sql = sqlMgr('localhost', 'root', '861217', 'football')

    while 1:
        id = channel.get()
        ipList = ipObj.getIpList()
        url = "https://odds.500.com/fenxi/shuju-{}.shtml".format(id)
        while 1:
            try:
                html =  parser(url, ipList, sql)
                html.getData(id)
                print(id,"  ok")
                break
            except Exception as e:
                if len(ipList) < 2:
                    break




def working(start, end):
    
    channel = queue.Queue()
    for i in range(20):
        _thread.start_new_thread(threadFun,(channel,))

    print("start work")
    ipObj = ipTool()
    ipList = ipObj.getIpList()


    for index in range(end - start + 1):
        id = index + start
        channel.put(id)
    time.sleep(60*60)
             


working(783817, 783983)
# threadFun(777206)

