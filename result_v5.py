from db.mysql import sqlMgr

indexList = [0,0,0,0]
rateList = {}


def checkMain():
    sql = sqlMgr('localhost', 'root', '861217', 'football')
    datas = sql.queryByTypeAll("k_commend")
    total = 0
    size = len(datas)
    winSize = 0

    danWin = 0
    for one in datas:
        id = one[0]
        tmp = id.split('_')
        # gameId = tmp[1]
        gameId = "{}_{}".format(tmp[0],tmp[1])
        result = sql.queryByGameId('k_corner', gameId)
        if len(result) == 0:
            continue

        gameInfo = result[0]

        if len(gameInfo) == 0:
            continue

        mainScore = int(gameInfo[2])
        clientScore = int(gameInfo[3])
        rate = float(gameInfo[4])
        scoreRate = float(gameInfo[11])

        winFlag = 0
        if mainScore - clientScore + rate > 0:
            winFlag = 1
        elif mainScore - clientScore + rate < 0:
            winFlag = -1


        bigFlag = 0
        if mainScore + clientScore - scoreRate > 0:
            bigFlag = 1
        elif mainScore + clientScore - scoreRate < 0:
            bigFlag = -1

        dan = ((mainScore + clientScore) % 2 == 1)
        shuang = ((mainScore + clientScore) % 2 == 0)

        winAdd = 3

        if rate > 0:
            if winFlag == 1 and bigFlag == -1 :
                total += winAdd
                winSize += 1
            elif (winFlag == 1 and bigFlag == 0) or (winFlag == 0 and bigFlag == -1) :
                total += 1
            elif winFlag == -1 or bigFlag == 1 or shuang:
                total += -1

            if shuang:
                danWin += 1
            else:
                danWin -= 1
            
        if rate < 0:
            if winFlag == 1 and bigFlag == 1 :
                total += winAdd 
                winSize += 1
            elif (winFlag == 1 and bigFlag == 0) or (winFlag == 0 and bigFlag == 1):
                total += 1
            elif winFlag == -1 or bigFlag == -1  :
                total += -1

            if dan:
                danWin += 1
            else:
                danWin -= 1

        if rate == 0:
            if winFlag == 1 and bigFlag == 1 :
                total += winAdd 
                winSize += 1
            elif (winFlag == 1 and bigFlag == 0) or (winFlag == 0 and bigFlag == 1) :
                total += 1
            elif winFlag == -1 or bigFlag == -1  :
                total += -1

            if dan:
                danWin += 1
            else:
                danWin -= 1

    print(total, round(total/size, 2), round(winSize/size, 2), round(danWin/size, 2))


            
checkMain()