# encoding=utf8
import json
from sklearn.linear_model import Ridge
import http.client
import numpy as np
import os
import fileUtil

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

    inputList = []
    outputList = []
    info = []

    try:
        conn = http.client.HTTPSConnection("api.footballant.com")
        conn.request("POST", "/api/v2/league-detail-schedule-news?lang=zh-CN&device=3", bodyJson, headers)
        res = conn.getresponse()
        data = res.read()
        str_data = str(data, encoding='utf-8')
        result=json.loads(str_data)
        dataList = result["data"]["list"]

        for data in dataList:
            inputList.append([float(data["o_odds"]['o_home']), float(data["o_odds"]['o_stand']), float(data["o_odds"]['o_guest'])])  
            outputList.append(float(data["total_score_odds"]['total_score_goal_r']))

            info.append(data["home"])
           
        
    except Exception as e:
        print("connect err:" + repr(e))
    
    finally:
        return inputList,outputList,info

# 英超
# for i in range(38):
#     saveInfo("36", "2023-2024", i+1)
#     time.sleep(5)

# 阿甲

def check(id, season, rounds, subSclassId=0):

    inputList,outputList,info = saveInfo(id, season, rounds, subSclassId)

    a = []
    b = []
    path = os.path.dirname(__file__)
    file = "{}\\data\\{}.json".format(path, id)
    with open(file, 'r',encoding='utf-8') as f:
        data = f.read()
        tmpList = json.loads(data)
        for result in tmpList:
            input = [float(result["o_home"]), float(result["o_stand"]), float(result["o_guest"])]
            # output = [float(result["y_goal"])]
            output = [float(result["score_goal"])]
            a.append(input)
            b.append(output)
    a=np.array(a)
    b=np.array(b)



    clf = Ridge() # good
    rf = clf.fit (a, b.ravel())

    inputList=np.array(inputList)
    outputList = np.array(outputList)
    y_pred = rf.predict(inputList)
    result = y_pred - outputList

    fileUtil.writeResult("start id:{}\n".format(id))
    for i in range(len(info)):
        addInfo = ""
        if (abs(result[i]) > 0.2):
            addInfo = "-->"

        wInfo = "{} {} {} \n".format(addInfo, round(result[i],2), info[i])
        fileUtil.writeResult(wInfo)
    fileUtil.writeResult("end id:{}\n".format(id))

check("2", "2024", 8, "2761")
# check("36", "2023-2024", 1)