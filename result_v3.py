from db.mysql import sqlMgr


def cal(mainParam, clientParam):
   
    # if mainParam[3] == mainParam[4] and mainParam[5] > 0: # 连续让输，主场让赢
    #     return 1
    # elif clientParam[2] == mainParam[4] and mainParam[5] > 0: # 连续让赢，客场让输
    #     return -1
    # return 0

    if mainParam[3] == mainParam[4]: # 连续让输，主场让赢
        return 1
    elif clientParam[2] == mainParam[4]: # 连续让赢，客场让输
        return -1
    return 0


def checkMain():
# key = 'k_rateBuy'
    sql = sqlMgr('localhost', 'root', '861217', 'football')
    gameCode = sql.queryByTypeAll("k_gamedic")

    outputInfo={}
    tableName = "k_rateBuy_v3"
    sql.cleanAll(tableName)
    for code in gameCode:
        id = code[0]
        gameName = code[1]
        data = sql.queryByTypeTime(gameName, 'k_corner')

        
        outputInfo = {}
        rateMax = -1
        for i in range(1):
            lostCount = i + 2
            info = {}
            winSum = 0
            lostSum = 0
            BigWinSum = 0
            BiglostSum = 0
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
                cornerRate = one[12]
                if rate == "-" or rate == "-\n" :
                    continue
                rate = float(rate)
                if scoreRate == "-" or scoreRate == "-\n" :
                    continue
                # if cornerRate == "-" or cornerRate == "-\n" :
                #     continue
                # cornerRate = float(cornerRate)
                scoreRate =  float(scoreRate)

                if info.__contains__(main) == False:
                    info[main] = []
                if info.__contains__(client) == False:
                    info[client] = []

                rateKey = "rateResult"
                bigKey = "big"
               
                mainInput = {rateKey:0, }
                clientInput = {rateKey:0, bigKey:0}

                checkFlag = False
                if main_score - client_score + rate > 0 and rate > 0:
                    # mainInput[rateKey] = 1
                    # clientInput[rateKey] = -1
                    checkFlag = True
                elif main_score - client_score + rate < 0 and rate < 0:
                    # mainInput[rateKey] = -1
                    # clientInput[rateKey] = 1
                    checkFlag = True

                if checkFlag == False:
                    continue

                # if mainCorner + clientCorner - cornerRate > 0 :
                #     BigWinSum += 1
                # elif mainCorner + clientCorner - cornerRate < 0 :
                #     BiglostSum += 1

                if main_score + client_score - scoreRate > 0 :
                    BigWinSum += 1
                elif main_score + client_score - scoreRate < 0 :
                    BiglostSum += 1

            bigRate = 0
            if BigWinSum+BiglostSum != 0:
                bigRate = round(BigWinSum/ (BigWinSum+BiglostSum),2 )
            

            if bigRate > rateMax:
                rateMax = bigRate
                outputInfo = [id, gameName, "大球", bigRate, 1]


        # if abs(outputInfo[4] - 0.5) < 0.09:
        #     continue
        print(outputInfo)
        # info = "'{}','{}','{}','{}','{}','{}'".format(outputInfo[0],outputInfo[1],outputInfo[2],outputInfo[3],outputInfo[4], outputInfo[5])
        # sql.insert(info, tableName)
 


checkMain()
# checkMain('k_rateBuy')
# checkBig('k_scoreBuy')
# checkCorner('k_cornerBuy')