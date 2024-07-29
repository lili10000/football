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

    check_1 = 0
    check_2 = 0
    check_3 = 0
    checkSum = 0

    checkParam = [0,0,0,0]
    # checkParam = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for code in gameCode:
        id = code[0]

        info = sql.queryByGameId('k_gamedic_v4',id)
        if len(info) == 0:
            continue
        param = info[0][2]
        param = json.loads(param)


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
            dou = (main_score * client_score != 0)

            # checkFlag = BigFlag
            # if checkFlag and dan:
            #     big_1 += 1
            # elif checkFlag and shuang:
            #     big_2 += 1
            # elif checkFlag == False and dan:
            #     small_1 += 1
            # elif checkFlag == False and shuang:
            #     small_2 += 1


            key = ""
            if rate > 0:
                key = "lost"
            elif rate < 0:
                key = "win"
            else:
                key = "ping"

            if result.__contains__(key) == False:
                result[key]={}

            tmpParam = param[key]
            maxDiv = tmpParam["maxDiv"]
            minDiv = tmpParam["minDiv"]

            rateDiv = scoreRate - abs(rate)

            if (rateDiv > maxDiv or rateDiv < minDiv):
                continue

            checkSum += 1
            if rateWinFlag:
                check_1 += 1
            else:
                check_1 -= 1

            if BigFlag:
                check_2 += 1
            else:
                check_2 -= 1


            # condi_1 = False
            # condi_2 = False

            # if (tmpParam["buy"] == 1) or (tmpParam["buy"] == 3):
            #     continue
            # if not BigFlag :
            #     continue

            # if tmpParam["buy"] == 0:
            #     condi_1 = (rateWinFlag and BigFlag)
            # elif tmpParam["buy"] == 1:
            #     condi_1 = (rateWinFlag and BigFlag == False)
            # elif tmpParam["buy"] == 2:
            #     condi_1 = (rateWinFlag == False and BigFlag)
            # elif tmpParam["buy"] == 3:
            #     condi_1 = (rateWinFlag == False and BigFlag == False)

            # if condi_1:
            #     check_1 += 3
            #     check_2 += 1 
            # else:
            #     check_1 -= 1
            #     check_3 += 1 


            # if rateWinFlag and BigFlag:
            #     checkParam[0] += 1
            # elif rateWinFlag  and BigFlag == False:
            #     checkParam[1] += 1
            # elif rateWinFlag  == False and BigFlag:
            #     checkParam[2] += 1
            # elif rateWinFlag  == False and BigFlag == False:
            #     checkParam[3] += 1


            if rateWinFlag:
                checkParam[0] += 1
            else:
                checkParam[1] += 1

            if BigFlag:
                checkParam[2] += 1
            else:
                checkParam[3] += 1

           

            # checkSum += 1
            # if dou:
            #     check_1 += 1
            # else:
            #     check_1 -= 1 
            
            # if dan:
            #     check_2 -= 1
            # else:
            #     check_2 += 1 


            # if result[key].__contains__(rateDiv) == False:
            #     result[key][rateDiv] = [0, 0, 0, 0]
            # if result[key].__contains__("all") == False:
            #     result[key]["all"] = [0, 0, 0, 0]

            # tmp = result[key][rateDiv]
            # alltmp = result[key]["all"]
            
            # if rateWinFlag and BigFlag:
            #     tmp[0] += 1
            #     alltmp[0] += 1
            #     indexTmp = 0
            #     if dan:
            #         checkParam[indexTmp][0] += 1
            #     else:
            #         checkParam[indexTmp][1] += 1

            #     if dou:
            #         checkParam[indexTmp][2] += 1
            #     else:
            #         checkParam[indexTmp][3] += 1
            # elif rateWinFlag  and BigFlag == False:
            #     tmp[1] += 1
            #     alltmp[1] += 1
            #     indexTmp = 1
            #     if dan:
            #         checkParam[indexTmp][0] += 1
            #     else:
            #         checkParam[indexTmp][1] += 1

            #     if dou:
            #         checkParam[indexTmp][2] += 1
            #     else:
            #         checkParam[indexTmp][3] += 1
            # elif rateWinFlag  == False and BigFlag:
            #     tmp[2] += 1
            #     alltmp[2] += 1
            #     indexTmp = 2
            #     if dan:
            #         checkParam[indexTmp][0] += 1
            #     else:
            #         checkParam[indexTmp][1] += 1

            #     if dou:
            #         checkParam[indexTmp][2] += 1
            #     else:
            #         checkParam[indexTmp][3] += 1
            # elif rateWinFlag  == False and BigFlag == False:
            #     tmp[3] += 1
            #     alltmp[3] += 1
            #     indexTmp = 3
            #     if dan:
            #         checkParam[indexTmp][0] += 1
            #     else:
            #         checkParam[indexTmp][1] += 1

            #     if dou:
            #         checkParam[indexTmp][2] += 1
            #     else:
            #         checkParam[indexTmp][3] += 1

            # result[key][rateDiv] = tmp
            # result[key]["all"] = alltmp


    print(checkParam)
    print(checkSum, check_1, check_2, check_3)
checkMain()