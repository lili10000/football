from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20
check_rate = 0.05
name = "国际友谊"

# def getRate(rate):
#     if rate == 0:
#         return 0
#     return round(1/rate, 2)
def getRate(rate):
    reduce = 1.05
    return 1/(reduce*(1-1/(rate*reduce))) 

def getResult(name, rate):
    data = []
    if name == None:
        data = sql.queryByTypeAll("k_rate")
    else:
        data = sql.queryByType(name, "k_rate")

    # print(name,",    size = ", len(data))
    if len(data) == 0 :
        return

    start_rate_win = 0
    start_rate_ping = 0
    start_rate_lost = 0

    end_rate_win = 0
    end_rate_ping = 0
    end_rate_lost = 0

 
    distribute = {}
    re_distribute = {}
    distribute_all = {}
    size = 0
    elseSize = 0

    size_sum = len(data)
    print("data size = ", size_sum)
    for one in data :
        main_score = int(one[3])
        client_score = int(one[4])
        scoreSum = main_score + client_score

        start_win_rate = float(one[6])
        start_ping_rate = float(one[7])
        start_lost_rate = float(one[8])

        end_win_rate = float(one[9])
        end_ping_rate = float(one[10])
        end_lost_rate = float(one[11])

        start_rate = 1/start_win_rate
        end_rate = 1/end_win_rate

        # start_client_rate = 1/start_lost_rate
        # end_client_rate = 1/end_lost_rate

        # if abs(start_rate - end_rate) <= rate or (abs(start_rate - end_rate) > rate + 0.01):
        #     continue
        if abs(start_rate - end_rate) <= rate:
            continue

        # if (start_rate - end_rate) > rate and main_score > client_score:
        #     index = int(start_win_rate/0.2)
        #     if distribute.__contains__(index) == False:
        #         distribute[index] = 0
        #     distribute[index] += 1 
        
        # elif (start_client_rate - end_client_rate) > rate and main_score < client_score:
        #     index = int(start_lost_rate/0.1)
        #     if re_distribute.__contains__(index) == False:
        #         re_distribute[index] = 0
        #     re_distribute[index] += 1 
        # else:
        if (end_rate - start_rate) > rate:
            index = int(start_win_rate/0.2)
            if distribute_all.__contains__(index) == False:
                distribute_all[index] = 0
            distribute_all[index] += 1

        if (start_rate - end_rate) > rate and main_score < client_score:
            index = int(start_lost_rate/0.2)
            if re_distribute.__contains__(index) == False:
                re_distribute[index] = 0
            re_distribute[index] += 1 

        elif (end_rate - start_rate) > rate and main_score > client_score:
            index = int(start_win_rate/0.2)
            if distribute.__contains__(index) == False:
                distribute[index] = 0
            distribute[index] += 1 

        else:
            elseSize += 1

        size += 1

    if size == 0:
        return 


    print("降水总数:",size, " 比例:", round( size/size_sum, 2), " 降水输比率", round( elseSize/size, 2))
    
    # key_list = sorted(distribute_all.keys())
    # for key in key_list:
    #     print("客降水分布 key:",round(key*0.2,2),"num:",round( distribute_all[key]/size, 3) )
    
    # key_list = sorted(distribute.keys())
    # for key in key_list:
    #     print("买主降水 key:",round(key*0.2,2),"num:",round( distribute[key]/size, 3) )

    key_list = sorted(distribute.keys())
    for key in key_list:
        ev = round((distribute[key]/distribute_all[key])*key*0.2 - 1, 2)
        print("买主降水 key:",round(key*0.2,2),"主降胜率:",round(distribute[key]/distribute_all[key], 3), " 主降数：", distribute[key], "   EV:",ev)


getResult(None, 0.05)
