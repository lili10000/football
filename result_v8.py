from db.mysql import sqlMgr
from db.htmlParser import parser

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20

Kong = 1

def getResult_1(name, rateMin, rateMax, num):
    db_name = "k_163_2017"

    data = sql.queryByTypeNum(name, db_name, str(num))
    if num == -1 :
        data = sql.queryByType(name, db_name)

    main_win = 0
    client_win = 0
    tie_win = 0

    winScoreSum = 0
    lostScoreSum = 0

    winSize = 0
    lostSize = 0 

    size = 0
    sizeAll = 0

    scoreAll = 0
    score_total =[0, 0, 0, 0, 0, 0]

    rate_1 = 0
    rate_2 = 0
    rate_3 = 0

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main = one[0]
        client = one[1]

        ping = one[6]
        main_win =  one[8]
        client_win = one[9]

        result = int(one[4])

        sizeAll += 1

        condition_1 = (main_win < rateMax and main_win > rateMin and main_win < client_win)
        condition_2 = (client_win < rateMax and client_win > rateMin and client_win < main_win )
        if condition_1:
            if result == 1:
                rate_1 += main_win - 1
            else:
                rate_1 -= 1
            
            if result == 0:
                rate_3 += ping -1 
            else :
                rate_3 -= 1

            size += 1 
        elif  condition_2:
            if result == -1:
                rate_1 += client_win - 1
            else:
                rate_1 -= 1

            if result == 0:
                rate_3 += ping -1 
            else :
                rate_3 -= 1
            size += 1 

        if condition_1:
            if result == -1:
                rate_2 += client_win - 1
            else:
                rate_2 -= 1
        elif  condition_2:
            if result == 1:
                rate_2 += main_win - 1
            else:
                rate_2 -= 1
 
    print(name,round(rateMin, 2), "num:", num, "买赢：", round(rate_1, 2), " 买输：", round(rate_2, 2), " size = ", size, " size all = ",sizeAll)
       
def getResult_2(name, rateMin, rateMax, num):
    db_name = "k_163_2016"

    data = sql.queryByTypeNum(name, db_name, str(num))
    if num == -1 :
        data = sql.queryByType(name, db_name)

    main_win = 0
    client_win = 0
    tie_win = 0


    size = 0
    sizeAll = 0

    rate_1 = 0
    rate_2 = 0
    rate_3 = 0

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main = one[0]
        client = one[1]

        ping = one[6]
        main_win =  one[8]
        client_win = one[9]

        result = int(one[4])

        sizeAll += 1

        teamName = "佩斯卡拉"
        condition_1 = (main == teamName)
        condition_2 = (client == teamName)

        # if num == 37:
        #     print(1)

        if condition_1:
            if result == -1:
                rate_1 += client_win - 1
            else:
                rate_1 -= 1

            size += 1 
        elif  condition_2:
            if result == 1:
                rate_1 += main_win - 1
            else:
                rate_1 -= 1
            size += 1 
    if size == 0 :
        return

    print(name, num,  "做空：", round(rate_1, 2),  " size = ", size, " size all = ",sizeAll)


def getResult_3(name, rateMin, rateMax, num):
    db_name = "k_163_2017"

    data = sql.queryByTypeNum(name, db_name, str(num))
    if num == -1 :
        data = sql.queryByType(name, db_name)

    main_win = 0
    client_win = 0


    size = 0
    sizeAll = 0

    rate = {}


    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main = one[0]
        client = one[1]

        ping = one[6]
        main_win =  one[8]
        client_win = one[9]

        result = int(one[4])

        sizeAll += 1

        if not rate.__contains__(main):
            rate[main] = 0
        if not rate.__contains__(client):
            rate[client] = 0

        rateMain = rate[main]
        rateclient = rate[client]

        

        if Kong == 1:
            if result == 1:
                rateMain -= 1
                rateclient += main_win - 1
            elif result == -1:
                rateMain += client_win - 1
                rateclient -= 1
            else:
                rateMain -= 1
                rateclient -= 1
        else:
            if result == -1:
                rateMain -= 1
                rateclient += client_win - 1
            elif result == 1:
                rateMain += main_win - 1
                rateclient -= 1
            else:
                rateMain -= 1
                rateclient -= 1

        rate[main] = rateMain
        rate[client] = rateclient

    # sorted(rate.items(), key=lambda x:x[0], reverse=True)
    rate = sorted(rate.items(), key=lambda e:e[1], reverse=True)
    print(rate)
    print(sizeAll)


def getResult_4(name, rateMin, rateMax, num, url):
    db_name = "k_163_2017"

    data = sql.queryByTypeNum(name, db_name, str(num))
    if num == -1 :
        data = sql.queryByType(name, db_name)

    main_win = 0
    client_win = 0

    size = 0
    size_1 = 0
    sizeAll = 0

    rate = {}
    rate_1 = {}

    num = 0

    if len(data) == 0 :
        return
    for one in data :
        offset = 3
        main = one[0]
        client = one[1]

        mainScore = one[2]
        clientScore = one[3]

        ping = one[6]
        main_win =  one[8]
        client_win = one[9]

        numGet= one[10]
        if num < numGet:
            num = numGet

        result = int(one[4])

        sizeAll += 1

        if not rate.__contains__(main):
            rate[main] = {"count":0, "value":0,"rate":0}
        if not rate.__contains__(client):
            rate[client] = {"count":0, "value":0,"rate":0}
        if not rate_1.__contains__(client):
            rate_1[client] = {"count":0, "value":0,"rate":0}

        tmp = rate[main]
        if mainScore > 0: 
            tmp["count"] += 1
            tmp["value"] += 1
            tmp["rate"] = round(tmp["value"] / tmp["count"], 2) 
        else:
            tmp["count"] += 1

        rate[main] = tmp

        tmp = rate_1[client]
        if clientScore > 0: 
            tmp["count"] += 1
            tmp["value"] += 1
            tmp["rate"] = round(tmp["value"] / tmp["count"], 2) 
        else:
            tmp["count"] += 1
        rate_1[client] = tmp


        if mainScore > 0 and clientScore > 0:
            size += 1
        # else:
        #     size_1 += 1
        #     rate[main] += 1
        #     rate[client] += 1
        # elif mainScore == 0:
        #     rate[client] +=1
        # elif clientScore == 0:
        #     rate[main] +=1
            

    # sorted(rate.items(), key=lambda x:x[0], reverse=True)
    if 0:
        print("主场进球")
        rate = sorted(rate.items(), key=lambda e:e[1]["rate"], reverse=False)
        for key in rate:
            print(key[0], key[1]["rate"],  key[1]["count"])
        
        print("\n 客场进球 \n")
        rate_1 = sorted(rate_1.items(), key=lambda e:e[1]["rate"], reverse=False)
        for key in rate_1:
            print(key[0], key[1]["rate"],  key[1]["count"])

    html = parser(url)
    data = html.getData()
    result = []
    for game in data :
        main = game[0]
        client = game[1]
        a =  rate[main]["rate"] * rate_1[client]["rate"]
        if a == 1:
            p = 100
        else:
            p = 1/(1 - rate[main]["rate"] * rate_1[client]["rate"])
        p = round(p,2)
        tmp = []
        tmp.append(main)
        tmp.append(client)
        tmp.append(p)
        result.append(tmp)
    
    # result.sort(lambda)
    print(sorted(result, key=lambda x:x[2], reverse=False))

    # print(round(sizeAll/(sizeAll - size), 2))
    # print(round(size/sizeAll, 2))
    # print(num)
    # print(name, "做空：", rate)

def compare_1(name): 
    for i in range(17) :
        rateMin = i*0.1 + 1
        rateMax = rateMin + 0.1*1
        getResult_1(name, rateMin,  rateMax, -1)

def compare_2(name): 
    getResult_1(name, 2,  2.6, -1)

def compare_3(name): 
    for i in range(39) :
        getResult_1(name, 1,  2.4, i)

def compare_4(name):
    getResult_2(name, 1,  2.6, -1)

def compare_5(name):
    for i in range(39) :
        getResult_2(name, 1,  2.6, i)

def compare_6(name):
    getResult_3(name, 1,  2.6, -1)  

def compare_7(name, url):
    getResult_4(name, 1,  2.6, -1, url)  


# compare_7("英超")
# compare_7("意甲")
# compare_7("西甲")
# compare_7("德甲")

# compare_6("英冠")
# compare_6("英甲")
# compare_6("巴甲")
# compare_6("J联赛")
# compare_2("欧洲冠军联赛")
# compare_4("英超")
# compare_7("德乙",  "http://saishi.caipiao.163.com/11/14008.html?weekId=11&groupId=&roundId=41486&indexType=0&guestTeamId=")
# compare_7("荷乙","http://saishi.caipiao.163.com/5/13843.html?weekId=10&groupId=&roundId=41039&indexType=0&guestTeamId=")
compare_7("法乙","http://saishi.caipiao.163.com/17/14061.html?weekId=12&groupId=&roundId=41647&indexType=0&guestTeamId=")
