# encoding=utf8
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from db.mysql import sqlMgr
import json 


class parser:
    class gameData:
        def __init__(self):
            
            self.main = ''     
            self.client = ''     
            self.main_score = 0  
            self.client_score = 0   
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
            for score in tag.find_all('p', class_="score") :
                data.main_score = int(score.string[:1].lower())
                data.client_score = int(score.string[4:].lower())

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

            if data.main_score > data.client_score :
                data.result = 1
            elif  data.main_score == data.client_score :
                data.result = 0
            else :
                data.result = -1

            input = "'"+ data.main + "','" + data.client +"','" + str(data.main_score) +"','" + str(data.client_score) + "','" + str(data.result) + "','" + str(data.type)+"'"
            input += ",'"+  str(data.win_rate) + "','" + str(data.lost_rate)+ "','" + str(data.tie_rate)+"'"
            input += ",'"+  str(data.win_rate_first) + "','" + str(data.lost_rate_first)+ "','" + str(data.tie_rate_first)+"'"

            self.sql.insert(input, "k_rate_euro")
            return True



# timeStart = datetime.strptime("2017-05-23",'%Y-%m-%d')
# timeEnd = datetime.strptime("2017-05-24",'%Y-%m-%d')
# startUnix = time.mktime(timeStart.timetuple())
# endUnix = time.mktime(timeEnd.timetuple())


def getTodayData() :
    endUnix = time.time()
    startUnix = endUnix - 3600 * 24

    date = time.strftime('%Y%m%d', time.localtime(startUnix))
    dayOfWeek = time.strftime("%w",time.localtime(startUnix))
    if dayOfWeek == '0':
        dayOfWeek = '7'

    for index in range(100) :
        num = ""
        if index < 9 :
            num = "00" + str(index+1)
        elif index < 99:
            num = "0" + str(index+1)
        url = 'https://vipc.cn/jczq/single/'+date+dayOfWeek+ num
        urlData = 'https://vipc.cn/i/jczq/single/'+date+dayOfWeek+ num+'/odds/euro'
        print(url, urlData)
        
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



SECONDS_PER_DAY = 24 * 60 * 60
 
def getSleepTime():
    from datetime import datetime, timedelta
    curTime = datetime.now()
    desTime = curTime.replace(hour=13, minute=0, second=0, microsecond=0)
    delta = curTime - desTime
    skipSeconds = SECONDS_PER_DAY - delta.total_seconds()
    print ("Must sleep %d seconds" % skipSeconds)
    return skipSeconds

        
while 1:
    sleepTime = getSleepTime()
    time.sleep(sleepTime)
    getTodayData()

