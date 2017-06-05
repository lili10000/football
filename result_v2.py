from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')

sizeMin = 20

def getResultAll():
    data = sql.queryByTypeAll("k_rate_euro")

    main_win = 0
    client_win = 0
    tie_win = 0
    if len(data) == 0 :
        return
    
    rate = 0
    rate = 3

    for one in data :
        if one[4] == 1 :
            main_win += one[6+rate] - 1
            client_win += -1
            tie_win += -1
        elif one[4] == -1 :
            main_win += - 1
            client_win += one[7+rate] -1
            tie_win += -1
        else :
            main_win += - 1
            client_win += -1
            tie_win += one[8+rate] -1

    mainResult = main_win/len(data)
    clientResult = client_win/len(data)
    tieResult = tie_win/len(data)
    gameSize = len(data)
    print(str(main_win/len(data)), "    ",str(client_win/len(data)),"    ",str(tie_win/len(data)),"    ",str(len(data)))

# getResultAll()

def getResult(name):
    main_win_count = sql.queryCount(name, "k_all", "1")
    tie_count = sql.queryCount(name, "k_all", "0")
    client_win_count = sql.queryCount(name, "k_all", "-1")
    
    total = main_win_count[0][0] + tie_count[0][0] + client_win_count[0][0]
    print(round(total / main_win_count[0][0],2), "    ",round(total / tie_count[0][0],2),"    ",round(total / client_win_count[0][0],2),"    ",name)

    main_win_rate_count = sql.queryCountRate(name, "k_all", "1")
    tie_rate_count = sql.queryCountRate(name, "k_all", "0")
    client_win_rate_count = sql.queryCountRate(name, "k_all", "-1")

    # print(round(total / main_win_rate_count[0][0],2), "    ",round(total / tie_rate_count[0][0],2),"    ",round(total / client_win_rate_count[0][0],2),"    ","让球",name)


def getResult_v2(name, value_max, value_min):
    data = sql.queryByType(name, "k_rate_euro")

    main_win = 0
    client_win = 0
    tie_win = 0
    size = 0

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        rate_win = one[6]
        rate_lost = one[7]
        rate_tie = one[8]

        if (rate_win > value_min and  rate_win < value_max):
            size += 1
            if one[4] == 1 :
                main_win += one[6] - 1
                client_win += -1
                tie_win += -1
            elif one[4] == -1 :
                main_win += - 1
                client_win += one[7] -1
                tie_win += -1
            elif one[4] == 0 :
                main_win += - 1
                client_win += -1
                tie_win += one[8] -1

    if size < sizeMin :
        return
    if main_win/size < 0.1 and client_win/size < 0.1 and tie_win/size < 0.1:
        return
    if main_win >0 or client_win >0 or tie_win >0 :
        print("[主",value_min,value_max , "]", "win",str(round(main_win/size, 2)), "   lost",str(round(client_win/size, 2)),"    tie",str(round(tie_win/size, 2)),"    ",str(size),"    ",name)
   

def getResult_v3(name, value_max, value_min):
    data = sql.queryByType(name, "k_rate_euro")

    main_win = 0
    client_win = 0
    tie_win = 0
    size = 0

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        rate_win = one[6]
        rate_lost = one[7]
        rate_tie = one[8]

        if (rate_lost > value_min and  rate_lost < value_max):
            size += 1
            if one[4] == 1 :
                main_win += one[6] - 1
                client_win += -1
                tie_win += -1
            elif one[4] == -1 :
                main_win += - 1
                client_win += one[7] -1
                tie_win += -1
            elif one[4] == 0 :
                main_win += - 1
                client_win += -1
                tie_win += one[8] -1

    if size < sizeMin :
        return
    if main_win/size < 0.1 and client_win/size < 0.1 and tie_win/size < 0.1:
        return
    if main_win >0 or client_win >0 or tie_win >0 :
        print("[客",value_min,value_max , "]", "win",str(round(main_win/size, 2)), "   lost",str(round(client_win/size, 2)),"    tie",str(round(tie_win/size, 2)),"    ",str(size),"    ",name)
    # print(str(round(main_win/size, 2)), "   ",str(round(client_win/size, 2)),"    ",str(round(tie_win/size, 2)),"    ",str(size),"    ",name)


def getResult_v4(name, value_max, value_min):
    data = sql.queryByType(name, "k_rate_euro")

    main_win = 0
    client_win = 0
    tie_win = 0
    size = 0

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        rate_win = one[6]
        rate_lost = one[7]
        rate_tie = one[8]

        if (tie_win > value_min and  tie_win < value_max):
            size += 1
            if one[4] == 1 :
                main_win += one[6] - 1
                client_win += -1
                tie_win += -1
            elif one[4] == -1 :
                main_win += - 1
                client_win += one[7] -1
                tie_win += -1
            elif one[4] == 0 :
                main_win += - 1
                client_win += -1
                tie_win += one[8] -1

    if size < sizeMin :
        return
    if main_win/size < 0.1 and client_win/size < 0.1 and tie_win/size < 0.1:
        return
    if main_win >0 or client_win >0 or tie_win >0 :
        print("[平",value_min,value_max , "]", "win",str(round(main_win/size, 2)), "   lost",str(round(client_win/size, 2)),"    tie",str(round(tie_win/size, 2)),"    ",str(size),"    ",name)
    # print(str(round(main_win/size, 2)), "   ",str(round(client_win/size, 2)),"    ",str(round(tie_win/size, 2)),"    ",str(size),"    ",name)



def compare(name): 
    # getResult_v2(name,1.6, 1.3) 
    # return

    weight = 0.2
    rangeMax = 12

    for i in range(0, rangeMax) :
        max = 1 + weight*(i+1) 
        min =  1 + weight*i
        min = round(min,2)
        max = round(max,2)
        getResult_v2(name,max, min) 
    getResult_v2(name,10, 3.5)

    for i in range(0, rangeMax) :
        max = 1 + weight*(i+1) 
        min =  1 + weight*i
        min = round(min,2)
        max = round(max,2)
        getResult_v3(name,max, min) 
    getResult_v3(name,10, 3.5)

    weight = 0.3
    for i in range(0, rangeMax) :
        max = 1 + weight*(i+1) 
        min =  1 + weight*i
        min = round(min,2)
        max = round(max,2)
        getResult_v4(name,max, min) 
    getResult_v4(name,10, 3.5)


# compare("美职业")
# compare("阿甲")
# compare("英超")
# compare("英甲")
# compare("英冠")
# compare("英乙")
# compare("意甲")
# compare("德甲")
# compare("德乙")
# compare("西甲")
# compare("葡超")
# compare("法甲")
# compare("法乙")
# compare("荷甲")
# compare("荷乙")
# compare("日职联")
# compare("日职乙")
# compare("苏超")
# compare("比甲")
# compare("俄超")
compare("挪超")
# compare("瑞典超")
# compare("巴西甲")
# compare("澳洲甲")
# compare("韩联")
