from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20
check_rate = 0.05
name = "自由杯"

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

    test = 0
    reTest = 0
    test_ping = 0
    re_test_ping = 0
    size = 0

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
        if abs(start_rate - end_rate) <= rate:
            continue

        # if (end_rate - start_rate) > check_rate and main_score < client_score:
        #     test += end_lost_rate -1
        # elif (start_rate - end_rate) > check_rate and main_score > client_score:
        #     test += end_win_rate -1
        # else:
        #     test -= 1

        # if not(main_score == client_score):
        #     tmp = getRate(end_ping_rate)
        #     test += tmp -1
        # else:
        #     test -= 1

        if (start_rate - end_rate) > rate and main_score < client_score:
            test += end_lost_rate -1
            reTest -= 1
        elif (start_rate - end_rate) > rate and main_score > client_score:
            reTest += end_win_rate -1
            test -= 1
        elif (end_rate - start_rate) > rate and main_score > client_score:
            test += end_win_rate -1
            reTest -= 1
        elif (end_rate - start_rate) > rate and main_score < client_score:
            reTest += end_lost_rate -1
            test -= 1
        else:
            test -= 1
            reTest -= 1


        size += 1

    if size == 0:
        return 
    print(rate, " ",name, "   买降水 = ",round( test/size, 4), "    买升水 = ",round( reTest/size, 4) ,"    size =", size)
    
    # print("start:   ",round( start_rate_win, 2),"   ",round(start_rate_ping, 2),"   ",round(start_rate_lost, 2) )
    # print("end:   ",round( end_rate_win, 2),"   ",round(end_rate_ping, 2),"   ",round(end_rate_lost, 2) )


# getResult(None, 0.12)
for i in range(20):
    rate = 0.01*i
    # getResult(None, rate)
    # getResult("英超", rate)
    # getResult("西甲", rate)
    # getResult("意甲", rate)
    # getResult("德甲", rate)
    # getResult("法甲", rate)
    getResult(name, rate)