from db.mysql import sqlMgr

def docal():
    sql = sqlMgr('localhost', 'root', '861217', 'football')

    name = None

    loopSize = 2
    params = sql.queryByTypeAll("k_gameDic")
    infoList = {}

    ngeFlag =True
    ngeFlag =False

    class getMinValue:
        def __init__(self):
            self.data = {}
            self.sum = 0

        def add(self, value):
            if self.data.__contains__(value) == False:
                self.data[value] = 0
            self.data[value] += 1
            self.sum += 1

        def getResult(self):
            sumTmp = 0
            for key in self.data:
                sumTmp += self.data[key]
                if sumTmp > (self.sum /2):
                    return key - 0.5


    def getResult(param, rateParam, checkType):
        data = []
        name = param[1]
        # gameParam = param[1]

        if name == None:
            data = sql.queryByTypeAll("k_corner")
        else:
            data = sql.queryByType(name, "k_corner")

        if len(data) == 0 :
            return
        # print("sum = ", len(data))
        win_size = 0
        lost_size = 0
        scoreMin = getMinValue()
        gameSum = 0

        cornerMin = getMinValue()

        class DataSize:
            def __init__(self):  
                self.main_win_size = 0     
                self.main_lost_size = 0    
                self.client_win_size = 0     
                self.client_lost_size = 0        


        result_slice = {}
        result_slice_v2 = {}
        for one in data :
            main = one[0]
            client = one[1]
            main_score = one[2]
            client_score = one[3]
            rate = one[4]
            gameType = one[5]

            mainCorner = one[6]
            clientCorner = one[7]
            cornerSum = int(mainCorner) + int(clientCorner)

            gameTime = one[9]

            

            if rate == "-" or rate == "-\n" :
                continue

            
            # scoreSum += main_score + client_score
            scoreMin.add(main_score + client_score)
            # cornerTotal += cornerSum
            cornerMin.add(cornerSum)
            gameSum += 1

            rate = float(rate)
            def addData(result_slice, key, gameTime, value, mainFlag=False, rate=0, score=0, corner=0):
                if result_slice.__contains__(key) == False:
                    result_slice[key] = {}
                result_slice[key][gameTime] = [value, mainFlag, rate, score, corner]
                return result_slice

            if main_score - client_score + rate> 0:
                key = main
                result_slice = addData(result_slice, key, gameTime, 1, True, rate, score=(main_score+client_score), corner=cornerSum)

                key = client
                result_slice = addData(result_slice, key, gameTime, -1,rate=rate, score=(main_score+client_score),corner=cornerSum)

            elif main_score - client_score + rate < 0:
                key = client
                result_slice = addData(result_slice, key, gameTime, 1,rate=rate, score=(main_score+client_score),corner=cornerSum)

                key = main
                result_slice = addData(result_slice, key, gameTime, -1, True,rate=rate, score=(main_score+client_score),corner=cornerSum)
            else :
                key = client
                result_slice = addData(result_slice, key, gameTime, 0,rate=rate, score=(main_score+client_score),corner=cornerSum)

                key = main
                result_slice = addData(result_slice, key, gameTime, 0, True,rate=rate, score=(main_score+client_score),corner=cornerSum)


            if main_score - client_score> 0:
                key = main
                result_slice_v2 = addData(result_slice_v2, key, gameTime, 1, True, score=(main_score+client_score),corner=cornerSum)

                key = client
                result_slice_v2 = addData(result_slice_v2, key, gameTime, -1, score=(main_score+client_score),corner=cornerSum)

            elif main_score - client_score < 0:
                key = client
                result_slice_v2 = addData(result_slice_v2, key, gameTime, 1, score=(main_score+client_score),corner=cornerSum)

                key = main
                result_slice_v2 = addData(result_slice_v2, key, gameTime, -1, True, score=(main_score+client_score),corner=cornerSum)
            else :
                key = client
                result_slice_v2 = addData(result_slice_v2, key, gameTime, 0, score=(main_score+client_score),corner=cornerSum)

                key = main
                result_slice_v2 = addData(result_slice_v2, key, gameTime, 0, True, score=(main_score+client_score),corner=cornerSum)
            

        rateMax = rateParam
        for gameTotalTmp in range(loopSize):
            for chechSumTmp in range(1):
                # chechSum = gameTotal - 1

                # if loopSize == 1:
                #     gameTotalTmp = gameParam - 1

                gameTotal = gameTotalTmp + 2
                chechSum = gameTotalTmp + 2

                # gameTotal = 3
                # chechSum = 3

                winSum = 0
                lostSum = 0

                checkScoreMin = getMinValue()
                checkGameSum = 0

                win_winScore = 0
                win_lostScore = 0
                lost_winScore = 0
                lost_lostScore = 0


                main_win_size = 0
                main_lost_size = 0
                client_win_size = 0
                client_lost_size = 0

                winCorner = 0
                lostCorner = 0
                checkCorner = getMinValue()

                win_winCorner = 0
                win_lostCorner = 0
                lost_winCorner = 0
                lost_lostCorner = 0
                # checkWinCorner = 0
                checkParam = 30

                comCheck = {}

                ping = 0
                for result in result_slice:
                    tmp = result_slice[result]  # 让球
                    tmp_v2 = result_slice_v2[result] #不让球
                    sorted(tmp.keys(),reverse=True)
                    index = 0
                    keys = list(tmp.keys())
                    keys.sort()
                    # print(result)
                    
                    while index + gameTotal < len(keys):
                        gameTmp = []
                        gameTmp_v2 = [] #不让球
                        for add in range(gameTotal):
                            gameTmp.append(tmp[keys[index + add]])
                            gameTmp_v2.append(tmp_v2[keys[index + add]]) #不让球
                        game_check = tmp[keys[index + gameTotal]] 
                        game_check_v2 = tmp_v2[keys[index + gameTotal]]  #不让球

                        game_check_pre = tmp[keys[index + gameTotal - 1]]

                        lost = 0

                        def chechResult( gameTmp, lost):
                            cond = (gameTmp == 1)
                            # if ngeFlag:
                            #     cond = (gameTmp == 1)

                            if cond :
                                return 1
                            return 0

                        for tmp_1 in gameTmp_v2: #不让球
                        # for tmp_1 in gameTmp:
                            lost += chechResult(tmp_1[0], lost)

                        cond_1 = (game_check[2] >= 0) 
                        cond_2 = (lost == chechSum)
                        # if ngeFlag :
                        #     cond_2 = (lost == 0) 

                        # cond_2 = (lost == chechSum-1) and (gameTmp[0][0] != -1)

                        gameCheck = game_check #让球

                        # gameCheck = game_check_v2  #不让球

                        scorePerGame = scoreMin.getResult()
                        # cornerPerGame = cornerTotal / gameSum
                        cornerPerGame = cornerMin.getResult()
                        if cond_2 and gameCheck[0] > 0 :
                            winSum += 1

                            # checkScoreSum += gameCheck[3]
                            checkScoreMin.add(gameCheck[3])
                            checkGameSum += 1
                            key = ""
                            if gameCheck[3] > scorePerGame:
                                win_winScore += 1
                                key +="大球 "
                            else:
                                win_lostScore += 1
                                key +="小球 "

                            winCorner += gameCheck[4]
                            checkCorner.add(gameCheck[4]) 

                            if gameCheck[4] > cornerPerGame:
                                win_winCorner += 1
                                key += "大角"
                            else:
                                win_lostCorner += 1
                                key += "小角"

                            if comCheck.__contains__(key) == False:
                                comCheck[key] = 0
                            comCheck[key] += 1

                        elif cond_2 and gameCheck[0] == -1:
                            lostSum += 1
                            # lostScore += gameCheck[3]

                            # checkScoreSum += gameCheck[3]
                            checkScoreMin.add(gameCheck[3])
                            checkGameSum += 1

                            key = ""
                            if gameCheck[3] > scorePerGame:
                                lost_winScore += 1
                                key +="大球 "
                            else:
                                lost_lostScore += 1
                                key +="小球 "

                            lostCorner += gameCheck[4]
                            checkCorner.add(gameCheck[4]) 


                            if gameCheck[4] > cornerPerGame:
                                lost_winCorner += 1
                                key += "大角"
                            else:
                                lost_lostCorner += 1
                                key += "小角"

                            if comCheck.__contains__(key) == False:
                                comCheck[key] = 0
                            comCheck[key] += 1

                        # elif cond_2:
                        #     # print(index)
                        #     # index = index
                        #     ping += 1
                        #     if gameCheck[3] > scorePerGame:
                        #         win_winScore += 1
                        #     else:
                        #         win_lostScore += 1

                        index += 1
                    # print(result, winSum, lostSum)
                if lostSum == 0:
                    continue
                rate  = winSum * 100 /(winSum+ lostSum)

                
                cond = (rateMax > rate and (checkGameSum > checkParam))
                infoType = "比小"
                if rateParam < 0:
                    cond = (rateMax < rate  and (checkGameSum > checkParam))
                    infoType = "比大"


                # # 让球
                if cond and checkType == 1:
                    rateMax = rate
                    winRate = round(winSum*100/(winSum+lostSum), 2)
                    # info = "{} {}  总场数：{}    连输数：{}   赢球比例：{}%    赢球场数：{}       输球数：{}".format(infoType, name,len(data),gameTotal,winRate,winSum,lostSum)
                    
                    info = "让胜"
                    if rate < 50:
                        info = "让输"

                    rateDivNew = abs(winRate - 50)
                    rateDivOld = 0
                    if infoList.__contains__(name):
                        rateDivOld = abs(infoList[name][4] - 50)

                    if rateDivNew > rateDivOld and rateDivNew > 5:
                        infoList[name]=[param[0], gameTotal, param[1], info, winRate, winRate]
                    
                


                # 大小球
                checkScorePer = round(checkScoreMin.getResult(),2)
                scorePerGame = round(scorePerGame,2)
                rate = (win_winScore + lost_winScore)*100/(win_winScore + lost_winScore + win_lostScore + lost_lostScore)
                if (lost_lostScore + lost_winScore) == 0 or (win_lostScore + win_winScore) == 0:
                    continue  

                cond = (rateMax > rate and (checkGameSum > checkParam))
                if rateParam < 0:
                    cond = (rateMax < rate and (checkGameSum > checkParam))
                if cond and checkType == 2:
                    rateMax = rate
                    winBig = win_winScore*100/(win_lostScore + win_winScore)
                    lostBig = lost_winScore*100/(lost_lostScore + lost_winScore)
                    # if abs(rate - 50) < 5 and abs(winBig - 50) < 5 and abs(lostBig - 50) < 5:
                    #     continue
                    # info = "{} {}  连输数：{}   大球比率：{}%    平均进球：{}".format(infoType, name,gameTotal,round(rate,1),scorePerGame)
                    
                    info = "大球"
                    if rate < 50:
                        info = "小球"

                    rateDivNew = abs(rate - 50)
                    rateDivOld = 0
                    if infoList.__contains__(name):
                        rateDivOld = abs(infoList[name][4] - 50)

                    if rateDivNew > rateDivOld and rateDivNew > 6:
                        infoList[name]=[param[0], gameTotal, param[1], info, rate, checkScorePer]

                # 角球
                checkCornerPer = round(checkCorner.getResult(), 2)
                cornerPerGame = round(cornerPerGame,2)
                rate = (win_winCorner + lost_winCorner)*100/(win_winCorner + lost_winCorner + win_lostCorner + lost_lostCorner)

                winBig = win_winCorner*100/(win_lostCorner + win_winCorner)
                lostBig = lost_winCorner*100/(lost_lostCorner + lost_winCorner)
                checkWeig = rate * 0.01 * checkGameSum

                cond = (rateMax > rate and (checkGameSum > checkParam))
                if rateParam < 0:
                    cond = (rateMax < rate and len(data)/(winSum+lostSum) < checkParam)
                if cond and checkType == 3:
                    rateMax = rate
                    # info = "{} {}  连输数：{}   大角比率：{}%    场均角球：{}".format(infoType, name,gameTotal,round(rate,1),cornerPerGame)

                    info = "大角"
                    if rate < 50:
                        info = "小角"

                    rateDivNew = abs(rate - 50)
                    rateDivOld = 0
                    if infoList.__contains__(name):
                        rateDivOld = abs(infoList[name][4] - 50)

                    if rateDivNew > rateDivOld and rateDivNew > 9:
                        infoList[name]=[param[0], gameTotal, param[1], info, rate, checkCornerPer]

                if checkType == 4:
                    for key in  comCheck:
                        dataTmp =  comCheck[key]
                        rate = round(dataTmp*100 / checkGameSum,2)

                        rateDivNew = rate 
                        rateDivOld = 0
                        if infoList.__contains__(name):
                            rateDivOld = abs(infoList[name][4])

                        if rateDivNew > rateDivOld and rateDivNew >= 35:
                            infoList[name]=[param[0], gameTotal, param[1], key, rate,rate]

    def working(type):
        for param in params:
            getResult(param, -1, type)

        if type != 4:
            for param in params:
                getResult(param, 100, type)

        tableName = ""
        if type == 1:
            tableName = "k_rateBuy"
        elif type == 2: 
            tableName = "k_scoreBuy"
        elif type == 3: 
            tableName = "k_cornerBuy"
        elif type == 4: 
            tableName = "k_compBuy"
        tableName += "_v2"

        sql.cleanAll(tableName)

        big = [0,0]
        small = [0,0]
        for index in infoList:
            tmp = infoList[index]
            info = "'{}','{}','{}','{}','{}'".format(tmp[0],tmp[1],tmp[2],tmp[3],tmp[5])
            sql.insert(info, tableName)
            print(tmp)
            if tmp[4] > 50:
                big[0] += tmp[4]
                big[1] += 1
            else :
                small[0] += tmp[4]
                small[1] += 1
        print(tableName, "small",small[0]/small[1])
        if type != 4:
            print(tableName, "big",big[0]/big[1])

        infoList.clear()

    working(1)
    working(2)
    working(3)
    working(4)

