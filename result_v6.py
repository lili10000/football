from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20
score_check = 2.5
corner_check = 9.5

# name = ["意大利甲级", "英格兰超级", "西班牙甲级", "德国甲级","法国甲级"]
name = ["英格兰冠军"]
# name=["法国甲级"]
# name = "英格兰超级"
# name = "西班牙甲级"
# name = "德国甲级"
# name = "法国甲级"
# name = "荷兰乙级"
# name = "亚足联冠军联赛"


def getRate(rate):
    # reduce = 1.05
    # return 1/(reduce*(1-1/(rate*reduce))) 
    if rate == 0:
        return 0
    # return rate
    return round(1/rate, 2)

def getResult_3(name, score):
    data = []
    if name == None:
        data = sql.queryByTypeAll("k_corner")
    else:
        data = sql.queryByType(name, "k_corner")

    size_big = 0
    size_small = 0

    size_low_corner = 0
    size_high_corner = 0
    
    score_corner_map_small={}
    score_corner_map_big={}
    
    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main_score = int(one[2])
        client_score = int(one[3])
        scoreSum = main_score + client_score

        rateDb = one[4]
        
        small = (float(rateDb) > -0.5 and float(rateDb) < 0.5)
        big = not(small) 

        main_corner = int(one[6])
        client_corner = int(one[7])

        corner_Sum = int(one[8])

        is_score = (main_score > 0) and (client_score > 0)


        # if float(rateDb) >= -1 and float(rateDb) <= 1:
        #     continue

        # if float(rateDb) < -1 or float(rateDb) > 1:
        #     continue

        if float(rateDb) <= 0 :
            continue

        def tmpFun(score_corner_map):
           
            rateTmp = float(rateDb)
            result = main_score - client_score + rateTmp
            tmp = (rateTmp < 0 and result > 0) or (rateTmp > 0 and  result <= 0) or (rateTmp == 0)

            key = ""
            if False:
                key = ""
            elif is_score and scoreSum > score_check and corner_Sum > corner_check:
                key="都进球 大球 大角"
            elif not is_score and scoreSum < score_check:
                key="非都进球 小球"
            else:
                key="极端情况"

        

            if not(score_corner_map.__contains__(key)):
                score_corner_map[key] = 0
            score_corner_map[key] += 1


            # if is_score and scoreSum > score_check and corner_Sum > corner_check:
            #     key="都进球 大球 大角"
            # elif is_score and scoreSum > score_check and corner_Sum < corner_check:
            #     key="都进球 大球 小角"
            # else:
            #     return
            # if not(score_corner_map.__contains__(key)):
            #     score_corner_map[key] = 0
            # score_corner_map[key] += 1

        if small:
            tmpFun(score_corner_map_small)
            size_small += 1
        else:
            tmpFun(score_corner_map_big)
            size_big += 1

        if corner_Sum < corner_check :
            size_low_corner += 1
        else:
            size_high_corner += 1
    
    size = size_small
    if size != 0:
        print("rate < 0.5   size=",size)
        for key in score_corner_map_small:
            print(key," ", getRate(round(score_corner_map_small[key]/size, 2)))

    
    size = size_big 
    if size != 0:
        print("rate > 0.5   size=",size)
        for key in score_corner_map_big:
            print(key," ", getRate(round(score_corner_map_big[key]/size, 2)))

    print("大角 : 小角 = ", round( size_high_corner/size_low_corner, 3))

def compare(name): 
    # getResult_2(name, 2.5)
    # getResult_2(name, 1, 1.3, 0.01) 
    # return
    # min_win = 0.25
    # getResult_2(name, 0.5, 7.5)
    print("\n"+name)
    getResult_3(name, 1)
    # for i in range(4) :
    #     getResult_3(name, i)
    #     for j in range(6) :
    #         getResult_2(name, 0.5+i, 7.5+j)
    # getResult_3(name, )

# compare("俄罗斯")
# compare("中超")

for i in name :
    compare(i)
# compare("法国乙级")
# compare("英超")
# compare("德甲")
# compare("西甲")
# compare("意甲")
# compare("法甲")