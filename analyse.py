# coding:utf-8  
import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser


# url = 'https://www.dszuqiu.com/diary/last'
# req = requests.get(url) 
# s = req.text
# with open("tmp.txt", 'w',encoding='utf-8') as f:
#     f.write(req.text)

def clearStr(str):
    str = str.replace(" ", "")
    str = str.replace("\n", "")
    return str

sum = 0
lastSocreSum = 0
lastSocreSum_2 = 0
scoreDic = {}
scoreDistrub = {}
noLastScoreDistrb = {}

check = {}

recordFile = {}
recordName = "dataRecord.txt"

# for index in range(5):
#     data = ""
#     day = ""
#     index += 7
#     if index < 10:
#         day = "0" + str(index)
#     else:
#         day = str(index)
#     # url = 'https://www.dszuqiu.com/diary/201807'+ day
#     # print(url)
#     # req = requests.get(url)
#     # data = req.text
#     # with open(day + ".txt", 'w',encoding='utf-8') as f:
#     #     f.write(req.text)
#     with open(day + ".txt", 'r',encoding='utf-8') as f:
#         data = f.read()
#     # continue
#     print("do ", day)

#     soup = BeautifulSoup(data)
#     table = soup.find('table', class_="live-list-table diary-table")
#     if table == None:
#         continue
#     tbody = table.find('tbody')

#     for tr in tbody.find_all('tr') :
#         td = tr.find('td', class_="text-right BR0")
#         a = td.find('a')
#         host = a.text
#         host = clearStr(host)

#         td = tr.find('td', class_="text-left")
#         a = td.find('a')
#         guest = a.text
#         guest = clearStr(guest)
#         key = host + " vs " + guest

#         score = []

#         for span in tr.find_all('span', class_="timeLineGoal"):
#             attrs = span.attrs
#             score_str = attrs['title']
#             scoreArray = score_str.split("'")
#             strTmp = scoreArray[0]
#             if "+" in strTmp:
#                 tmpArray = strTmp.split("+")
#                 strTmp = tmpArray[0]
#             score_time = int(strTmp)
#             score.append(score_time)

#         recordFile[key] = score

# with open(recordName, 'w',encoding='utf-8') as f:
#     f.write(str(recordFile))

with open(recordName, 'r',encoding='utf-8') as f:
    data = f.read()
    recordFile = eval(data)

for key in recordFile:
    score = recordFile[key]
    size = len(score)
    last_score = 0
    last_score_2 = 0
    if size > 0:
        last_score = int(score[size - 1])
    if size > 1:
        last_score_2 = int(score[size - 2])

    if scoreDic.__contains__(size) == False:
        scoreDic[size] = 0
    scoreDic[size] += 1

    # if last_score >= 85 and last_score_2 < 70:
    lastTime = 85
    checkStart = 80

    if last_score >= lastTime:
        lastSocreSum += 1
        if scoreDistrub.__contains__(size) == False:
            scoreDistrub[size] = 0
        scoreDistrub[size] += 1

    if last_score < lastTime and last_score >= checkStart:
        if check.__contains__(size) == False:
            check[size] = 0
        check[size] += 1

    if last_score > lastTime:
        lastSocreSum_2 +=1
    else:
        if noLastScoreDistrb.__contains__(size) == False:
            noLastScoreDistrb[size] = 0
        noLastScoreDistrb[size] += 1
    sum += 1




print("sum:", sum, "    lastSocreSum:",lastSocreSum, "  lastSocreSum_2:",lastSocreSum_2)

for key in range(10):
    score1 = 0
    score2 = 0
    score3 = 0
    score4 = 0
    if scoreDistrub.__contains__(key):
        score1 = scoreDistrub[key]
    if noLastScoreDistrb.__contains__(key):
        score2 = noLastScoreDistrb[key]
    if scoreDic.__contains__(key):
        score3 = scoreDic[key]
    if check.__contains__(key):
        score4 = check[key]
    print(" key = ",key ,"  高赔绝杀 = ",score1," 非绝杀 = ",score2,"   进球分布 = ",score3,"   check = ",score4)

