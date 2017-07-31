from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20


def getResult_1(name, key, key_max, min_win,):
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

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main_score = int(one[2])
        client_score = int(one[3])

        scoreSum = main_score+client_score
        rate_result = one[4]

        rate_win = float(one[8])
        rate_lost = float(one[9])
        rate_tie = one[6]
        if rate_win < key or  rate_win > key_max:
            continue
        
        scoreAll += scoreSum
        if scoreSum >= 5 :
            score_total[5] += 1 
        if scoreSum <= 0 :
            score_total[0] += 1 
        if scoreSum <= 1 :
            score_total[1] += 1
        if scoreSum <= 2 :
            score_total[2] += 1
        if scoreSum <= 3 :
            score_total[3] += 1
        if scoreSum <= 4 :
            score_total[4] += 1
        


        size += 1
        if rate_result > 0 :
            winScoreSum += scoreSum
            winSize +=1
        elif rate_result < 0 :
            lostScoreSum += scoreSum
            lostSize += 1

        if rate_result > 0 :
            main_win += rate_win - 1
            client_win += -1
            tie_win += -1
        elif rate_result < 0 :
            client_win += rate_lost - 1
            main_win += -1
            tie_win += -1
        else :
            tie_win += rate_tie - 1
            main_win += -1
            client_win += -1


    if  size < 1 :
    #     # print(key, winSize, lostSize)
        return
    # if main_win/size >min_win or client_win/size >min_win or tie_win/size >min_win :
        # print("主 key[",round(key, 2),round(key_max, 2), "]win",str(round(winScoreSum/winSize, 2))," win rate",round(winSize/size,3), "   lost",str(round(lostScoreSum/lostSize, 2)),"   lost rate",round(lostSize/size,3)," ",winSize,lostSize,"    ",name)
    # print("key[",round(key, 2),round(key_max, 2), "]win",str(round(main_win/size, 2)),"   lost",str(round(client_win/size, 2)),"    tie",str(round(tie_win/size, 2)),"    ",str(size), winSize, lostSize,"    ",name)
        
    print("key[",round(key, 2),round(key_max, 2), "]    ", round(score_total[1]/size, 2), "     ", round(score_total[2]/size, 2), "     ", round(score_total[3]/size, 2), "     ", round(score_total[4]/size, 2), "  size =",size, "    ",name)
    # j = 0
    # for i in score_total :
    #     print(j, round(i/size, 2))
    #     j += 1
def getResult_2(name, key, key_max, min_win,):
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

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main_score = int(one[2])
        client_score = int(one[3])

        scoreSum = main_score+client_score
        rate_result = one[4]

        rate_win = float(one[8])
        rate_lost = float(one[9])
        rate_tie = one[6]
        if rate_lost < key or  rate_lost > key_max:
            continue
        
        scoreAll += scoreSum
        if scoreSum >= 5 :
            score_total[5] += 1 
        if scoreSum <= 0 :
            score_total[0] += 1 
        if scoreSum <= 1 :
            score_total[1] += 1
        if scoreSum <= 2 :
            score_total[2] += 1
        if scoreSum <= 3 :
            score_total[3] += 1
        if scoreSum <= 4 :
            score_total[4] += 1
        


        size += 1
        if rate_result > 0 :
            winScoreSum += scoreSum
            winSize +=1
        elif rate_result < 0 :
            lostScoreSum += scoreSum
            lostSize += 1

        if rate_result > 0 :
            main_win += rate_win - 1
            client_win += -1
            tie_win += -1
        elif rate_result < 0 :
            client_win += rate_lost - 1
            main_win += -1
            tie_win += -1
        else :
            tie_win += rate_tie - 1
            main_win += -1
            client_win += -1


    if size < 1 :
        # print(key, winSize, lostSize)
        return
    # if main_win/size >min_win or client_win/size >min_win or tie_win/size >min_win :
        # print("主 key[",round(key, 2),round(key_max, 2), "]win",str(round(winScoreSum/winSize, 2))," win rate",round(winSize/size,3), "   lost",str(round(lostScoreSum/lostSize, 2)),"   lost rate",round(lostSize/size,3)," ",winSize,lostSize,"    ",name)
    # print("key[",round(key, 2),round(key_max, 2), "]win",str(round(main_win/size, 2)),"   lost",str(round(client_win/size, 2)),"    tie",str(round(tie_win/size, 2)),"    ",str(size), winSize, lostSize,"    ",name)
        
    print("客 key[",round(key, 2),round(key_max, 2), "]    ", round(score_total[1]/size, 2), "     ", round(score_total[2]/size, 2), "     ", round(score_total[3]/size, 2), "     ", round(score_total[4]/size, 2), "  size =",size, "    ",name)
    # j = 0
    # for i in score_total :
    #     print(j, round(i/size, 2))
    #     j += 1


def getResult_3(name, key, key_max, min_win,):
    # data = sql.queryByTypeAll("k_163")
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
    score_1 = 0
    score_2 = 0
    score_total =[0, 0, 0, 0, 0, 0]

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main_score = int(one[2])
        client_score = int(one[3])

        scoreSum = main_score+client_score
        rate_result = one[4]

        rate_win = float(one[8])
        rate_lost = float(one[9])
        rate_tie = one[6]
        if rate_win < key or  rate_win > key_max:
            continue
        
        scoreAll += scoreSum
        if scoreSum % 2 == 1 :
            score_1 += 1 
        if scoreSum % 2 == 0 :
            score_2 += 1 

        size += 1
        
    if size == 0 :
        return
    print("key[",round(key, 2),round(key_max, 2), "]    单", round(score_1/size, 2), "     双", round(score_2/size, 2), "  size =",size, "    ", name)
  

def getResult_4( key, key_max, min_win,):
    data = sql.queryByTypeAll( "k_163")

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

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main_score = int(one[2])
        client_score = int(one[3])

        scoreSum = main_score+client_score
        rate_result = one[4]

        rate_win = float(one[8])
        rate_lost = float(one[9])
        rate_tie = one[6]
        if rate_lost < key or  rate_lost > key_max:
            continue
        
        scoreAll += scoreSum
        if scoreSum >= 5 :
            score_total[5] += 1 
        if scoreSum <= 0 :
            score_total[0] += 1 
        if scoreSum <= 1 :
            score_total[1] += 1
        if scoreSum <= 2 :
            score_total[2] += 1
        if scoreSum <= 3 :
            score_total[3] += 1
        if scoreSum <= 4 :
            score_total[4] += 1
        


        size += 1
        if rate_result > 0 :
            winScoreSum += scoreSum
            winSize +=1
        elif rate_result < 0 :
            lostScoreSum += scoreSum
            lostSize += 1

        if rate_result > 0 :
            main_win += rate_win - 1
            client_win += -1
            tie_win += -1
        elif rate_result < 0 :
            client_win += rate_lost - 1
            main_win += -1
            tie_win += -1
        else :
            tie_win += rate_tie - 1
            main_win += -1
            client_win += -1


    print("客 key[",round(key, 2),round(key_max, 2), "]    ", round(score_total[1]/size, 2), "     ", round(score_total[2]/size, 2), "     ", round(score_total[3]/size, 2), "     ", round(score_total[4]/size, 2), "  size =",size, "    all")


def compare(name): 
    # getResult_2(name, 1, 1.3, 0.01) 
    # return
    min_win = 0.01
    for index in range(10) :
        # print("start", 1 + 0.3*index)
        key = 1 + 0.3*index
        key_max = 1 + 0.3*(index+1)
    #     getResult_1(name, key,key_max, min_win) 
    # getResult_1(name, 4,100, min_win)
    # getResult_1(name, 1,1.1, min_win)
    # getResult_1(name, 1.1,1.2, min_win)
        getResult_2(name, key,key_max, min_win) 
    getResult_2(name, 4,100, min_win)
    getResult_2(name, 1,1.1, min_win)
    getResult_2(name, 1.1,1.2, min_win)

    #     getResult_3(name, key,key_max, min_win) 
    # getResult_3(name, 4,100, min_win)
    # getResult_3(name, 1,1.1, min_win)
    # getResult_3(name, 1.1,1.2, min_win)

def compare_1(): 
    # getResult_2(name, 1, 1.3, 0.01) 
    # return
    min_win = 0.01
    for index in range(10) :
        # print("start", 1 + 0.3*index)
        key = 1 + 0.3*index
        key_max = 1 + 0.3*(index+1)
        # getResult_1(name, key,key_max, min_win) 
        getResult_3(key,key_max, min_win) 
    getResult_3(1,1.1, min_win)
    getResult_3(1.1,1.2, min_win)
    getResult_3(4,100, min_win)

def compare_2(): 
    # getResult_2(name, 1, 1.3, 0.01) 
    # return
    min_win = 0.01
    for index in range(10) :
        # print("start", 1 + 0.3*index)
        key = 1 + 0.3*index
        key_max = 1 + 0.3*(index+1)
        # getResult_1(name, key,key_max, min_win) 
        getResult_4(key,key_max, min_win) 
    getResult_4(1,1.1, min_win)
    getResult_4(1.1,1.2, min_win)
    getResult_4(4,100, min_win)

# compare("J联赛")
# compare("J2联赛")
# compare("日联杯")
# compare("美职联")
compare("德乙")
