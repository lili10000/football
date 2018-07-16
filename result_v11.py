from db.mysql import sqlMgr
from ouToAsia import ouToAsia

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20
check_rate = 0.03
name = None
# name = "国际友谊"



# def getRate(rate):
#     if rate == 0:
#         return 0
#     return round(1/rate, 2)




def getResult(name, rate):
    data = []
    if name == None:
        data = sql.queryByTypeAll("k_rate")
    else:
        data = sql.queryByType(name, "k_rate")

    if len(data) == 0 :
        return

    conver = ouToAsia()




    for i in range(10):
        check_rate = 1.5 + i*0.1
        start_rate_win = 0
        start_rate_ping = 0
        start_rate_lost = 0

        end_rate_win = 0
        end_rate_ping = 0
        end_rate_lost = 0

        test = 0
        reTest = 0
        result = {}

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
            # if abs(start_rate - end_rate) <= rate or (abs(start_rate - end_rate) > rate + 0.01):
            #     continue
            # if abs(start_rate - end_rate) <= rate:
            #     continue

            # if (end_rate - start_rate) > rate or start_lost_rate > 3.6 or start_lost_rate < 2 :
            #     continue

            checkCondition_1 = (main_score + client_score)%2
            # checkCondition_2 = (main_score + client_score)%2
            if end_win_rate > end_lost_rate:
                tmp = end_win_rate
                end_win_rate = end_lost_rate
                end_lost_rate = tmp

                tmp = main_score
                main_score = client_score
                client_score = tmp

            
            if (end_win_rate < check_rate):
                    continue

            if conver.getWinResult(end_win_rate, main_score, client_score) == 1 and (checkCondition_1 == 1) :
                key = "强奇胜"
                if result.__contains__(key) == False:
                    result[key] = 0
                result[key] += 1
            elif conver.getWinResult(end_win_rate, main_score, client_score) == 1 and (checkCondition_1 == 0) :
                key = "强偶胜"
                if result.__contains__(key) == False:
                    result[key] = 0
                result[key] += 1
            elif conver.getWinResult(end_win_rate, main_score, client_score) == -1 and (checkCondition_1 == 1) :
                key = "强奇败"
                if result.__contains__(key) == False:
                    result[key] = 0
                result[key] += 1

            elif conver.getWinResult(end_win_rate, main_score, client_score) == -1 and (checkCondition_1 == 0) :
                key = "强偶败"
                if result.__contains__(key) == False:
                    result[key] = 0
                result[key] += 1

            elif conver.getWinResult(end_win_rate, main_score, client_score) == 0 and (checkCondition_1 == 0) :
                key = "偶平"
                if result.__contains__(key) == False:
                    result[key] = 0
                result[key] += 1

    
            else:
                test -= 1
                # reTest -= 1

            size += 1

        if size == 0:
            return 

        print("check_rate = ",check_rate)
        for tmp in result:
            print(check_rate, " key = ",tmp ,"    rate = ",round(result[tmp]/size, 2),"    size =", size)
        print("")


getResult(name, check_rate)
