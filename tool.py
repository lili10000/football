# encoding=utf8
# import urllib.request
from bs4 import BeautifulSoup
import requests
import time
# from gzip import GzipFile
from io import StringIO
import gzip



class ipTool:
    def __init__(self):

        self.loopSize = 0

    def getIpList(self):
        urlTmp = "http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp=电信"
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
        print("get ips size:", len(ips))
        if len(ips) == 0:
            time.sleep(3)
            return ips

        return ips


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
