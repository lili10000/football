from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')


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

def getResult(name, value):
    data = sql.queryByType(name, "k_rate_euro")

    main_win = 0
    client_win = 0
    tie_win = 0
    if len(data) == 0 :
        return
        
    rate = 0
    # rate = 3

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
    if (mainResult > value or clientResult > value or tieResult > value)  and gameSize > 30:
        # print("")
        print(str(main_win/len(data)), "    ",str(client_win/len(data)),"    ",str(tie_win/len(data)),"    ",str(len(data)),"    ",name)
        return True
    return False


def getResult_v2(name, value):
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
        rate_win_first = one[6+ offset]
        rate_lost = one[7]
        rate_lost_first = one[7+ offset]
        rate_tie = one[8]
        rate_tie_first = one[8+ offset]

        if rate_win_first == 0 or rate_lost_first == 0 :
            return
        change_min = abs(rate_win_first - rate_win)/rate_win_first
        change = abs(rate_lost_first - rate_lost)/rate_lost_first
        if change_min > change :
            change_min = change

        if change_min < value :
            continue
        size += 1
        if one[4] == 1 :
            main_win += one[6] - 1
            client_win += -1
            tie_win += -1
        elif one[4] == -1 :
            main_win += - 1
            client_win += one[7] -1
            tie_win += -1
        else :
            main_win += - 1
            client_win += -1
            tie_win += one[8] -1

    if size < 30 :
        return
    if main_win/size < 0.1 and client_win/size < 0.1 and tie_win/size < 0.1:
        return
    if main_win >0 or client_win >0 or tie_win >0 :
        print(str(round(main_win/size, 2)), "   ",str(round(client_win/size, 2)),"    ",str(round(tie_win/size, 2)),"    ",str(size),"    ",name, value)


# def compare(name):
    
#     if getResult(name, 0.03) == False :
#         return
    # getResult_v2(name, 0.15)
   
def compare(name):
    getResult_v2(name, 0.1)
#     for index in range(20):
        # getResult_v2(name, 0.01*index)

compare("美职业")
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
# compare("挪超")
# compare("瑞典超")
# compare("巴西甲")
# compare("澳洲甲")
