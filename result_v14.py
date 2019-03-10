from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')

name = None
name = "意甲"
# name = '荷乙'

ngeFlag =True
ngeFlag =False

def getResult(name):
    data = []
    if name == None:
        data = sql.queryByTypeAll("k_corner")
    else:
        data = sql.queryByType(name, "k_corner")

    if len(data) == 0 :
        return
    print("sum = ", len(data))

    win_size = 0
    lost_size = 0




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
        gameTime = one[9]

        if rate == "-":
            continue
        
        rate = float(rate)
        def addData(result_slice, key, gameTime, value, mainFlag=False, rate=0, score=0):
            if result_slice.__contains__(key) == False:
                result_slice[key] = {}
            result_slice[key][gameTime] = [value, mainFlag, rate, score]
            return result_slice

        if main_score - client_score + rate> 0:
            key = main
            result_slice = addData(result_slice, key, gameTime, 1, True, rate, score=(main_score+client_score))

            key = client
            result_slice = addData(result_slice, key, gameTime, -1,rate=rate, score=(main_score+client_score))

        elif main_score - client_score + rate < 0:
            key = client
            result_slice = addData(result_slice, key, gameTime, 1,rate=rate, score=(main_score+client_score))

            key = main
            result_slice = addData(result_slice, key, gameTime, -1, True,rate=rate, score=(main_score+client_score))
        else :
            key = client
            result_slice = addData(result_slice, key, gameTime, 0,rate=rate, score=(main_score+client_score))

            key = main
            result_slice = addData(result_slice, key, gameTime, 0, True,rate=rate, score=(main_score+client_score))


        if main_score - client_score> 0:
            key = main
            result_slice_v2 = addData(result_slice_v2, key, gameTime, 1, True, score=(main_score+client_score))

            key = client
            result_slice_v2 = addData(result_slice_v2, key, gameTime, -1, score=(main_score+client_score))

        elif main_score - client_score < 0:
            key = client
            result_slice_v2 = addData(result_slice_v2, key, gameTime, 1, score=(main_score+client_score))

            key = main
            result_slice_v2 = addData(result_slice_v2, key, gameTime, -1, True, score=(main_score+client_score))
        else :
            key = client
            result_slice_v2 = addData(result_slice_v2, key, gameTime, 0, score=(main_score+client_score))

            key = main
            result_slice_v2 = addData(result_slice_v2, key, gameTime, 0, True, score=(main_score+client_score))
        
    rateMax = -1
    loopSize = 10
    # loopSize = 1
    for gameTotalTmp in range(loopSize):
        for chechSumTmp in range(1):
            # chechSum = gameTotal - 1

            gameTotal = gameTotalTmp + 1
            chechSum = gameTotalTmp + 1

            # gameTotal = 3
            # chechSum = 3

            winSum = 0
            lostSum = 0

            main_winScore = 0
            main_lostScore = 0
            client_winScore = 0
            client_lostScore = 0


            main_win_size = 0
            main_lost_size = 0
            client_win_size = 0
            client_lost_size = 0

            for result in result_slice:
                tmp = result_slice[result]  # 让球
                tmp_v2 = result_slice_v2[result]
                sorted(tmp.keys(),reverse=True)
                index = 0
                keys = list(tmp.keys())
                keys.sort()
                # print(result)
                
                while index + gameTotal < len(keys):
                    gameTmp = []
                    gameTmp_v2 = []
                    for add in range(gameTotal):
                        gameTmp.append(tmp[keys[index + add]])
                        gameTmp_v2.append(tmp_v2[keys[index + add]])
                    game_check = tmp[keys[index + gameTotal]] 
                    game_check_v2 = tmp_v2[keys[index + gameTotal]] 

                    game_check_pre = tmp[keys[index + gameTotal - 1]]

                    lost = 0

                    def chechResult( gameTmp, lost):
                        cond = (gameTmp == -1)
                        # if ngeFlag:
                        #     cond = (gameTmp == 1)

                        if cond :
                            return 1
                        return 0

                    for tmp_1 in gameTmp_v2:
                    # for tmp_1 in gameTmp:
                        lost += chechResult(tmp_1[0], lost)

                    cond_1 = (game_check[2] >= 0) 
                    cond_2 = (lost == chechSum) 
                    # if ngeFlag :
                    #     cond_2 = (lost == 0) 

                    # cond_2 = (lost == chechSum-1) and (gameTmp[0][0] != -1)

                    gameCheck = game_check
                    # gameCheck = game_check_v2
                    if cond_2 and gameCheck[0] > 0 :
                        winSum += 1

                        if gameCheck[3] > 2.5:
                            main_winScore += 1
                        else:
                            main_lostScore += 1


                        # if cond_1:
                        #     main_win_size += 1
                        
                        # if game_check[1]:
                        #     main_win_size += 1
                        # else:
                        #     client_win_size += 1

                    elif cond_2 and gameCheck[0] == -1:
                        lostSum += 1
                        # lostScore += gameCheck[3]


                        if gameCheck[3] > 2:
                            client_winScore += 1
                        else:
                            client_lostScore += 1

                        # if cond_1:
                        #     main_lost_size += 1


                        
                        # if game_check[1]:
                        #     main_lost_size += 1
                        # else:
                        #     client_lost_size += 1
                    else:
                        # print(index)
                        index = index

                    index += 1
                # print(result, winSum, lostSum)
            if lostSum == 0:
                continue
            rate  = winSum / lostSum

            if rateMax < rate:
                rateMax = rate
            print(name, gameTotal,"场输",chechSum,"场, 后一场,赢",winSum,"  ", round(winSum*100/(winSum+lostSum)),"%", "输",lostSum)
            print("赢",  round(main_winScore*100/(main_lostScore + main_winScore),2),"%",  round(client_winScore*100/(client_lostScore + client_winScore),2),"%")
                # print("     主客场比    赢",main_win_size,client_win_size,   round(main_win_size*100/(main_win_size+client_win_size)),"%    输",main_lost_size, client_lost_size, round(main_lost_size*100/(main_lost_size+client_lost_size)),"%")
                # print("     只买主  ", main_win_size, main_lost_size, round(main_win_size*100/(main_win_size+main_lost_size)),"%")


getResult(name)
