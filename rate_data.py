# coding:utf-8  
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from db.mysql import sqlMgr
import codecs


index = 1
end = 30
year="2017"
month = "09"
scoreTmp = "-"



def clearText(text):
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.replace("\t", "")
    return text

sql = sqlMgr('localhost', 'root', '861217', 'football')
table_name = 'k_rate'

def doBaseInfo(date):
    url = "http://www.365rich.com/KJ/"+date+"/"
    req = requests.get(url)
    s = req.text


    soup = BeautifulSoup(s)
    for tr in soup.find_all('tr'):
        if not tr.has_attr('id'):
            continue
        id = tr.get('id')
        id = id[3:]

        td = tr.find('td', class_='gameName')
        type = td.text
        div = tr.find('div', class_='home')
        main = div.text
        div = tr.find('div', class_='guest')
        client = div.text
        scoreTmp = tr.find('strong')
        scoreTmp = scoreTmp.text
        scoreTmp = clearText(scoreTmp)
        scoreTmp = scoreTmp.split('-')
        if scoreTmp[0] == "":
            continue
        if int(scoreTmp[0]) < 0:
            continue
        main_score = int(scoreTmp[0])

        if int(scoreTmp[1]) < 0:
            continue
        client_score = int(scoreTmp[1])

        start_win_rate = 0
        start_ping_rate = 0
        start_lost_rate = 0

        end_win_rate = 0
        end_ping_rate = 0
        end_lost_rate = 0

        input = "'"+ id + "','" + main + "','" + client +"','" + str(main_score) +"','" + str(client_score) + "','"+ type +"'"
        input += ",'"+  str(start_win_rate) + "','" + str(start_ping_rate)+ "','" + str(start_lost_rate)+"'" 
        input += ",'"+  str(end_win_rate) + "','" + str(end_ping_rate)+ "','" + str(end_lost_rate)+"'" 
        input = clearText(input)
        sql.insert(input, table_name)

def doRate(date):
    url = "http://www.365rich.com/handle/football/1x2.aspx?companyid=0&date="+date
    req = requests.get(url)
    s = req.text
    while not(s.find('i') == -1):
        start_pos = s.find('<i>')
        end_pos = s.find('</i>')
        start_pos +=3
        data = s[start_pos:end_pos]
        dataList = data.split(',')

        id = dataList[1]
        start_win_rate = dataList[3]
        start_ping_rate = dataList[4]
        start_lost_rate = dataList[5]

        end_win_rate = dataList[6]
        end_ping_rate = dataList[7]
        end_lost_rate = dataList[8]

        input = "start_win_rate = '" + start_win_rate + "'"
        input += ", start_ping_rate = '" + start_ping_rate + "'"
        input += ", start_lost_rate = '" + start_lost_rate + "'"
        input += ", end_win_rate = '" + end_win_rate + "'"
        input += ", end_ping_rate = '" + end_ping_rate + "'"
        input += ", end_lost_rate = '" + end_lost_rate + "'"

        sql.update(id,input,table_name)

        end_pos += 4
        s = s[end_pos:]

while (index <= end) :
    day = str(index)
    if index < 10:
        day = "0" + day

    day = year+"-"+month+"-" + day
    print(day, "   start")
    doBaseInfo(day)
    doRate(day)
    print(day, "   ok")
    time.sleep(3)
    index +=1