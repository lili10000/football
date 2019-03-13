from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')

name = None
# name = "英超"
loopSize = 10
loopSize = 1
params = [
    ["葡超", 3],
    ["英甲", 3],
    ["英乙", 3],
    ["墨秋联", 3],
    ["墨春联", 3],
    ["巴西乙", 3]

    # ["英超", 3],
    # ["巴甲", 2],
    # ["意乙", 2],
    # ["法甲", 2],
    # ["荷甲", 3],
    # ["德甲", 4],
    # ["阿甲", 2],
    # ["中超", 3],
    # ["英冠", 3],
    # ["西甲", 2],
    # ["德乙", 3],
    # ["苏超", 2],
    # ["美职联", 3],
    # ["韩k联", 2],
    # ["意甲", 3],
    # ["土超", 2],
    # ["以超", 3],
    # ["马来超", 4],
    # ["荷乙", 2],
    # ["伊朗超", 2],
    # ["俄超", 2],
    # ["法乙", 3],
    # ["澳超", 3]
]


# name = '荷乙'

ngeFlag =True
ngeFlag =False

def getResult(param):
    data = []
    name = param[0]
    gameParam = param[1]

    if name == None:
        data = sql.queryByTypeAll("k_corner")
    else:
        data = sql.queryByType(name, "k_corner")

    if len(data) == 0 :
        return
    print("sum = ", len(data))

    win_size = 0
    lost_size = 0

    scoreSum = 0
    gameSum = 0

    cornerTotal = 0

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

        
        scoreSum += main_score + client_score
        cornerTotal += cornerSum
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
        
    rateMax = -1

    for gameTotalTmp in range(loopSize):
        for chechSumTmp in range(1):
            # chechSum = gameTotal - 1

            if loopSize == 1:
                gameTotalTmp = gameParam - 1

            gameTotal = gameTotalTmp + 1
            chechSum = gameTotalTmp + 1

            # gameTotal = 3
            # chechSum = 3

            winSum = 0
            lostSum = 0

            checkScoreSum = 0
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
            checkCorner = 0

            win_winCorner = 0
            win_lostCorner = 0
            lost_winCorner = 0
            lost_lostCorner = 0
            # checkWinCorner = 0

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
                        cond = (gameTmp == -1)
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

                    scorePerGame = scoreSum / gameSum
                    cornerPerGame = cornerTotal / gameSum
                    if cond_2 and gameCheck[0] > 0 :
                        winSum += 1

                        checkScoreSum += gameCheck[3]
                        checkGameSum += 1
                        if gameCheck[3] > scorePerGame:
                            win_winScore += 1
                        else:
                            win_lostScore += 1

                        winCorner += gameCheck[4]
                        checkCorner += gameCheck[4]

                        if gameCheck[4] > cornerPerGame:
                            win_winCorner += 1
                        else:
                            win_lostCorner += 1

                    elif cond_2 and gameCheck[0] == -1:
                        lostSum += 1
                        # lostScore += gameCheck[3]

                        checkScoreSum += gameCheck[3]
                        checkGameSum += 1

                        if gameCheck[3] > scorePerGame:
                            lost_winScore += 1
                        else:
                            lost_lostScore += 1

                        lostCorner += gameCheck[4]
                        checkCorner += gameCheck[4]


                        if gameCheck[4] > cornerPerGame:
                            lost_winCorner += 1
                        else:
                            lost_lostCorner += 1


                        # if cond_1:
                        #     main_lost_size += 1


                        
                        # if game_check[1]:
                        #     main_lost_size += 1
                        # else:
                        #     client_lost_size += 1
                    elif cond_2:
                        # print(index)
                        # index = index
                        ping += 1
                        if gameCheck[3] > scorePerGame:
                            win_winScore += 1
                        else:
                            win_lostScore += 1

                    index += 1
                # print(result, winSum, lostSum)
            if lostSum == 0:
                continue
            rate  = winSum / lostSum

                # rateMax = 100
                # if rateMax > rate:
                # if rateMax < rate:
                #     rateMax = rate

            # print(name, gameTotal,"场输",chechSum,"场, 后一场,赢",winSum,"  ", round(winSum*100/(winSum+lostSum)),"%", "输",lostSum, ping)
            checkScorePer = round(checkScoreSum / checkGameSum,2)
            scorePerGame = round(scorePerGame,2)
            rate = (win_winScore + lost_winScore)*100/(win_winScore + lost_winScore + win_lostScore + lost_lostScore)
            if (lost_lostScore + lost_winScore) == 0 or (win_lostScore + win_winScore) == 0:
                continue  
            # print(name, gameTotal,scorePerGame, round(scorePerGame - checkScorePer,2), "    比率：",round(rate,2),"%", "    赢大：",round(win_winScore*100/(win_lostScore + win_winScore),2),"%",  "    输大：",round(lost_winScore*100/(lost_lostScore + lost_winScore),2),"%")
                # print("     主客场比    赢",main_win_size,client_win_size,   round(main_win_size*100/(main_win_size+client_win_size)),"%    输",main_lost_size, client_lost_size, round(main_lost_size*100/(main_lost_size+client_lost_size)),"%")
                # print("     只买主  ", main_win_size, main_lost_size, round(main_win_size*100/(main_win_size+main_lost_size)),"%")

            checkCornerPer = round(checkCorner / checkGameSum,2)
            cornerPerGame = round(cornerPerGame,2)
            rate = (win_winCorner + lost_winCorner)*100/(win_winCorner + lost_winCorner + win_lostCorner + lost_lostCorner)

            winBig = win_winCorner*100/(win_lostCorner + win_winCorner)
            lostBig = lost_winCorner*100/(lost_lostCorner + lost_winCorner)

            if abs(rate - 50) < 5 and abs(winBig - 50) and abs(lostBig - 50):
                continue
            print(name, gameTotal,cornerPerGame, round(cornerPerGame - checkCornerPer,2), "    比率：",round(rate,2),"%", "    角球赢大：",round(winBig,2),"%",  "    角球输大：",round(lostBig,2),"%")


for param in params:
    getResult(param)
