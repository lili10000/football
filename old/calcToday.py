# encoding=utf8
import requests
import re
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from db.mysql import sqlMgr
import json 


# os.mknod("today.txt") 
file_object = open('today.txt' ,'w')

class parser:
    class gameData:
        def __init__(self):
            
            self.main = ''     
            self.client = ''     
            self.result = 0  
            self.type = ''
            self.win_rate = 0
            self.lost_rate = 0
            self.tie_rate = 0
            self.win_rate_first = 0
            self.lost_rate_first = 0
            self.tie_rate_first = 0

    def __init__(self, url, urlData):
        req = requests.get(url)
        s = req.text
        self.sql = sqlMgr('localhost', 'root', '861217', 'football')
        self.soup = BeautifulSoup(s)

        # self.url = url
        self.urlData = urlData

    def getData(self):
        for title in self.soup.find_all('title') :
            if title.string.find('404') != -1:
                return False


        index = 0
        for tag in self.soup.find_all('div', class_="vMatch2_info_header") :
            data = self.gameData()

            for main in tag.find_all('div', class_="team", style='left: 10px;') :
                data.main = main.b.string
            for client in tag.find_all('div', class_="team", style='right: 10px;') :
                data.client = client.b.string


            for gameType in tag.find_all('span', style='text-align: left;'): 
                tmp = gameType.text
                tmp = tmp.replace("\n", "")
                tmp = tmp.replace(" ", "")
                tmp = tmp.replace("主", "")
                data.type = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", tmp)


            req = requests.get(self.urlData)
            jsonData = json.loads(req.text) 

            index = 0
            if jsonData["odds"][index]['firstOdds'][0] == "NaN.00" :
                index = 1
            if len(jsonData["odds"]) == 1 :
                return True

            data.win_rate_first = float(jsonData["odds"][index]['firstOdds'][0])
            data.tie_rate_first = float(jsonData["odds"][index]['firstOdds'][1])
            data.lost_rate_first = float(jsonData["odds"][index]['firstOdds'][2])
            data.win_rate = float(jsonData["odds"][index]['odds'][0])
            data.tie_rate = float(jsonData["odds"][index]['odds'][1])
            data.lost_rate = float(jsonData["odds"][index]['odds'][2])

            change_min = abs(data.win_rate_first - data.win_rate)/data.win_rate_first
            change = abs(data.lost_rate_first - data.lost_rate)/data.lost_rate_first
            if change_min > change :
                change_min = change


            # input = "'"+ data.main + "','" + data.client  + "','" + str(data.type)+"'"
            # input += ",'"+  str(data.win_rate) + "','" + str(data.lost_rate)+ "','" + str(data.tie_rate)+"'"
            # input += ",'"+  str(data.win_rate_first) + "','" + str(data.lost_rate_first)+ "','" + str(data.tie_rate_first)+"'"

            all_the_text = data.type + "   " + data.main + "    " + data.client + " min =" + str(round(change_min,2)) + "\n"
            file_object.write(all_the_text)
            # self.sql.insert(input, "k_rate_euro")
            return True



date = time.strftime('%Y%m%d', time.localtime(time.time()))
dayOfWeek = time.strftime("%w",time.localtime(time.time()))
if dayOfWeek == '0':
    dayOfWeek = '7'



for index in range(150) :
    print(index)
    num = ""
    if index < 9 :
        num = "00" + str(index+1)
    elif index < 99:
        num = "0" + str(index+1)
    url = 'https://vipc.cn/jczq/single/'+date+dayOfWeek+ num
    urlData = 'https://vipc.cn/i/jczq/single/'+date+dayOfWeek+ num+'/odds/euro'
    # print(url, urlData)
    
    try:
        html =  parser(url, urlData)
    except :
        time.sleep(10)
        print ("connect err")
        continue

    try:   
        if html.getData() == False :
            break
    except:
        print ("error :")
    time.sleep(1)
    
file_object.close()
print("end")