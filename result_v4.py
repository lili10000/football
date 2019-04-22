from db.mysql import sqlMgr


def checkMain():

    sql = sqlMgr('localhost', 'root', '861217', 'football')
    gameCode = sql.queryByTypeAll("k_gamedic")

    outputInfo={}
    tableName = "k_rateDiv"
    sql.cleanAll(tableName)
    size = 0
    rateSum = 0
    
    for code in gameCode:
        id = code[0]
        gameName = code[1]
        data = sql.queryByTypeTime(gameName, 'k_corner')

        
        outputInfo = {}
        rateMax = -1
        result = {}

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

            

            rateWinFlag = 0
            if main_score - client_score + rate> 0:
                rateWinFlag = 1
            elif main_score - client_score + rate < 0:
                rateWinFlag = -1


            BigFlag = 0
            if main_score + client_score - scoreRate > 0:
                BigFlag = 1
            if main_score + client_score - scoreRate < 0:
                BigFlag = -1


            rateDiv = scoreRate - abs(rate)
            if result.__contains__(rateDiv) == False:
                result[rateDiv] = [0, 0, 0]
            tmp = result[rateDiv]
            tmp[0] += rateWinFlag
            tmp[1] += BigFlag
            tmp[2] += 1
            result[rateDiv] = tmp

        bigMax = -1
        info = "让"
        getData = []
        rateDiv = 0
        rateTmp = 0
       
        for key in result:
            tmp = result[key]
            if abs(tmp[0]) > bigMax:
                bigMax = abs(tmp[0])
                getData = tmp
                info = "让"
                rateTmp = round (abs(tmp[0]) / tmp[2], 2)
                rateDiv = key

            # if abs(tmp[1]) > bigMax:
            #     bigMax = abs(tmp[1])
            #     getData = tmp
            #     info = "球"
            #     rateTmp = round (abs(tmp[1]) / tmp[2], 2)
            #     rateDiv = key

        if rateTmp < 0.2:
            continue

        if info == "让" and getData[0] < 0:
            info += "输"
        if info == "让" and getData[0] > 0:
            info += "赢"
        if info == "球" and getData[1] > 0:
            info = "大" + info
        if info == "球" and getData[1] < 0:
            info = "小" + info


        logInfo = "'{}','{}','{}','{}','{}'".format(id, gameName, rateDiv, info, rateTmp)
        # print(logInfo)
        sql.insert(logInfo, tableName)
        size += 1
            # return

    print("size:", size)
    #     if outputInfo[4] < 0.6:
    #         continue
    #     # print(outputInfo)
    #     size += 1
    #     rateSum += outputInfo[4]

    #     info = "'{}','{}','{}','{}','{}','{}'".format(outputInfo[0],outputInfo[1],outputInfo[2],outputInfo[3],outputInfo[4], outputInfo[5])
    #     sql.insert(info, tableName)
    # print("size:", size, " rate:", round(rateSum/size, 2))


# checkMain()
