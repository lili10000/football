from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20

def getResult_1(name):
    data = sql.queryByType(name, "k_rate_euro")

    main_win = 0
    client_win = 0
    tie_win = 0
    size = 0

    flag_win = False
    flag_lost = False
    changeCount = 0

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

        factor = 1/(1/rate_win + 1/rate_lost +  1/rate_tie)
        factor_first = 1/(1/rate_win_first + 1/rate_lost_first +  1/rate_tie_first)

        rate_win = (1/rate_win)*factor
        rate_lost = (1/rate_lost)*factor
        rate_win_first = (1/rate_win_first)*factor_first
        rate_lost_first = (1/rate_lost_first)*factor_first

        rate = 0
        # if rate_lost > rate_lost_first :
        if rate_win > rate_win_first :
            size += 1
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

        if (main_win > 0 and flag_win == False)  :
            changeCount += 1
            flag_win = True
        elif (main_win < 0 and flag_win == True) :
            changeCount += 1
            flag_win = False
    if size == 0 :
        return
    # if main_win >0 or client_win >0 or tie_win >0 :
    print("[主胜率升]", "win",str(round(main_win/size, 2)), "   lost",str(round(client_win/size, 2)),"    tie",str(round(tie_win/size, 2)),"    ",str(size),"    ",name, "changeCount=", changeCount)
  
def getResult_2(name):
    data = sql.queryByType(name, "k_rate_euro")

    main_win = 0
    client_win = 0
    tie_win = 0
    size = 0

    flag_win = False
    flag_lost = False
    changeCount = 0

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

        factor = 1/(1/rate_win + 1/rate_lost +  1/rate_tie)
        factor_first = 1/(1/rate_win_first + 1/rate_lost_first +  1/rate_tie_first)

        rate_win = (1/rate_win)*factor
        rate_lost = (1/rate_lost)*factor
        rate_win_first = (1/rate_win_first)*factor_first
        rate_lost_first = (1/rate_lost_first)*factor_first

        rate = 0
        # if rate_lost > rate_lost_first :
        if rate_win < rate_win_first :
            size += 1
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

        if (main_win > 0 and flag_win == False)  :
            changeCount += 1
            flag_win = True
        elif (main_win < 0 and flag_win == True) :
            changeCount += 1
            flag_win = False
    if size == 0 :
        return
    # if main_win >0 or client_win >0 or tie_win >0 :
    print("[主胜率降]", "win",str(round(main_win/size, 2)), "   lost",str(round(client_win/size, 2)),"    tie",str(round(tie_win/size, 2)),"    ",str(size),"    ",name, "changeCount=", changeCount)


def getResult_3(name):
    data = sql.queryByType(name, "k_rate_euro")

    main_win = 0
    client_win = 0
    tie_win = 0
    size = 0

    flag_win = False
    flag_lost = False
    changeCount = 0

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

        factor = 1/(1/rate_win + 1/rate_lost +  1/rate_tie)
        factor_first = 1/(1/rate_win_first + 1/rate_lost_first +  1/rate_tie_first)

        rate_win = (1/rate_win)*factor
        rate_lost = (1/rate_lost)*factor
        rate_win_first = (1/rate_win_first)*factor_first
        rate_lost_first = (1/rate_lost_first)*factor_first


        rate = 0
        if rate_lost > rate_lost_first :
        # if rate_win > rate_win_first :
            size += 1
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

        if (main_win > 0 and flag_win == False)  :
            changeCount += 1
            flag_win = True
        elif (main_win < 0 and flag_win == True) :
            changeCount += 1
            flag_win = False
    if size == 0 :
        return
    # if main_win >0 or client_win >0 or tie_win >0 :
    print("[客胜率升]", "win",str(round(main_win/size, 2)), "   lost",str(round(client_win/size, 2)),"    tie",str(round(tie_win/size, 2)),"    ",str(size),"    ",name, "changeCount=", changeCount)
  
def getResult_4(name):
    data = sql.queryByType(name, "k_rate_euro")

    main_win = 0
    client_win = 0
    tie_win = 0
    size = 0

    flag_win = False
    flag_lost = False
    changeCount = 0

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

        factor = 1/(1/rate_win + 1/rate_lost +  1/rate_tie)
        factor_first = 1/(1/rate_win_first + 1/rate_lost_first +  1/rate_tie_first)

        rate_win = (1/rate_win)*factor
        rate_lost = (1/rate_lost)*factor
        rate_win_first = (1/rate_win_first)*factor_first
        rate_lost_first = (1/rate_lost_first)*factor_first


        rate = 0
        if rate_lost < rate_lost_first :
        # if rate_win < rate_win_first :
            size += 1
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

        if (main_win > 0 and flag_win == False)  :
            changeCount += 1
            flag_win = True
        elif (main_win < 0 and flag_win == True) :
            changeCount += 1
            flag_win = False
    if size == 0 :
        return
    # if main_win >0 or client_win >0 or tie_win >0 :
    print("[客胜率降]", "win",str(round(main_win/size, 2)), "   lost",str(round(client_win/size, 2)),"    tie",str(round(tie_win/size, 2)),"    ",str(size),"    ",name, "changeCount=", changeCount)

def compare(name): 
    getResult_1(name) 
    getResult_2(name) 
    getResult_3(name) 
    getResult_4(name) 
    # return

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
# compare("挪超")
# compare("瑞典超")
# compare("巴西甲")
# compare("澳洲甲")
# compare("韩联")