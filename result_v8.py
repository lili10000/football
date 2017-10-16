from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20


def getResult_1(name, rateMin, rateMax):
    # data = sql.queryByType(name, "k_163_2016")
    data = sql.queryByType(name, "k_163_2017")

    main_win = 0
    client_win = 0
    tie_win = 0

    winScoreSum = 0
    lostScoreSum = 0

    winSize = 0
    lostSize = 0 

    size = 0
    sizeAll = 0

    scoreAll = 0
    score_total =[0, 0, 0, 0, 0, 0]

    rate_1 = 0
    rate_2 = 0

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main = one[0]
        client = one[1]

        main_win =  one[8]
        client_win = one[9]

        result = int(one[4])

        sizeAll += 1

        # teamName = "佩斯卡拉"
        # if (main == teamName) or (client == teamName):
        #     continue

        # teamName = "莱切斯特"
        # if (main == teamName) or (client == teamName):
        #     continue

        # teamName = "斯托克城"
        # if (main == teamName) or (client == teamName):
        #     continue


        # rateMax = 1.8
        # rateMin = 1.5
        condition_1 = (main_win < rateMax and main_win > rateMin and main_win < client_win)
        condition_2 = (client_win < rateMax and client_win > rateMin and client_win < main_win )
        if condition_1:
            if result == 1:
                rate_1 += main_win - 1
            else:
                rate_1 -= 1
            size += 1 
        elif  condition_2:
            if result == -1:
                rate_1 += client_win - 1
            else:
                rate_1 -= 1
            size += 1 

        if condition_1:
            if result == -1:
                rate_2 += client_win - 1
            else:
                rate_2 -= 1
        elif  condition_2:
            if result == 1:
                rate_2 += main_win - 1
            else:
                rate_2 -= 1


    print(name,round(rateMin, 2), "买赢：", rate_1, " 买输：", rate_2, " size = ", size, " size all = ",sizeAll)
    #print(name, "买赢率：", rate_1/size, " 买输率：", rate_2/size)

       


def compare_1(name): 
    for i in range(14) :
        rateMin = i*0.1 + 1
        rateMax = rateMin + 0.1*1
        getResult_1(name, rateMin,  rateMax)
def compare_2(name): 
    getResult_1(name, 1.4,  2)

compare_2("英超")
# compare_2("意甲")
# compare_1("西甲")
# compare_1("德甲")

# compare_2("英冠")
# compare_1("英甲")
# compare_2("巴甲")
# compare_2("J联赛")
