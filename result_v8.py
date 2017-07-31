from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20


def getResult_1(name, key_max, min_win):
    data = sql.queryByType(name, "k_163")

    main_win = 0
    client_win = 0
    tie_win = 0

    winScoreSum = 0
    lostScoreSum = 0

    winSize = 0
    lostSize = 0 

    size = 0

    scoreAll = 0
    score_total =[0, 0, 0, 0, 0, 0]

    result_win_big = 0
    result_win_big_size = 0
    result_win_small = 0
    result_win_small_size = 0
    result_lost_big = 0
    result_lost_big_size = 0
    result_lost_small = 0
    result_lost_small_size = 0

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main_score = int(one[2])
        client_score = int(one[3])

        scoreSum = main_score+client_score
        result = one[4]

        rate_win = float(one[8])
        rate_lost = float(one[9])
        rate_tie = one[6]
        if rate_win < min_win or  rate_win > key_max:
            continue
        size += 1
        scoreAll += scoreSum
        if scoreSum > 2.5 :
            if result == -1 :
                result_lost_big_size += 1
                result_win_big -= 1
                result_win_small -= 1
                result_lost_big += (rate_win - 1 )
                result_lost_small -= 1
            elif result == 1 :
                result_win_big_size += 1
                result_win_big += (rate_win - 1 )
                result_win_small -= 1
                result_lost_big -= 1
                result_lost_small -= 1
            else :
                result_win_big -= 1
                result_win_small -= 1
                result_lost_big -= 1
                result_lost_small -= 1
        else :
            if result == -1 :
                result_lost_small_size += 1
                result_win_big -= 1
                result_win_small -= 1
                result_lost_big -= 1
                result_lost_small += (rate_win - 1 )
            elif result == 1 :
                result_win_small_size += 1
                result_win_big -= 1
                result_win_small += (rate_win - 1 )
                result_lost_big -= 1
                result_lost_small -= 1
            else :
                result_win_big -= 1
                result_win_small -= 1
                result_lost_big -= 1
                result_lost_small -= 1
    if  size < 1 :
        return
    print("key[",round(min_win, 2),round(key_max, 2), "概率]    ",round(result_win_big_size/size, 2), "     ",round(result_lost_big_size/size, 2), "     ",round(result_win_small_size/size, 2), "     ", round(result_lost_small_size/size, 2), "  size =",size, "    ",name)
    # print("key[",round(min_win, 2),round(key_max, 2), "胜率]    ", round(result_win_big,2), "     ",round(result_lost_big, 2), "     ",round(result_win_small,2), "     ",round(result_lost_small,2), "  size =",size, "    ",name)


def compare_1(name): 
    # getResult_1(name, 1, 1.3, 0.01) 
    # return
    min_win = 0.01
    for index in range(10) :
        # print("start", 1 + 0.3*index)
        key_min = 1 + 0.3*index
        key_max = 1 + 0.3*(index+1)
        getResult_1(name, key_max, key_min) 

compare_1("德乙")
