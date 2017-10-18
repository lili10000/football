from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20

Kong = 1

def getResult_1(name, rateMin, rateMax, num):
    db_name = "k_163_2017"

    data = sql.queryByTypeNum(name, db_name, str(num))
    if num == -1 :
        data = sql.queryByType(name, db_name)

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
    rate_3 = 0

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main = one[0]
        client = one[1]

        ping = one[6]
        main_win =  one[8]
        client_win = one[9]

        result = int(one[4])

        sizeAll += 1

        condition_1 = (main_win < rateMax and main_win > rateMin and main_win < client_win)
        condition_2 = (client_win < rateMax and client_win > rateMin and client_win < main_win )
        if condition_1:
            if result == 1:
                rate_1 += main_win - 1
            else:
                rate_1 -= 1
            
            if result == 0:
                rate_3 += ping -1 
            else :
                rate_3 -= 1

            size += 1 
        elif  condition_2:
            if result == -1:
                rate_1 += client_win - 1
            else:
                rate_1 -= 1

            if result == 0:
                rate_3 += ping -1 
            else :
                rate_3 -= 1
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
 
    print(name,round(rateMin, 2), "num:", num, "买赢：", round(rate_1, 2), " 买输：", round(rate_2, 2), " size = ", size, " size all = ",sizeAll)
       
def getResult_2(name, rateMin, rateMax, num):
    db_name = "k_163_2016"

    data = sql.queryByTypeNum(name, db_name, str(num))
    if num == -1 :
        data = sql.queryByType(name, db_name)

    main_win = 0
    client_win = 0
    tie_win = 0


    size = 0
    sizeAll = 0

    rate_1 = 0
    rate_2 = 0
    rate_3 = 0

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main = one[0]
        client = one[1]

        ping = one[6]
        main_win =  one[8]
        client_win = one[9]

        result = int(one[4])

        sizeAll += 1

        teamName = "佩斯卡拉"
        condition_1 = (main == teamName)
        condition_2 = (client == teamName)

        # if num == 37:
        #     print(1)

        if condition_1:
            if result == -1:
                rate_1 += client_win - 1
            else:
                rate_1 -= 1

            size += 1 
        elif  condition_2:
            if result == 1:
                rate_1 += main_win - 1
            else:
                rate_1 -= 1
            size += 1 
    if size == 0 :
        return

    print(name, num,  "做空：", round(rate_1, 2),  " size = ", size, " size all = ",sizeAll)


def getResult_3(name, rateMin, rateMax, num):
    db_name = "k_163_2017"

    data = sql.queryByTypeNum(name, db_name, str(num))
    if num == -1 :
        data = sql.queryByType(name, db_name)

    main_win = 0
    client_win = 0


    size = 0
    sizeAll = 0

    rate = {}


    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main = one[0]
        client = one[1]

        ping = one[6]
        main_win =  one[8]
        client_win = one[9]

        result = int(one[4])

        sizeAll += 1

        if not rate.__contains__(main):
            rate[main] = 0
        if not rate.__contains__(client):
            rate[client] = 0

        rateMain = rate[main]
        rateclient = rate[client]

        

        if Kong == 1:
            if result == 1:
                rateMain -= 1
                rateclient += main_win - 1
            elif result == -1:
                rateMain += client_win - 1
                rateclient -= 1
            else:
                rateMain -= 1
                rateclient -= 1
        else:
            if result == -1:
                rateMain -= 1
                rateclient += client_win - 1
            elif result == 1:
                rateMain += main_win - 1
                rateclient -= 1
            else:
                rateMain -= 1
                rateclient -= 1

        rate[main] = rateMain
        rate[client] = rateclient

    # sorted(rate.items(), key=lambda x:x[0], reverse=True)
    rate = sorted(rate.items(), key=lambda e:e[1], reverse=True)
    print(rate)
    print(sizeAll)
    # print(name, "做空：", rate)



def compare_1(name): 
    for i in range(17) :
        rateMin = i*0.1 + 1
        rateMax = rateMin + 0.1*1
        getResult_1(name, rateMin,  rateMax, -1)

def compare_2(name): 
    getResult_1(name, 2,  2.6, -1)

def compare_3(name): 
    for i in range(39) :
        getResult_1(name, 1,  2.4, i)

def compare_4(name):
    getResult_2(name, 1,  2.6, -1)

def compare_5(name):
    for i in range(39) :
        getResult_2(name, 1,  2.6, i)

def compare_6(name):
    getResult_3(name, 1,  2.6, -1)   

# compare_6("英超")
# compare_6("意甲")
# compare_6("西甲")
# compare_6("德甲")

# compare_6("英冠")
# compare_6("英甲")
# compare_6("巴甲")
# compare_6("J联赛")
# compare_2("欧洲冠军联赛")
# compare_4("英超")
