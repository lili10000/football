# encoding=utf8
# import urllib.request
from bs4 import BeautifulSoup
import requests
import time
# from gzip import GzipFile
from io import StringIO
import gzip
import requests
import random
import ssl
import json
import queue
from db.mysql import sqlMgr
from commend import commend
import threading



class ipTool:
    def __init__(self):

        self.loopSize = 0

    def getIpList(self):
        while 1:
            try:
                urlTmp = "http://www.89ip.cn/tqdl.html?api=1&num=10&port=&address=&isp=电信"
                req = requests.get(urlTmp)
                s = req.text
                ips = s.split('<br>')
                if len(ips) == 0:
                    time.sleep(3)
                    return ips
                ips.pop(0)
                if len(ips) == 0:
                    time.sleep(3)
                    return ips
                ips.pop(0)
                if len(ips) == 0:
                    time.sleep(3)
                    return ips
                ips.pop(len(ips)-1)
                # print("get ips size:", len(ips))
                if len(ips) == 0:
                    time.sleep(3)
                    return ips
                return ips
            except :
                time.sleep(5)
                pass
            


    # def getIpList(self):
    #     id = 1356
    #     compare = 1553961600
    #     now  = int(time.time()) 
    #     add = int((now - compare) / (60*60*12))
    #     startId = id + add - self.loopSize

    #     url = 'http://www.xsdaili.com/dayProxy/ip/{}.html'.format(startId)
    #     headers ={"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:36.0) Gecko/20100101 Firefox/36.0",
    #             "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    #             #"Accept-Language":"en-US,en;q=0.5",
    #             "Accept-Encoding":"gzip, deflate",
    #             #"Connection":"keep-alive",
    #             "Content-Type":"application/x-www-form-urlencoded",
    #             }
    #     req = requests.get(url,headers=headers,timeout=5)
    #     soup = BeautifulSoup(req.text)
    #     ips = []
    #     ipList = []
    #     for title in soup.find_all('div',class_="cont") :
    #         content = title.contents
    #         for info in content:
    #             if len(info) < 10:
    #                 continue

    #             info = info.replace("\r", "")
    #             info = info.replace("\t", "")
    #             info = info.replace("\n", "")
    #             end = info.find('@')
    #             if end == -1:
    #                 continue
    #             ip = info[0:end]
    #             ipList.append(ip)
    #         self.loopSize -= 1
    #         print("ipList size:", len(ipList))
    #         return ipList


def clearStr(str):
    str = str.replace(" ", "")
    str = str.replace("\r", "")
    str = str.replace("\n", "")
    return str

def addIp(ipStr):
    proxies =[]
    proxies.append({'http': ipStr,'https': ipStr})
    return proxies

def getHtmlText(url, ipList):
    
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


def updateGameDic():
    ipObj = ipTool()
    ipList = ipObj.getIpList()
    url = "https://liansai.500.com/zuqiu-5114/"
    sql = sqlMgr('localhost', 'root', '861217', 'football')
    while 1:
        try:
            soup = BeautifulSoup(getHtmlText(url, ipList), features="html.parser")
            select = soup.find('select', id='select_notcups')
            info = []
            for option in select.find_all('option'):
                value = option.attrs['value']
                gameType = option.text
                gameType = gameType[2:]
                info.append([value, gameType])
            info.pop(0)

            sql.cleanAll('k_gamedic_v2')
            for data in info:
                input = "'{}','{}',''".format(data[0], data[1])
                
                sql.insert(input, 'k_gamedic_v2')
            return

        except Exception as e:
            if len(ipList) < 2:
                ipList = ipObj.getIpList()
            continue



def getData(subUrl, channelOut):
    req = ""
    ipObj = ipTool()
    ips = ipObj.getIpList()
    while 1:
        try:
            req = requests.get(subUrl,proxies=random.choice(addIp(random.choice(ips))),timeout=5)
            req = clearStr(req.text)
            # print("ok",subUrl)
        except Exception as e:
            if len(ips) < 2:
                ips = ipObj.getIpList()
            continue
        break
    channelOut.put(req)

def getGameCodeList(url):

    # channel = queue.Queue()
    channelOut = queue.Queue()

    jifenId = url.split("jifen-")
    jifenId = jifenId[1][:-1]

    ipObj = ipTool()
    ipList = ipObj.getIpList()
    
    # sql = sqlMgr('localhost', 'root', '861217', 'football')

    codeList = []

    threadPool = []


    while 1:
        try:
            soup = BeautifulSoup(getHtmlText(url, ipList), features="html.parser")
            group = 1
            for li in soup.find_all('li', class_='on'):
                a = li.find('a')
                group = 1
                if a.attrs.__contains__('data-group'):
                    group = int(a.attrs['data-group'])
            print("need get data size:",group)
            for index in range(group):
                subUrl = "https://liansai.500.com/index.php?c=score&a=getmatch&stid={}&round={}".format(jifenId, index + 1)
                # _thread.start_new_thread(getData,(subUrl, channelOut, ))
                t=threading.Thread(target=getData,args=(subUrl, channelOut))
                t.start()
                threadPool.append(t)

            for t in threadPool:
                t.join()

            while not channelOut.empty():
                try:
                    req = channelOut.get() 
                    # print("recv data")                   
                    jsonObj = json.loads(req)
                    for obj in jsonObj:
                        codeList.append(obj['fid'])
                except Exception as e:
                    print(e)
            break

        except Exception as e:
            if len(ipList) < 2:
                ipList = ipObj.getIpList()
            continue

    return codeList

# url = "https://liansai.500.com/zuqiu-5114/jifen-13894/"
# getGameCodeList(url)
