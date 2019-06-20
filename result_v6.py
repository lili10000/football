# -*- coding: utf-8 -*-
from db.mysql import sqlMgr
import json

indexList = [0,0,0,0]
rateList = {}
def checkMain():

    sql = sqlMgr('localhost', 'root', '861217', 'football')
    gameCode = sql.queryByTypeAll("k_gamedic")

    outputInfo={}
    tableName = "k_rateDiv"
    sql.cleanAll(tableName)
    size = 0
    rateSum = 0

    big_1 = 0
    big_2 = 0
    small_1 = 0
    small_2 = 0

    checkParam = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for code in gameCode:
        id = code[0]
        gameName = code[1]
        data = sql.queryByTypeTime(gameName, 'k_corner')

        
        outputInfo = {}
   
        result = {}

        total = len(data)
        for one in data:
            main = one[0]
            client = one[1]
            main_score = int(one[2])
            client_score = int(one[3])
            rate = one[4]
            gameType = one[5]
            mainCorner = one[6]
            clientCorner = one[7]
            scoreRate = one[11]
            time = one[9]
            if rate == "-" or rate == "-\n" :
                continue
            rate = float(rate)
            if scoreRate == "-" or scoreRate == "-\n" :
                continue
            scoreRate = float(scoreRate)

            

            rateWinFlag = False
            if main_score - client_score + rate> 0:
                rateWinFlag = True
            elif main_score - client_score + rate < 0:
                rateWinFlag = False
            else :
                continue


            BigFlag = False
            if main_score + client_score - scoreRate > 0:
                BigFlag = True
            elif main_score + client_score - scoreRate < 0:
                BigFlag = False
            else :
                continue

            dan = ((main_score + client_score) % 2 == 1)
            shuang = ((main_score + client_score) % 2 == 0)
            dou = (main_score > 0 and client_score > 0)

            checkFlag = BigFlag
            if checkFlag and dan:
                big_1 += 1
            elif checkFlag and shuang:
                big_2 += 1
            elif checkFlag == False and dan:
                small_1 += 1
            elif checkFlag == False and shuang:
                small_2 += 1




            key = ""
            if rate > 0:
                key = "lost"
            elif rate < 0:
                key = "win"
            else:
                key = "ping"

            if result.__contains__(key) == False:
                result[key]={}



            rateDiv = scoreRate - abs(rate)
            if result[key].__contains__(rateDiv) == False:
                result[key][rateDiv] = [0, 0, 0, 0]
            if result[key].__contains__("all") == False:
                result[key]["all"] = [0, 0, 0, 0]

            tmp = result[key][rateDiv]
            alltmp = result[key]["all"]
            
            if rateWinFlag and BigFlag:
                tmp[0] += 1
                alltmp[0] += 1
                indexTmp = 0
                if dan:
                    checkParam[indexTmp][0] += 1
                else:
                    checkParam[indexTmp][1] += 1

                if dou:
                    checkParam[indexTmp][2] += 1
                else:
                    checkParam[indexTmp][3] += 1
            elif rateWinFlag  and BigFlag == False:
                tmp[1] += 1
                alltmp[1] += 1
                indexTmp = 1
                if dan:
                    checkParam[indexTmp][0] += 1
                else:
                    checkParam[indexTmp][1] += 1

                if dou:
                    checkParam[indexTmp][2] += 1
                else:
                    checkParam[indexTmp][3] += 1
            elif rateWinFlag  == False and BigFlag:
                tmp[2] += 1
                alltmp[2] += 1
                indexTmp = 2
                if dan:
                    checkParam[indexTmp][0] += 1
                else:
                    checkParam[indexTmp][1] += 1

                if dou:
                    checkParam[indexTmp][2] += 1
                else:
                    checkParam[indexTmp][3] += 1
            elif rateWinFlag  == False and BigFlag == False:
                tmp[3] += 1
                alltmp[3] += 1
                indexTmp = 3
                if dan:
                    checkParam[indexTmp][0] += 1
                else:
                    checkParam[indexTmp][1] += 1

                if dou:
                    checkParam[indexTmp][2] += 1
                else:
                    checkParam[indexTmp][3] += 1

            result[key][rateDiv] = tmp
            result[key]["all"] = alltmp


        # rawData = json.dumps(result)

        # keys = result.keys()
        params = {}
        for key in result:
            datas = result[key]["all"]
            countSum = sum(datas)
            result[key].pop('all')
            datas = [0,0,0,0]

            maxDiv = 0
            minDiv = 10
            for div in result[key]:
                if sum(result[key][div]) < 0.1*countSum:
                    continue
                datas[0] += result[key][div][0]
                datas[1] += result[key][div][1]
                datas[2] += result[key][div][2]
                datas[3] += result[key][div][3]


                if div > maxDiv:
                    maxDiv = div
                if div < minDiv:
                    minDiv = div

            maxIndex = 0
            maxCount = 0
            for index in range(4):
                if datas[index] > maxCount:
                    maxCount = datas[index]
                    maxIndex = index

            params[key] = {"buy":maxIndex, "maxDiv":maxDiv, "minDiv": minDiv}

            


        params = json.dumps(params)

        info = "'{}','{}','{}'".format(id, gameName, params)
        sql.insert(info, "k_gamedic_v4",id)
    
    # print(checkParam)
# checkMain()