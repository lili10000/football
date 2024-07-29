from db.mysql import sqlMgr

indexList = [0,0,0,0]
rateList = {}
def checkMain():

    sql = sqlMgr('localhost', 'root', '861217', 'football')
    gameCode = sql.queryByTypeAll("k_gamedic")

    outputInfo={}
    tableName = "k_rateDiv"
    sql.cleanAll(tableName)
    size = 0
    rateSum = 0

    big_1 = 0
    big_2 = 0
    small_1 = 0
    small_2 = 0
    for code in gameCode:
        id = code[0]
        gameName = code[1]
        data = sql.queryByTypeTime(gameName, 'k_corner')

        
        outputInfo = {}
   
        result = {}

        total = len(data)
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

            

            rateWinFlag = False
            if main_score - client_score + rate> 0:
                rateWinFlag = True
            elif main_score - client_score + rate < 0:
                rateWinFlag = False
            else :
                continue


            BigFlag = False
            if main_score + client_score - scoreRate > 0:
                BigFlag = True
            elif main_score + client_score - scoreRate < 0:
                BigFlag = False
            else :
                continue

            dan = ((main_score + client_score) % 2 == 1)
            shuang = ((main_score + client_score) % 2 == 0)
            checkFlag = BigFlag
            if checkFlag and dan:
                big_1 += 1
            elif checkFlag and shuang:
                big_2 += 1
            elif checkFlag == False and dan:
                small_1 += 1
            elif checkFlag == False and shuang:
                small_2 += 1

            key = ""
            if rate > 0:
                key = "主弱"
            elif key < 0:
                key = "主强"
            else:
                key = "平"

            if result.__contains__(key) == False:
                result[key]={}



            rateDiv = scoreRate - abs(rate)
            if result[key].__contains__(rateDiv) == False:
                result[key][rateDiv] = [0, 0, 0, 0]
            if result[key].__contains__("all") == False:
                result[key][rateDiv] = [0, 0, 0, 0]

            tmp = result[key][rateDiv]
            alltmp = result[key]["all"]
            
            if rateWinFlag and BigFlag:
                tmp[0] += 1
                alltmp[0] += 1
            elif rateWinFlag  and BigFlag == False:
                tmp[1] += 1
                alltmp[0] += 1
            elif rateWinFlag  == False and BigFlag:
                tmp[2] += 1
                alltmp[0] += 1
            elif rateWinFlag  == False and BigFlag == False:
                tmp[3] += 1
                alltmp[0] += 1

            result[key][rateDiv] = tmp
            result[key]["all"] = alltmp






        # bigMax = -1
        # info = "让"
        # getData = []
        # rateDiv = 0
        # rateTmp = 0
       
        # info = ""
        # rateMax = 0
        # keyTmp = 0
        # for key in result:

        #     # if key < 1.5 or key > 2.25:
        #     #     continue

        #     data = result[key]
        #     dataSum = data[0] + data[1]+ data[2]+ data[3]
            

        #     def getRate(sum, data, rateCmp, index):
        #         # global indexList
        #         tmpRate = round(data/sum, 2)
        #         if rateCmp < tmpRate:
        #             if tmpRate > 0.3:
        #                 indexList[index] += 1
        #             return tmpRate
        #         return rateCmp
            
        #     rateTmp = rateMax
        #     rateTmp = getRate(dataSum, data[0], rateTmp, 0)
        #     rateTmp = getRate(dataSum, data[1], rateTmp, 1)
        #     rateTmp = getRate(dataSum, data[2], rateTmp, 2)
        #     rateTmp = getRate(dataSum, data[3], rateTmp, 3)

        #     if rateTmp > 0.3 and dataSum > 0.03*total and rateTmp > rateMax:
        #         rateMax = rateTmp
        #         keyTmp = key
        #         input = "'{}','{}'".format(code[0], code[1])
        #         sql.insert(input, "k_gamedic_v3")
                # indexTmp = 0
                # if data[indexTmp] < data[1] :
                #     indexTmp = 1
                # if data[indexTmp] < data[2] :
                #     indexTmp = 2
                # if data[indexTmp] < data[3] :
                #     indexTmp = 3

                # indexList[indexTmp] += 1

                # info = "【{}】 {}, {}, {}".format(gameName,rateMax, key, data)


        # if len(info) > 0:

    #     if not rateList.__contains__(keyTmp):
    #         rateList[keyTmp] = 0
    #     rateList[keyTmp] += 1
    
    # print(indexList) 

    # print(round(big_1/(big_1+big_2),2), round(big_2/(big_1+big_2),2), round(small_1/(small_1+small_2),2), round(small_2/(small_1+small_2),2))

    # keys = list(rateList.keys())
    # keys.sort(reverse = True)
    # for key in keys:
    #     print(key, rateList[key])
            
# checkMain()