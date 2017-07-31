from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20


def getResult_2(name, score, corner):
    data = sql.queryByType(name, "k_corner")
    # data = sql.queryByTypeAll("k_corner")
    main_win = 0
    client_win = 0
    tie_win = 0

    corner_All = 0
    corner_total = [0, 0, 0, 0, 0, 0]

    score_all =0
    corner_6 = 0
    corner_6_8 = 0
    corner_9_11 = 0
    corner_12_14 = 0
    corner_14 = 0


    corner_else = 0
    score_esle = 0

    size = 0
    if len(data) == 0 :
        return
    for one in data :
        main_score = int(one[2])
        client_score = int(one[3])
        score_sum = main_score + client_score

        main_corner = int(one[6])
        client_corner = int(one[7])

        corner_Sum = int(one[8])
        rateDb = one[4]
        # if rateDb != rate :
        #     continue
        size += 1
        # corner_All += corner_Sum
        score_flag = score_sum < score
        corner_flag = corner_Sum > corner

        if score_flag:
            score_all += 1

        if corner_flag :
            corner_All += 1
            if score_flag:
                corner_6 += 1
            else:
                corner_else += 1

        # if corner_Sum >= 6 and corner_Sum <= 8 and score_sum <= score:
        #     corner_6_8 += 1 

        # if corner_Sum >= 9 and corner_Sum <= 11 and score_sum <= score:
        #     corner_9_11 += 1

        # if corner_Sum >= 12 and corner_Sum <= 14 and score_sum <= score:
        #     corner_12_14 += 1

        # if corner_Sum > 14 and score_sum <= score:
        #     corner_14 += 1


    print("[<",score, " >", corner,"]    ", round(corner_6/size, 2), "  size =",size)
    # print("score [",score,"]    ", round(corner_6/size, 2), "     ", round(corner_6_8/size, 2), "     ", round(corner_9_11/size, 2), "     ", round(corner_12_14/size, 2), "     ", round(corner_14/size, 2),  "  size =",size,name)


def getResult_3(name):
    data = sql.queryByType(name, "k_corner")

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
        # if rate_result > 0 :
        #     winScoreSum += scoreSum
        #     winSize +=1
        # elif rate_result < 0 :
        #     lostScoreSum += scoreSum
        #     lostSize += 1


    print(round(score_total[1]/size, 2), "     ", round(score_total[2]/size, 2), "     ", round(score_total[3]/size, 2), "     ", round(score_total[4]/size, 2), "  size =",size, "    all")
  

def compare(name): 
    # getResult_2(name, 2.5)
    # getResult_2(name, 1, 1.3, 0.01) 
    # return
    # min_win = 0.25
    # getResult_2(name, 0.5, 7.5)
    for i in range(4) :
        for j in range(6) :
            getResult_2(name, 0.5+i, 7.5+j)
    # getResult_3(name)
# compare("J联赛")
compare("韩k联")
# compare("日联杯")
# compare("美职联")
# compare("巴甲")
# compare("阿甲")
# compare("挪超")
# compare("瑞典超")
# compare("瑞典甲")
# compare("冰岛超")
# compare("k联赛")
# compare("英超")
# compare("英冠")
# compare("英甲")
# compare("意甲")
# compare("意乙")
# compare("德甲")
# compare("西甲")
# compare("法甲")
# compare("国际A级")
# compare("中甲")
# compare("苏联杯")