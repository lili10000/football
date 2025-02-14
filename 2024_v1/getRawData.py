# encoding=utf8
import json

import os
import time

# import jpush as jpush
import requests
import http.client


url="https://api.footballant.com/api/v2/league-detail-schedule-news"
querystring = {"lang":"zh-CN","device":"3"}
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "application/json",
    "User-Agent": "PostmanRuntime-ApipostRuntime/1.1.0",
    "Connection": "keep-alive",
    "Content-Type": "application/json"
}





def saveInfo(id, season, rounds, subSclassId=0):
    bodyInfo = {
        "sclassId": id,
        "season": season,
        "subSclassId": subSclassId,
        "rounds":rounds,
        "page":1,
        "pageSize":60,
        "type":0,
        "useCache":True,
    }

    bodyJson = json.dumps(bodyInfo)
    # print(bodyJson)

    try:
        conn = http.client.HTTPSConnection("api.footballant.com")
        conn.request("POST", "/api/v2/league-detail-schedule-news?lang=zh-CN&device=3", bodyJson, headers)
        res = conn.getresponse()
        data = res.read()
        str_data = str(data, encoding='utf-8')

        fileName = "{}-{}-{}".format(id, rounds,subSclassId)
        path = os.path.dirname(__file__)
        file = "{}/resource/{}.json".format(path, fileName)
        with open(file, 'w',encoding='utf-8') as f:
            f.write(str_data)
            print("write ", file, " ok")
    except Exception as e:
        print("connect err:" + repr(e))
        return


def saveGroupInfo(id, season, grouping):
    bodyInfo = {
        "sclassId": id,
        "season": season,
        "grouping": grouping, 
        "grouping2": "",
        "page":1,
        "pageSize":60,
        "type":0,
        "useCache":True,
    }

    bodyJson = json.dumps(bodyInfo)
    # print(bodyJson)

    try:
        conn = http.client.HTTPSConnection("api.footballant.com")
        conn.request("POST", "/api/v2/league-detail-schedule-group-news?type=0&lang=zh-CN&device=3", bodyJson, headers)
        res = conn.getresponse()
        data = res.read()
        str_data = str(data, encoding='utf-8')

        fileName = "{}-{}".format(id, grouping)
        path = os.path.dirname(__file__)
        file = "{}/resource/{}.json".format(path, fileName)
        with open(file, 'w',encoding='utf-8') as f:
            f.write(str_data)
            print("write ", file, " ok")
    except Exception as e:
        print("connect err:" + repr(e))
        return


# 英超
# for i in range(38):
#     saveInfo("36", "2023-2024", i+1)
#     time.sleep(5)

# 阿甲
# for i in range(8):
#     saveInfo("2", "2024", i+1, "2761")
#     time.sleep(5)

# 澳足总
for i in range(1):
    saveGroupInfo("1356", "2023", "外围赛")
    time.sleep(5)