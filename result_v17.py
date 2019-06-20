import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from db.mysql import sqlMgr
import random
import ssl
import os
from commend import commend
from tool import ipTool
import threading
import json

class parser:
    def __init__(self, url, ipList):
        # self.sql = sql
        self.soup = BeautifulSoup(self.getHtmlText(url, ipList))
        self.url = url
        # self.commend = commend()
        # self.version = 1

    def __getRate(self, info):
        rateList = info.split("/")
        if len(rateList) < 2:
            return float(rateList[0])
        return float(rateList[0]) + 0.25
        

    def getHtmlText(self, url, ipList):
        def addIp(ipStr):
            proxies =[]
            proxies.append({'http': ipStr,'https': ipStr})
            return proxies
        ipChoice = random.choice(ipList)

        try:
            # req = requests.get(url,proxies=random.choice(addIp(ipChoice)),timeout=3)
            req = requests.get(url)
        except:
            ipList.remove(ipChoice)
            # print("remove ip, restSize:", len(ipList))
            raise Exception()
        
        s = req.text
        if len(s) < 100:
            ipList.remove(ipChoice)
            # print("remove ip, restSize:", len(ipList))
            raise Exception()
        return s

    def getData(self):
        for title in self.soup.find_all('title') :
            if title.string.find('404') != -1:
                return 
        divs = []

        for div in self.soup.find_all('div', class_="small-12 medium-4 columns tableCol3in1"):
            divs.append(div)

        tbody = divs.find("tbody")
        rateList = []
        for tr in tbody.find_all("tr"):
            tds = tr.find_all("td")
            main = float(tds[0])
            rate = self.__getRate(tds[1])
            client = float(tds[2])
            rateList.append([main, rate, client])






def updata(code):
    ipObj = ipTool()
    ipList = ipObj.getIpList()
    url = "https://www.dszuqiu.com/race/baijia/{}?t=8".format(code) 
    print(url)
    while 1:
        
        try:
            html =  parser(url, ipList)
            if len(ipList) < 2:
                ipList = ipObj.getIpList()
        except:
            if len(ipList) < 2:
                ipList = ipObj.getIpList()
            continue
        return html.getData()


updata(630237)