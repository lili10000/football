# encoding=utf8
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from db.mysql import sqlMgr



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
            self.rate = 0
            self.win_rate = float(0)
            self.lost_rate = float(0)
            self.tie_rate = float(0)
            self.lost_rate_balance = float(0)
            self.tie_rate_balance = float(0)

    def __init__(self, url):
        req = requests.get(url)
        s = req.text
        self.sql = sqlMgr('localhost', 'root', '861217', 'football')
        self.soup = BeautifulSoup(s)
        self.url = url

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


        for tag in self.soup.find_all('table', class_="vMatch2_experts_officialOdds_table main") :

            for td in tag.find_all('td') :
                rate = td.find('span')
                if rate == None:
                    continue
                scoreTmp = rate.string.lower()
                if td.text.find("让胜") != -1  :
                    data.win_rate_balance = float(scoreTmp)
                elif td.text.find("胜") != -1  :
                    data.win_rate = float(scoreTmp)
                elif td.text.find("让平") != -1  :
                    data.tie_rate_balance = float(scoreTmp)
                elif td.text.find("平") != -1  :
                    data.tie_rate = float(scoreTmp)
                elif td.text.find("让负") != -1  :
                    data.lost_rate_balance = float(scoreTmp)
                elif td.text.find("负") != -1  :
                    data.lost_rate = float(scoreTmp)

            for rateTmp in tag.find_all('span', class_="red") :
                # print(rateTmp.string)
                data.rate = int(rateTmp.string.lower())
                # print(data.rate)

            if data.main_score > data.client_score :
                data.result = 1
            elif  data.main_score == data.client_score :
                data.result = 0
            else :
                data.result = -1
            
            if data.main_score + data.rate > data.client_score :
                data.rate_result = 1
            elif  data.main_score + data.rate == data.client_score :
                data.rate_result = 0
            else :
                data.rate_result = -1

            input = "'"+ data.main + "','" + data.client +"','" + str(data.main_score) +"','" + str(data.client_score) + "','" + str(data.result)+ "','" + str(data.rate_result)+ "','" + str(data.rate) + "','" + str(data.type)+"'"
            input += ",'"+  str(data.win_rate) + "','" + str(data.lost_rate)+ "','" + str(data.tie_rate)+"'"
            input += ",'"+  str(data.win_rate_balance) + "','" + str(data.lost_rate_balance)+ "','" + str(data.tie_rate_balance)+"'"

            self.sql.insert(input, "k_all_rate")
            return True



timeStart = datetime.strptime("2015-11-03",'%Y-%m-%d')
timeEnd = datetime.strptime("2017-05-18",'%Y-%m-%d')
startUnix = time.mktime(timeStart.timetuple())
endUnix = time.mktime(timeEnd.timetuple())
while (startUnix < endUnix) :
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
        print(url)
        
        try:
            html =  parser(url)
        except:
            time.sleep(10)
            print ("connect err")
            continue

        try:   
            if html.getData() == False :
                break
        except:
            print ("error :")
        time.sleep(1)
    
    startUnix += 3600 * 24


# now.strftime('%Y-%m-%d')

# date = "2017-05-17"
# url = 'https://vipc.cn/jczq/singles/'+date+'#start'
# url = 'https://vipc.cn/jczq/single/201705173042'
# html =  parser(url)
# html.getData()
# print("end")





    # for child in tag.descendants :
    #     print(child.find_all('div', class_="team_info"))
        # if child.div['class'] == "team_info" :
        #     print(child.children.span.string)



        # for teamInfo in child.find_all('div', class_="team_info"):
        #     print("start")
        #     print(teamInfo.span.string)
