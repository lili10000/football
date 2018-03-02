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

def getRate(rate):
    # reduce = 1.05
    # return 1/(reduce*(1-1/(rate*reduce))) 
    if rate == 0:
        return 0
    return round(1/rate, 2)

def getResult_3(name, score):
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
    corner_total =[0, 0, 0, 0, 0, 0, 0, 0, 0]  # <6, 6, 7, 8,9, 10, 11, 12, >12

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main_score = int(one[2])
        client_score = int(one[3])

        rateDb = one[4]
        if (float(rateDb) > -0.5 and float(rateDb) < 0.5):
            continue

        main_corner = int(one[6])
        client_corner = int(one[7])

        corner_Sum = int(one[8])
        
        index = corner_Sum - 5
        if index > 8:
            index = 8

        if index <= 0:
            index = 0

        corner_total[index] += 1

        size += 1
        # if rate_result > 0 :
        #     winScoreSum += scoreSum
        #     winSize +=1
        # elif rate_result < 0 :
        #     lostScoreSum += scoreSum
        #     lostSize += 1
    if size == 0:
        return

    print(name,"score:",score, " size:",size)
    index = 0
    rate = 0
    rate += round(corner_total[index]/size, 2)
    print("<6   ", round(corner_total[index]/size, 2), "    <=",getRate(rate), "    >", getRate(1-rate))
    index +=1
    rate += round(corner_total[index]/size, 2)
    print("6    ", round(corner_total[index]/size, 2), "    <=",getRate(rate), "    >", getRate(1-rate))
    index +=1
    rate += round(corner_total[index]/size, 2)
    print("7    ", round(corner_total[index]/size, 2), "    <=",getRate(rate), "    >", getRate(1-rate))
    index +=1
    rate += round(corner_total[index]/size, 2)
    print("8    ", round(corner_total[index]/size, 2), "    <=",getRate(rate), "    >", getRate(1-rate))
    index +=1
    rate += round(corner_total[index]/size, 2)
    print("9    ", round(corner_total[index]/size, 2), "    <=",getRate(rate), "    >", getRate(1-rate))
    index +=1
    rate += round(corner_total[index]/size, 2)
    print("10   ", round(corner_total[index]/size, 2), "    <=",getRate(rate), "    >", getRate(1-rate))
    index +=1
    rate += round(corner_total[index]/size, 2)
    print("11   ", round(corner_total[index]/size, 2), "    <=",getRate(rate), "    >", getRate(1-rate))
    index +=1
    rate += round(corner_total[index]/size, 2)
    print("12   ", round(corner_total[index]/size, 2), "    <=",getRate(rate), "    >", getRate(1-rate))
    index +=1
    rate += round(corner_total[index]/size, 2)
    print(">12  ", round(corner_total[index]/size, 2), "    <=",getRate(rate), "    >", getRate(1-rate))


def compare(name): 
    # getResult_2(name, 2.5)
    # getResult_2(name, 1, 1.3, 0.01) 
    # return
    # min_win = 0.25
    # getResult_2(name, 0.5, 7.5)
    getResult_3(name, 1)
    # for i in range(4) :
    #     getResult_3(name, i)
    #     for j in range(6) :
    #         getResult_2(name, 0.5+i, 7.5+j)
    # getResult_3(name, )
# compare("J联赛")
# compare("韩k联")
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
compare("意甲")
# compare("意乙")
# compare("德甲")
# compare("西甲")
# compare("法甲")
# compare("国际A级")
# compare("中甲")
# compare("苏联杯")