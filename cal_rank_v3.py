from db.mysql import sqlMgr
import json

sql = sqlMgr('localhost', 'root', '861217', 'football')

max = 2.5

def checkRank(mainRank, clientRank, teamSum):
    divRank = mainRank - clientRank
    global max
    step =  (max / teamSum) / 0.25
    rate = (divRank / step)*0.25 - 0.25
    return rate
    
def checkHis2(win, ping, lost):
    gameSum = win + ping + lost
    global max
    step = (max / gameSum) / 0.25

    div = (lost - win)
    rate = int(div * step) * 0.25 - 0.25
    return rate

def checkHisAll(win1, ping1, lost1, win2, ping2, lost2):
    gameSum = win1 + ping1 + lost1
    global max
    step = (max / gameSum) / 0.25
    div = (lost1 - win1)
    main_rate = int(div * step) * 0.25

    gameSum = win2 + ping2 + lost2
    step = (max / gameSum) / 0.25
    div = (lost2 - win2)
    client_rate = int(div * step) * 0.25

    rate = main_rate - client_rate - 0.25
    return rate


def checkHis1(win1, ping1, lost1, win2, ping2, lost2):
    gameSum = win1 + ping1 + lost1
    global max
    step = (max / gameSum) / 0.25
    div = (lost1 - win1)
    main_rate = int(div * step) * 0.25 - 0.25

    gameSum = win2 + ping2 + lost2
    step = (max / gameSum) / 0.25
    div = (lost2 - win2)
    client_rate = int(div * step) * 0.25

    rate = main_rate - client_rate - 0.25
    return rate

def checkScore(main, main_lost, client, client_lost):
    if (main + main_lost) == 0 or (client + client_lost) == 0:
        return -0.25

    attc = main / (main + main_lost) - 0.5
    defend =  client_lost / (client + client_lost) - 0.5

    global max
    step = max / 0.25
    rate = int((attc + defend) * step) *0.25 
    return rate


def checkScore_v2(score1, scoreLost1, score2, scoreLost2):
    if score1*scoreLost1*score2*scoreLost2 == 0:
        return 2.5


    main = (score1 + scoreLost2)/2
    client = (score2 + scoreLost1)/2
    div = main + client
    return div/10

def getWeg():
    weg = [1, 1, 1, 1, 1]
    wegEnd = []
    Sum = 0
    for tmp in weg:
        Sum += tmp

    for tmp in weg:
        wegEnd.append(tmp / Sum)
    return wegEnd

def getWeg_v2():
    weg = [1, 1, 1]
    wegEnd = []
    Sum = 0
    for tmp in weg:
        Sum += tmp

    for tmp in weg:
        wegEnd.append(tmp / Sum)
    return wegEnd

def cal(gameName):
    winBig = 0
    winSmall = 0
    lostBig  = 0
    lostSmall  = 0
    sizeSum = 0

    scoreSum = 0
    scoreCalSum = 0

    result = {}
    data = sql.queryByTypeAll("k_gameInfoDetail")
    total = len(data)
    for one in data:
        info = one[2]
        
        info = json.loads(info)


        rankRate = checkRank(int(info['main_rank']), int(info['client_rank']), 20)
        his2Rate = checkHis2(info['his_2_win'], info['his_2_ping'], info['his_2_lost'])
        hisAllRate = checkHisAll(info['his_main_all_win'], info['his_main_all_ping'], info['his_main_all_lost'],
            info['his_client_all_win'], info['his_client_all_ping'], info['his_client_all_lost'])

        his1Rate = checkHis1(info['his_main_1_win'], info['his_main_1_ping'], info['his_main_1_lost'],
            info['his_client_1_win'], info['his_client_1_ping'], info['his_client_1_lost'])

        scoreRate = checkScore(info['his_main_main_socre'], info['his_main_main_socre_lost'],
            info['his_client_client_socre'], info['his_client_client_socre_lost'])

        weg = getWeg()

        rate = rankRate * weg[0]
        rate += his2Rate * weg[1]
        rate += hisAllRate * weg[2]
        rate += his1Rate * weg[3]
        rate += scoreRate * weg[4]

        rate = int(rate / 0.25) * 0.25

        winFlag = False
        if info["main_score"] - info["client_score"] - rate > 0:
            winFlag = True



        allScore = checkScore_v2(int(info['his_main_all_score']), int(info['his_main_all_score']), 
            int(info['his_client_all_score']), int(info['his_client_all_score_lost']))
        score1 = checkScore_v2(int(info['his_main_1_score']), int(info['his_main_1_score_lost']), 
            int(info['his_client_1_score']), int(info['his_client_1_score_lost']))
        score = checkScore_v2(int(info['his_main_main_socre']*10), int(info['his_main_main_socre_lost']*10), 
            int(info['his_client_client_socre']*10), int(info['his_client_client_socre_lost']*10))
        

        weg = getWeg_v2()
        scoreRate = allScore * weg[0]
        scoreRate += score1 * weg[1]
        scoreRate += score * weg[2]

        scoreSum += info["main_score"] + info["client_score"]
        scoreCalSum += scoreRate

        bigFalg = False
        if info["main_score"] + info["client_score"] - scoreRate > 0:
            bigFalg = True



        # if bigFalg:
        #     winBig += 1
        # else:
        #     winSmall += 1

        div = scoreRate - abs(rate)

        div = int(div / 0.25) * 0.25

        if not result.__contains__(div):
            result[div] = [0,0,0,0]


        sizeSum += 1

        if winFlag and bigFalg:
            winBig += 1
            result[div][0] += 1
        elif winFlag and bigFalg == False:
            winSmall += 1
            result[div][1] += 1
        elif winFlag == False and bigFalg:
            lostBig += 1
            result[div][2] += 1
        elif winFlag == False and bigFalg == False:
            lostSmall += 1
            result[div][3] += 1

    # tmpMin = abs(winSize - lostSize)

    # record[gameName] = [min, index_1, index_2, index_3]
    print(sizeSum, winBig, winSmall, lostBig, lostSmall)    


    for key in  result:
        data = result[key]
        dataSum = data[0] + data[1]+ data[2]+ data[3]
        rateMax = 0

        def getRate(sum, data, rateCmp):
            tmpRate = round(data/sum, 2)
            if rateCmp < tmpRate:
                return tmpRate
            return rateCmp
        
        rateMax = getRate(dataSum, data[0], rateMax)
        rateMax = getRate(dataSum, data[1], rateMax)
        rateMax = getRate(dataSum, data[2], rateMax)
        rateMax = getRate(dataSum, data[3], rateMax)

        if rateMax > 0.3 and dataSum > 0.1*total :
            print(rateMax, key, data)
            # result[rateMax] = key

    # print(result)
    # print(round(scoreSum/sizeSum, 2), round(scoreCalSum/sizeSum, 2))  



cal("中超")

