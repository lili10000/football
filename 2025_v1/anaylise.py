# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import numpy as np
from datetime import datetime
import requests



def checkRate(rateTmp):
    rateTmp2 = []
    for i in range(len(rateTmp)-2):
        rate = rateTmp[i+2] - 2*rateTmp[i+1] + rateTmp[i]
        rateTmp2.append(float(rate))


    if len(rateTmp2) < 2:
        return 0

    try :
        data = np.array(rateTmp2)
        dataAbs = np.abs(data)

        # print(rateTmp2)
        # 计算期望（均值）
        mean = np.mean(dataAbs)
        # print("期望（均值）:", mean)
        if mean == 0:
            return 0

        max = 0
        get = 0
        for item in data:
            tmp = abs(item) - abs(mean)
            if tmp > abs(max):
                max = tmp
                get = item

        # print(max)

        num = 3
        if(abs(get) / abs(mean)) > num and abs(get) > 0.1:
            return round(get, 2) 
        else:
            return 0
    except Exception as e:
        return 0

def writeFile(info):
    with open(r"result_v1.txt", 'a', encoding="utf-8") as f:
        f.write(info + "\n")
        print(info)
    return 

def outInfo(data):
    doc = pq(data)
    tables = doc('table')
    rateList = []
    for table in tables.items():
        rows = table('tr')  # 获取当前表格的所有行
        for row in rows.items():  # 遍历每一行
            cells = row('td')  # 获取当前行的所有单元格
            data = [cell.text() for cell in cells.items()]  # 提取单元格文本
            rateList.append(data)

    rateTmp = []
    rateTmp1 = []
    rateTmp2 = []

    info= "{} vs {} ".format(rateList[0][0], rateList[0][2]) 

    for i in range(len(rateList)-1):
        rate = rateList[i+1][-4]
        rateTmp.append(float(rate))

        rate = rateList[i+1][-3]
        rateTmp1.append(float(rate))

        rate = rateList[i+1][-2]
        rateTmp2.append(float(rate))

    main = checkRate(rateTmp)
    ping = checkRate(rateTmp1)
    client = checkRate(rateTmp2)


    if main == 0 and ping == 0 and client == 0:
        return
    max = 0
    if abs(main) > abs(ping) and abs(main) > abs(client):
        info += "主"
        max = main
    if abs(ping) > abs(main) and abs(ping) > abs(client):
        info += "平"
        max = ping
    if abs(client) > abs(ping) and abs(client) > abs(main):
        info += "客"
        max = client

    if max > 0:
        info += "赢"
    else:
        info += "输"
    info = "{} [{},{},{}]".format(info, main, ping, client)
    writeFile(info)

# outInfo(rateList)

# now = datetime.now()
# url = "https://livestatic.titan007.com/vbsxml/detail_ut.js?r=007{}".format(int(now.timestamp()) * 1000) 
# print("https://livestatic.titan007.com/vbsxml/detail_ut.js?r=0071739416701000")
# print(url)
# try:
#     req = requests.get(url=url)
#     print(req.text)

# except Exception as e:
#     print("connect err:"+ repr(e))

       