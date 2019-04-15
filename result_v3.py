from db.mysql import sqlMgr


def cal(mainParam, clientParam):
   
    # if mainParam[3] == mainParam[4] and mainParam[5] > 0: # 连续让输，主场让赢
    #     return 1
    # elif clientParam[2] == mainParam[4] and mainParam[5] > 0: # 连续让赢，客场让输
    #     return -1
    # return 0

# [round(scoreSum / lostCount, 2), round(lostScoreSum / lostCount, 2), GoodSum, badSum, lostCount, rate]

    # if mainParam[2] == mainParam[4]: # 主连续大球，主场让输
    #     return -1
    # if clientParam[3] == clientParam[4]: # 客连续小球，主场让输
    #     return -1
    # if clientParam[2] == clientParam[4]: # 客连续大球，主场让赢
    #     return 1


    # if clientParam[3] == clientParam[4]: # 主连续大球，小球
    #     return -1
    if clientParam[2] == clientParam[4]: # 客连续大球，小球
        return -1




    # if clientParam[3] == clientParam[4]: # 客连续小球，主场让输
    #     return -1

    return 0


def checkMain():
# key = 'k_rateBuy'
    sql = sqlMgr('localhost', 'root', '861217', 'football')
    gameCode = sql.queryByTypeAll("k_gamedic")

    outputInfo={}
    tableName = "k_rateBuy_v4"
    sql.cleanAll(tableName)
    size = 0
    rateSum = 0
    for code in gameCode:
        id = code[0]
        gameName = code[1]
        data = sql.queryByTypeTime(gameName, 'k_corner')

        
        outputInfo = {}
        rateMax = -1
        for i in range(2):
            # rateMax = -1
            lostCount = i + 2
            # lostCount = 3
            # gameName = "英超"
            # index = lostCount

            info = {}
            winSum = 0
            lostSum = 0
            clientWinSum = 0
            clientlostSum = 0
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
                if info.__contains__(main) == False:
                    info[main] = []
                if info.__contains__(client) == False:
                    info[client] = []

                rateKey = "rateResult"
                normalKey = "normal"
                scoreKey = "score"
                lostKey = "lost"
                timeKey = "time"
                goodKey = "rate"
                scoreResult = "scoreResult"
                mainInput = {rateKey:0, normalKey:0, scoreKey:0, lostKey:0, timeKey:0, goodKey:0, scoreResult:0}
                clientInput = {rateKey:0, normalKey:0, scoreKey:0, lostKey:0, timeKey:0, goodKey:0, scoreResult:0}
                if main_score - client_score + rate> 0:
                    mainInput[rateKey] = 1
                    clientInput[rateKey] = -1
                elif main_score - client_score + rate < 0:
                    mainInput[rateKey] = -1
                    clientInput[rateKey] = 1


                if main_score - client_score> 0:
                    mainInput[normalKey] = 1
                    clientInput[normalKey] = -1
                elif main_score - client_score < 0:
                    mainInput[normalKey] = -1
                    clientInput[normalKey] = 1

                if main_score + client_score - scoreRate> 0:
                    mainInput[scoreResult] = 1
                    clientInput[scoreResult] = 1
                elif main_score + client_score - scoreRate < 0:
                    mainInput[scoreResult] = -1
                    clientInput[scoreResult] = -1

                mainInput[scoreKey] = main_score
                mainInput[lostKey] = client_score
                mainInput[goodKey] = rate

                clientInput[scoreKey] = client_score
                clientInput[lostKey] = main_score
                clientInput[goodKey] = rate * -1

                info[main].append(mainInput)
                info[client].append(clientInput)

                        
                mainSize = len(info[main])
                clientSize = len(info[client])

                # lostCount = 5
                if mainSize < lostCount + 1:
                    continue
                if clientSize < lostCount + 1:
                    continue


                tmpName = main
                tmpSize = mainSize
                checkFlag = False

                scoreSum = 0
                lostScoreSum = 0
                GoodSum = 0
                badSum = 0
                for i in range(lostCount):
                    if info[tmpName][tmpSize-i-2].__contains__(scoreResult) == False:
                        print(info[tmpName][tmpSize-i-2])
                        continue
                    if info[tmpName][tmpSize-i-2][scoreResult] == 1:
                        GoodSum += 1
                    if info[tmpName][tmpSize-i-2][scoreResult] == -1:
                        badSum += 1
                    scoreSum += info[tmpName][tmpSize-i-2][scoreKey]
                    lostScoreSum += info[tmpName][tmpSize-i-2][lostKey]
                mainParam =  [round(scoreSum / lostCount, 2), round(lostScoreSum / lostCount, 2), GoodSum, badSum, lostCount, rate]
            

                tmpName = client
                tmpSize = clientSize
                scoreSum = 0
                lostScoreSum = 0
                GoodSum = 0
                badSum = 0
                for i in range(lostCount):
                    if info[tmpName][tmpSize-i-2][normalKey] == 1:
                        GoodSum += 1
                    if info[tmpName][tmpSize-i-2][normalKey] == -1:
                        badSum += 1
                    scoreSum += info[tmpName][tmpSize-i-2][scoreKey]
                    lostScoreSum += info[tmpName][tmpSize-i-2][lostKey]
                clientParam = [round(scoreSum / lostCount, 2), round(lostScoreSum / lostCount, 2), GoodSum, badSum, lostCount]

                calRate = cal(mainParam, clientParam)
                if calRate == 0:
                    continue


                if calRate == 1 and main_score + client_score - scoreRate> 0:
                    winSum += 1
                    # clientWinSum += 1

                elif calRate == 1 and main_score + client_score - scoreRate < 0:
                    lostSum += 1
                    # clientlostSum += 1
                
                if calRate == -1 and main_score + client_score - scoreRate > 0:
                    clientlostSum += 1
                    # lostSum += 1

                elif calRate == -1 and main_score + client_score - scoreRate < 0:
                    # winSum += 1
                    clientWinSum += 1


            mainRate = 0
            if winSum+lostSum != 0:
                mainRate = round(winSum/ (winSum+lostSum),2 )
            

            clientRate = 0
            if clientWinSum+clientlostSum != 0:
                clientRate =  round(clientWinSum/ (clientWinSum+clientlostSum),2 )

            if mainRate > rateMax:
                rateMax = mainRate
                outputInfo = [id, lostCount, gameName, "大球", mainRate, 1]
            if clientRate > rateMax:
                rateMax = clientRate
                outputInfo = [id, lostCount, gameName, "小球", clientRate, -1]


        if outputInfo[4] < 0.6:
            continue
        # print(outputInfo)
        size += 1
        rateSum += outputInfo[4]
        info = "'{}','{}','{}','{}','{}','{}'".format(outputInfo[0],outputInfo[1],outputInfo[2],outputInfo[3],outputInfo[4], outputInfo[5])
        sql.insert(info, tableName)

    print("size:", size, " rate:", round(rateSum/size, 2))


# checkMain()
# checkMain('k_rateBuy')
# checkBig('k_scoreBuy')
# checkCorner('k_cornerBuy')