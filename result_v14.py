from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')

name = None
# name = "英超"
name = '法乙'


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

    main_win_size = 0
    main_lost_size = 0
    client_win_size = 0
    client_lost_size = 0



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
        rate = float(one[4])
        gameType = one[5]
        gameTime = one[9]


        def addData(result_slice, key, gameTime, value):
            if result_slice.__contains__(key) == False:
                result_slice[key] = {}
            result_slice[key][gameTime] = value
            return result_slice

        if main_score - client_score + rate> 0:
            key = main
            result_slice = addData(result_slice, key, gameTime, 1)

            key = client
            result_slice = addData(result_slice, key, gameTime, -1)

        elif main_score - client_score + rate < 0:
            key = client
            result_slice = addData(result_slice, key, gameTime, 1)

            key = main
            result_slice = addData(result_slice, key, gameTime, -1)
        else :
            key = client
            result_slice = addData(result_slice, key, gameTime, 0)

            key = main
            result_slice = addData(result_slice, key, gameTime, 0)


        if main_score - client_score> 0:
            key = main
            result_slice_v2 = addData(result_slice_v2, key, gameTime, 1)

            key = client
            result_slice_v2 = addData(result_slice_v2, key, gameTime, -1)

        elif main_score - client_score < 0:
            key = client
            result_slice_v2 = addData(result_slice_v2, key, gameTime, 1)

            key = main
            result_slice_v2 = addData(result_slice_v2, key, gameTime, -1)
        else :
            key = client
            result_slice_v2 = addData(result_slice_v2, key, gameTime, 0)

            key = main
            result_slice_v2 = addData(result_slice_v2, key, gameTime, 0)
        
    rateMax = -1
    loopSize = 10
    # loopSize = 1
    for gameTotalTmp in range(loopSize):
        for chechSumTmp in range(1):
            # chechSum = gameTotal - 1

            gameTotal = gameTotalTmp + 1
            chechSum = gameTotalTmp + 1

            winSum = 0
            lostSum = 0


            for result in result_slice:
                tmp = result_slice[result]
                tmp_v2 = result_slice_v2[result]
                sorted(tmp.keys(),reverse=True)
                index = 0
                keys = list(tmp.keys())
                keys.sort()
                # print(result)
                
                while index + gameTotal < len(keys):
                    gameTmp = []
                    for add in range(gameTotal):
                        gameTmp.append(tmp_v2[keys[index + add]])
                    game_check = tmp[keys[index + gameTotal]] 

                    lost = 0

                    def chechResult( gameTmp, lost):
                        if gameTmp == -1 :
                            return 1
                        return 0

                    for tmp_1 in gameTmp:
                        lost += chechResult(tmp_1, lost)

                    if lost == chechSum and game_check > 0:
                        winSum += 1
                    elif lost == chechSum and game_check == -1:
                        lostSum += 1
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


getResult(name)