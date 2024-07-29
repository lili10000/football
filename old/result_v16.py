from db.mysql import sqlMgr

def checkMain(key):
# key = 'k_rateBuy'
    sql = sqlMgr('localhost', 'root', '861217', 'football')
    gameCode = sql.queryByTypeAll(key)
    for code in gameCode:
        id = code[0]
        lostCount = code[1]
        gameName = code[2]
        param = code[4]

        data = sql.queryByTypeTime(gameName, 'k_corner')
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
            if rate == "-" or rate == "-\n" :
                continue
            rate = float(rate)

            if info.__contains__(main) == False:
                info[main] = []
            if info.__contains__(client) == False:
                info[client] = []

            rateKey = "rate"
            normalKey = "normal"
            timeKey = "time"
            mainInput = {rateKey:0, normalKey:0, timeKey:0}
            clientInput = {rateKey:0, normalKey:0}
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

            
            info[main].append(mainInput)
            info[client].append(clientInput)

                    
            mainSize = len(info[main])
            clientSize = len(info[client])

            if mainSize < lostCount + 1:
                continue
            if clientSize < lostCount + 1:
                continue


            tmpName = main
            tmpSize = mainSize
            checkFlag = False
            for i in range(lostCount):
                if info[tmpName][tmpSize-i-2][normalKey] != -1:
                    checkFlag = True

            if checkFlag == False and info[tmpName][tmpSize-1][rateKey] == 1:
                winSum += 1
            elif checkFlag == False and info[tmpName][tmpSize-1][rateKey] != 1:
                lostSum += 1
            

            tmpName = client
            tmpSize = clientSize
            checkFlag = False
            for i in range(lostCount):
                if info[tmpName][tmpSize-i-2][normalKey] != -1:
                    checkFlag = True

            if checkFlag == False and info[tmpName][tmpSize-1][rateKey] == 1:
                clientWinSum += 1
            elif checkFlag == False and info[tmpName][tmpSize-1][rateKey] != 1:
                clientlostSum += 1

        mainRate = round(winSum/ (winSum+lostSum),2 )
        clientRate =  round(clientWinSum/ (clientWinSum+clientlostSum),2 )
        info =""
        value = 0
        choiceRate = 0

        # if "意甲" in gameName:
        #     print(gameName)

        if abs(mainRate - 0.5) > abs(clientRate - 0.5):
            # info="主"
            value = 1
            choiceRate = mainRate
            if mainRate > 0.5:
                info = "让胜"
            else:
                info = "让输"
        else:
            # info="客"
            value = -1
            choiceRate = clientRate
            if clientRate > 0.5:
                info = "让胜"
            else:
                info = "让输"
        
    
        sql.cleanById(key, id)
        if abs(choiceRate - 0.5) < 0.06:
            continue 
        info = "'{}','{}','{}','{}','{}','{}'".format(code[0],code[1],code[2],info, round(choiceRate*100,1), value)
        sql.insert(info, key)


def checkBig(key):
    sql = sqlMgr('localhost', 'root', '861217', 'football')
    gameCode = sql.queryByTypeAll(key)
    for code in gameCode:
        id = code[0]
        lostCount = code[1]
        gameName = code[2]
        param = code[4]

        data = sql.queryByTypeTime(gameName, 'k_corner')
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

            rateKey = "rate"
            normalKey = "normal"
            timeKey = "time"
            mainInput = {rateKey:0, normalKey:0, timeKey:0}
            clientInput = {rateKey:0, normalKey:0}
            if main_score + client_score > scoreRate:
                mainInput[rateKey] = 1
                clientInput[rateKey] = -1
            elif main_score + client_score  < scoreRate:
                mainInput[rateKey] = -1
                clientInput[rateKey] = 1


            if main_score - client_score> 0:
                mainInput[normalKey] = 1
                clientInput[normalKey] = -1
            elif main_score - client_score < 0:
                mainInput[normalKey] = -1
                clientInput[normalKey] = 1

            
            info[main].append(mainInput)
            info[client].append(clientInput)

                    
            mainSize = len(info[main])
            clientSize = len(info[client])

            if mainSize < lostCount + 1:
                continue
            if clientSize < lostCount + 1:
                continue


            tmpName = main
            tmpSize = mainSize
            checkFlag = False
            for i in range(lostCount):
                if info[tmpName][tmpSize-i-2][normalKey] != -1:
                    checkFlag = True

            if checkFlag == False and info[tmpName][tmpSize-1][rateKey] == 1:
                winSum += 1
            elif checkFlag == False and info[tmpName][tmpSize-1][rateKey] != 1:
                lostSum += 1
            

            tmpName = client
            tmpSize = clientSize
            checkFlag = False
            for i in range(lostCount):
                if info[tmpName][tmpSize-i-2][normalKey] != -1:
                    checkFlag = True

            if checkFlag == False and info[tmpName][tmpSize-1][rateKey] == 1:
                clientWinSum += 1
            elif checkFlag == False and info[tmpName][tmpSize-1][rateKey] != 1:
                clientlostSum += 1

        mainRate = round(winSum/ (winSum+lostSum),2 )
        clientRate =  round(clientWinSum/ (clientWinSum+clientlostSum),2 )
        info =""
        value = 0
        choiceRate = 0

        # if "意甲" in gameName:
        #     print(gameName)

        if abs(mainRate - 0.5) > abs(clientRate - 0.5):
            # info="主"
            value = 1
            choiceRate = mainRate
            if mainRate > 0.5:
                info = "大球"
            else:
                info = "小球"
        else:
            # info="客"
            value = -1
            choiceRate = clientRate
            if clientRate > 0.5:
                info = "大球"
            else:
                info = "小球"
        
    
        sql.cleanById(key, id)
        if abs(choiceRate - 0.5) < 0.06:
            continue 
        info = "'{}','{}','{}','{}','{}','{}'".format(code[0],code[1],code[2],info, round(choiceRate*100,1), value)
        sql.insert(info, key)

def checkCorner(key):
    sql = sqlMgr('localhost', 'root', '861217', 'football')
    gameCode = sql.queryByTypeAll(key)
    for code in gameCode:
        id = code[0]
        lostCount = code[1]
        gameName = code[2]
        param = code[4]

        data = sql.queryByTypeTime(gameName, 'k_corner')
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
            cornerRate = one[12]
            if rate == "-" or rate == "-\n" :
                continue
            if cornerRate == "-" or cornerRate == "-\n" :
                continue
            rate = float(rate)
            cornerRate = float(cornerRate)

            if info.__contains__(main) == False:
                info[main] = []
            if info.__contains__(client) == False:
                info[client] = []

            rateKey = "rate"
            normalKey = "normal"
            timeKey = "time"
            mainInput = {rateKey:0, normalKey:0, timeKey:0}
            clientInput = {rateKey:0, normalKey:0}
            if mainCorner + clientCorner > cornerRate:
                mainInput[rateKey] = 1
                clientInput[rateKey] = -1
            elif mainCorner + clientCorner  < cornerRate:
                mainInput[rateKey] = -1
                clientInput[rateKey] = 1


            if main_score - client_score> 0:
                mainInput[normalKey] = 1
                clientInput[normalKey] = -1
            elif main_score - client_score < 0:
                mainInput[normalKey] = -1
                clientInput[normalKey] = 1

            
            info[main].append(mainInput)
            info[client].append(clientInput)

                    
            mainSize = len(info[main])
            clientSize = len(info[client])

            if mainSize < lostCount + 1:
                continue
            if clientSize < lostCount + 1:
                continue


            tmpName = main
            tmpSize = mainSize
            checkFlag = False
            for i in range(lostCount):
                if info[tmpName][tmpSize-i-2][normalKey] != -1:
                    checkFlag = True

            if checkFlag == False and info[tmpName][tmpSize-1][rateKey] == 1:
                winSum += 1
            elif checkFlag == False and info[tmpName][tmpSize-1][rateKey] != 1:
                lostSum += 1
            

            tmpName = client
            tmpSize = clientSize
            checkFlag = False
            for i in range(lostCount):
                if info[tmpName][tmpSize-i-2][normalKey] != -1:
                    checkFlag = True

            if checkFlag == False and info[tmpName][tmpSize-1][rateKey] == 1:
                clientWinSum += 1
            elif checkFlag == False and info[tmpName][tmpSize-1][rateKey] != 1:
                clientlostSum += 1

        mainRate = round(winSum/ (winSum+lostSum),2 )
        clientRate =  round(clientWinSum/ (clientWinSum+clientlostSum),2 )
        info =""
        value = 0
        choiceRate = 0

        # if "意甲" in gameName:
        #     print(gameName)

        if abs(mainRate - 0.5) > abs(clientRate - 0.5):
            # info="主"
            value = 1
            choiceRate = mainRate
            if mainRate > 0.5:
                info = "大角"
            else:
                info = "小角"
        else:
            # info="客"
            value = -1
            choiceRate = clientRate
            if clientRate > 0.5:
                info = "大角"
            else:
                info = "小角"
        
    
        sql.cleanById(key, id)
        if abs(choiceRate - 0.5) < 0.06:
            continue 
        info = "'{}','{}','{}','{}','{}','{}'".format(code[0],code[1],code[2],info, round(choiceRate*100,1), value)
        sql.insert(info, key)

        
# checkMain('k_rateBuy')
# checkBig('k_scoreBuy')
# checkCorner('k_cornerBuy')