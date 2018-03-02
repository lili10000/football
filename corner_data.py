# coding:utf-8  
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from db.mysql import sqlMgr

def clearText(text):
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.replace("\t", "")
    return text


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
        tmp = self.soup.find('ol', class_="breadcrumb big_breadcrumb")
        type = tmp.find('li', class_="active")
        tmp=''
        type=clearText(type.text)
        for tb in self.soup.find_all('table', class_="table table-striped table-bordered table-condensed table-hover background_table"):
            for tr in tb.find_all('tr'):
                check=False
                tmp = tr.find('td', class_="text-center match_status")
                if tmp == None:
                    continue

                tmp = clearText(tmp.text)
                if tmp == "全":
                    check=True
                if check==False:
                    continue
                main = tr.find('td', class_="text-right")
                main=clearText(main.text)

                left = tr.find('td', class_="text-left")
                client = left.find('a')
                client = clearText(client.text)

                score = tr.find('td', class_="text-center match_goal")
                scoreTmp =clearText(score.text)
                scoreTmp = scoreTmp.split('-')
                if int(scoreTmp[0]) < 0:
                    continue
                main_score = int(scoreTmp[0])

                if int(scoreTmp[1]) < 0:
                    continue
                client_score = int(scoreTmp[1])

                corner = tr.find('td', class_="text-center match_corner")
                corner = clearText(corner.text)
                cornerTmp = corner.split('-')
                main_corner = int(cornerTmp[0])
                client_corner = int(cornerTmp[1])

                tmp = tr.find_all('td', class_="text-center")
                rate = tmp[3]
                rate = clearText(rate.text)
                rates = rate.split(',')
                if len(rates) == 1:
                    rate = float(rates[0])
                else:
                    rate = (float(rates[0]) + float(rates[1]))/2


                input = "'"+ main + "','" + client +"','" + str(main_score) +"','" + str(client_score) + "','"  + str(rate) + "','"+ type +"'"
                input += ",'"+  str(main_corner) + "','" + str(client_corner)+ "','" + str(client_corner + main_corner)+"'" 

                self.sql.insert(input, key)



index = 1
end = 20
key = "k_corner"

while (index < end) :
    
    url = "http://jq.chewtang.com/league/view/17/page:1"
    url = url.replace("page:1", "page:"+ str(index) )
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
        

