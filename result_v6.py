from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20

def getRate(rate):
    # reduce = 1.05
    # return 1/(reduce*(1-1/(rate*reduce))) 
    if rate == 0:
        return 0
    return rate
    return round(1/rate, 2)

def getResult_3(name, score):
    data = []
    if name == None:
        data = sql.queryByTypeAll("k_corner")
    else:
        data = sql.queryByType(name, "k_corner")

    size_big = 0
    size_small = 0
    
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


        def tmpFun(score_corner_map):
            score_check = 2.5
            corner_check = 8.5
            key = ""
            # if scoreSum > score_check and  corner_Sum > corner_check:
            #     key="大球大角"
            # if scoreSum > score_check and  corner_Sum < corner_check:
            #     key="大球小角"
            # if scoreSum < score_check and  corner_Sum > corner_check:
            #     key="小球大角"
            # if scoreSum < score_check and  corner_Sum < corner_check:
            #     key="小球小角"
            # if not(score_corner_map.__contains__(key)):
            #     score_corner_map[key] = 0
            # score_corner_map[key] += 1

            # result = main_score - client_score + float(rateDb)

            # if result > 0 and  corner_Sum > corner_check:
            #     key="主胜 大球"
            # elif result > 0 and  corner_Sum < corner_check:
            #     key="主胜 小球"
            # elif result <= 0 and corner_Sum > corner_check:
            #     key="主败 大球"
            # elif result <= 0 and  corner_Sum < corner_check:
            #     key="主败 小球"
            rateTmp = float(rateDb)
            result = main_score - client_score + rateTmp
            tmp = (rateTmp < 0 and result > 0) or (rateTmp > 0 and  result <= 0) or (rateTmp == 0)
            if False:
                key = ""
            elif tmp and  corner_Sum > corner_check:
                key="让球赢，大角"
            # elif not tmp and  corner_Sum < corner_check:
            #     key="让球输，小角"
            # elif scoreSum < score_check and corner_Sum < corner_check:
            #     key="小球，小角"          
            elif (rateTmp < 0 and client_score > 0) or (rateTmp > 0 and main_score > 0) and  corner_Sum < corner_check:
                key="劣势进球， 小角"
            # elif (rateTmp < 0 and client_score > 0) or (rateTmp > 0 and main_score > 0) and  corner_Sum > corner_check:
            #     key="劣势进球， 大角"
            else:
                key="极端情况"


            if not(score_corner_map.__contains__(key)):
                score_corner_map[key] = 0
            score_corner_map[key] += 1

                
        
        if small:
            tmpFun(score_corner_map_small)
            size_small += 1
        else:
            tmpFun(score_corner_map_big)
            size_big += 1


    print("rate < 0.5")
    size = size_small
    if size == 0:
        return
    for key in score_corner_map_small:
        print(key," ", getRate(round(score_corner_map_small[key]/size, 2)))

    print("rate > 0.5")
    size = size_big 
    if size == 0:
        return
    for key in score_corner_map_big:
        print(key," ", getRate(round(score_corner_map_big[key]/size, 2)))


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

compare("俄罗斯")
# compare("中超")
# compare("德国乙级")
# compare("法国乙级")
# compare("英超")
# compare("德甲")
# compare("西甲")
# compare("意甲")
# compare("法甲")