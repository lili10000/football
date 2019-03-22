from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')

name = None
# name = "英超"
loopSize = 3
# loopSize = 1

params = [

    ["罗甲"  , 4],
    ["罗乙"  , 4]
    # ["罗马LIII"  , 4],
    # ["澳维超2"  , 4],
    # ["西澳超"  , 4],
    # ["德丙"  , 4],
    # ["意大利丙A"  , 4],
    # ["苏乙"  , 4]


    # ["阿尔甲"  , 4],
    # ["阿尔乙"  , 4],
    # ["埃及超"  , 4],
    # ["埃及乙"  , 4],
    # ["澳维超"  , 4],
    # ["爱超"  , 4],
    # ["爱甲"  , 4]

    # ["法N"  , 4],
    # ["以乙南"  , 4],
    # ["以乙北"  , 4],
    # ["哥伦甲"  , 4],
    # ["瑞典甲"  , 4],
    # ["英北超"  , 4],
    # ["英全联"  , 4],
    # ["英联北"  , 4],
    # ["英联南"  , 4],
    # ["丹甲"   , 4],
    # ["墨乙"   , 4],
    # ["俄甲"   , 4],
    # ["德丙"   , 4],
    # ["苏冠"   , 4],
    # ["捷甲"   , 4]
    # ["马来超", 4],
    # ["伊朗超", 2],
    # ["墨秋联", 3],
    # ["墨春联", 3],
    # ["巴西乙", 3],
    # ["美职联", 3],
    # ["韩k联", 2],
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
    # ["意甲", 3],
    # ["土超", 2],
    # ["以超", 3],
    # ["荷乙", 2],
    # ["葡超", 3],
    # ["英甲", 3],
    # ["英乙", 3],
    # ["俄超", 2],
    # ["法乙", 3],
    # ["澳超", 3]
]
infoList = {}

# name = '荷乙'

ngeFlag =True
ngeFlag =False

def getResult(param, rateParam):
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
        

    rateMax = rateParam
    for gameTotalTmp in range(loopSize):
        for chechSumTmp in range(1):
            # chechSum = gameTotal - 1

            if loopSize == 1:
                gameTotalTmp = gameParam - 1

            gameTotal = gameTotalTmp + 2
            chechSum = gameTotalTmp + 2

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
            checkParam = 30

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

            
            cond = (rateMax > rate and (checkGameSum > checkParam))
            infoType = "比小"
            if rateParam < 0:
                cond = (rateMax < rate  and (checkGameSum > checkParam))
                infoType = "比大"


            # # 让球
            if cond:
                rateMax = rate
                winRate = round(winSum*100/(winSum+lostSum))
                info = "{} {}  总场数：{}    连输数：{}   赢球比例：{}%    赢球场数：{}       输球数：{}".format(infoType, name,len(data),gameTotal,winRate,winSum,lostSum)
                infoList[infoType + " " +name]=info
            


            # 大小球
            # checkScorePer = round(checkScoreSum / checkGameSum,2)
            # scorePerGame = round(scorePerGame,2)
            # rate = (win_winScore + lost_winScore)*100/(win_winScore + lost_winScore + win_lostScore + lost_lostScore)
            # if (lost_lostScore + lost_winScore) == 0 or (win_lostScore + win_winScore) == 0:
            #     continue  

            # cond = (rateMax > rate and (checkGameSum > checkParam))
            # if rateParam < 0:
            #     cond = (rateMax < rate and (checkGameSum > checkParam))
            # if cond:
            #     rateMax = rate
            #     winBig = win_winScore*100/(win_lostScore + win_winScore)
            #     lostBig = lost_winScore*100/(lost_lostScore + lost_winScore)
            #     # if abs(rate - 50) < 5 and abs(winBig - 50) < 5 and abs(lostBig - 50) < 5:
            #     #     continue
            #     info = "{} {}  连输数：{}   大球比率：{}%    平均进球：{}".format(infoType, name,gameTotal,round(rate,1),scorePerGame)
            #     infoList[infoType + " " +name]=info


            # 角球
            # checkCornerPer = round(checkCorner / checkGameSum,2)
            # cornerPerGame = round(cornerPerGame,2)
            # rate = (win_winCorner + lost_winCorner)*100/(win_winCorner + lost_winCorner + win_lostCorner + lost_lostCorner)

            # winBig = win_winCorner*100/(win_lostCorner + win_winCorner)
            # lostBig = lost_winCorner*100/(lost_lostCorner + lost_winCorner)
            # checkWeig = rate * 0.01 * checkGameSum

            # cond = (rateMax > rate and (checkGameSum > checkParam))
            # if rateParam < 0:
            #     cond = (rateMax < rate and len(data)/(winSum+lostSum) < checkParam)
            # if cond:
            #     rateMax = rate
            #     info = "{} {}  连输数：{}   大角比率：{}%    场均角球：{}".format(infoType, name,gameTotal,round(rate,1),cornerPerGame)
            #     infoList[infoType + " " +name]=info

            

for param in params:
    getResult(param, -1)

for param in params:
    getResult(param, 100)


for info in infoList:
    print(infoList[info])