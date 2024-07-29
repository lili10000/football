import json
from db.mysql import sqlMgr

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

def getWeg():
    weg = [1,0,2,1,1]
    wegEnd = []
    Sum = 0
    for tmp in weg:
        Sum += tmp
    for tmp in weg:
        wegEnd.append(tmp / Sum)
    return wegEnd

def cal(info):
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


    
    return rate


def checkScore_v2(score1, scoreLost1, score2, scoreLost2):
    if score1*scoreLost1*score2*scoreLost2 == 0:
        return 2.5


    main = (score1 + scoreLost2)/2
    client = (score2 + scoreLost1)/2
    div = main + client
    return div/10



def getWegScore(index_1, index_2, index_3):
    weg = [index_1, index_2, index_3]
    wegEnd = []
    Sum = 0
    for tmp in weg:
        Sum += tmp

    for tmp in weg:
        wegEnd.append(tmp / Sum)
    return wegEnd

def calScore(info):
    sql = sqlMgr('localhost', 'root', '861217', 'football')

    info = json.loads(info)
    gameType = info['type']

    data = sql.queryByName('k_gamedic_v2', gameType)

    index_1 = 1
    index_2 = 1
    index_3 = 1

    if len(data) > 0:
        param = data[0][2]
        param = json.loads(param)
        index_1 = int(param['1'])
        index_2 = int(param['2'])
        index_3 = int(param['3'])



    allScore = checkScore_v2(int(info['his_main_all_score']), int(info['his_main_all_score']), 
        int(info['his_client_all_score']), int(info['his_client_all_score_lost']))
    score1 = checkScore_v2(int(info['his_main_all_score']), int(info['his_main_all_score']), 
        int(info['his_client_all_score']), int(info['his_client_all_score_lost']))
    score = checkScore_v2(int(info['his_main_main_socre']*10), int(info['his_main_main_socre_lost']*10), 
        int(info['his_client_client_socre']*10), int(info['his_client_client_socre_lost']*10))
    

    weg = getWegScore(index_1, index_2, index_3)
    rate = allScore * weg[0]
    rate += score1 * weg[1]
    rate += score * weg[2]
    return round(rate, 2)
