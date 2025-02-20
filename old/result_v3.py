from db.mysql import sqlMgr


def cal(mainParam, clientParam):
   
    # if mainParam[3] == mainParam[4] and mainParam[5] > 0: # 连续让输，主场让赢
    #     return 1
    # elif clientParam[2] == mainParam[4] and mainParam[5] > 0: # 连续让赢，客场让输
    #     return -1
    # return 0

    # if (mainParam[2] == mainParam[4]) and (clientParam[3] == clientParam[4]):
    #     return 0

    # if mainParam[3] == mainParam[4]: # 连续大，买大
    #     return -1

    if clientParam[3] == clientParam[4]: # 连续大，买大
        return -1

    # if clientParam[3] == mainParam[4]: # 连续大，买大
    #     return -1

    # if clientParam[3] == clientParam[4] : #连续小，买小
    #     return -1


    # if clientParam[3] == clientParam[4]: # 连续让输，买让输
    #     return -1


    # if mainParam[2] == mainParam[4]: # 连续让赢，买让输
    #     return -1
    # if clientParam[2] == clientParam[4]: # 连续让赢，买让输
    #     return 1
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
        
        for i in range(3):
            # rateMax = -1
            # lostCount = i + 2
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
                time = one[9]
                scoreRate = one[11]

                if rate == "-" or rate == "-\n" :
                    continue
                if scoreRate == "-" or scoreRate == "-\n" :
                    continue

                rate = float(rate)        
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
                mainInput = {rateKey:0, normalKey:0, scoreKey:0, lostKey:0, timeKey:0, goodKey:0}
                clientInput = {rateKey:0, normalKey:0}
                if main_score + client_score - scoreRate > 0:
                    mainInput[rateKey] = 1
                    clientInput[rateKey] = 1
                elif main_score + client_score - scoreRate < 0:
                    mainInput[rateKey] = -1
                    clientInput[rateKey] = -1


                if main_score - client_score> 0:
                    mainInput[normalKey] = 1
                    clientInput[normalKey] = -1
                elif main_score - client_score < 0:
                    mainInput[normalKey] = -1
                    clientInput[normalKey] = 1

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
                    if info[tmpName][tmpSize-i-2][rateKey] == 1:
                        GoodSum += 1
                    if info[tmpName][tmpSize-i-2][rateKey] == -1:
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
                buyBig = False
                if calRate > 0 :
                    buyBig = True
                elif calRate == 0:
                    continue


                if buyBig and main_score + client_score - scoreRate > 0:
                    winSum += 1
                elif buyBig and main_score + client_score - scoreRate  < 0:
                    lostSum += 1
                elif buyBig == False and main_score + client_score - scoreRate  > 0:
                    lostSum += 1
                elif buyBig == False and main_score + client_score - scoreRate  < 0:
                    winSum += 1
            
                

            mainRate = 0
            if winSum+lostSum != 0:
                mainRate = round(winSum/ (winSum+lostSum),2 )
            

            if mainRate > rateMax:
                rateMax = mainRate
                outputInfo = [id, lostCount, gameName, "小球", mainRate, -1, winSum+lostSum]


        if outputInfo[4] < 0.6:
            continue
        # print(outputInfo)
        size += 1
        rateSum += outputInfo[4]

        info = "'{}','{}','{}','{}','{}','{}'".format(outputInfo[0],outputInfo[1],outputInfo[2],outputInfo[3],outputInfo[4], outputInfo[5])
        sql.insert(info, tableName)
        # print(outputInfo[6], info)
    print("size:", size, " rate:", round(rateSum/size, 2))


# checkMain()
# checkMain('k_rateBuy')
# checkBig('k_scoreBuy')
# checkCorner('k_cornerBuy')