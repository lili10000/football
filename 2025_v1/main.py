from pyquery import PyQuery as pq
import numpy as np
import requests
import anaylise as an
import time


# with open("test.js", 'r',encoding='utf-8') as f:
#     html_doc = f.read()
#     doc = pq(html_doc)
#     tables = doc('game')
#     print(tables)
    # for table in tables.items():
    #     rows = table('tr')  # 获取当前表格的所有行
    #     for row in rows.items():  # 遍历每一行
    #         cells = row('td')  # 获取当前行的所有单元格
    #         data = [cell.text() for cell in cells.items()]  # 提取单元格文本
    #         rateList.append(data)




def getId(data):
    lines = data.split("\n")
    for line in lines:
        info = 'var game=Array("'
        if info in line:
            info = line[len(info):]
            tmpList = info.split('|')
            id=tmpList[1]
            return id


def getIdBySid(sid):
    url = "https://1x2d.titan007.com/{}.js".format(sid)
    try:
        req = requests.get(url=url)
        return getId(req.text)

    except Exception as e:
        # print("connect err:"+ repr(e))
        return



# print(getIdBySid(2719455)) 

sidList = []
with open("list.txt", 'r',encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        tmp = "var "
        if "var " in line:
            continue
        tmp = ' = "'
        tmpList = line.split(tmp)
        if len(tmpList) < 2:
            continue
        info = tmpList[1]
        tmpList = info.split('^')
        if len(tmpList) < 2:
            continue
        sid = tmpList[0]
        sidList.append(sid)

for sid in sidList:
    id = getIdBySid(sid)
    if id == None:
        continue

    url = "https://1x2.titan007.com/OddsHistory.aspx?id={}&sid={}&cid=281&l=0".format(id,sid)
    try:
        req = requests.get(url=url)
        data = req.text
        an.outInfo(data)
        time.sleep(1)
        continue
    except Exception as e:
        # print("connect err:"+ repr(e))
        continue





