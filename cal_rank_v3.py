from db.mysql import sqlMgr
import json



sql = sqlMgr('localhost', 'root', '861217', 'football')


for 

    min = 100

    def checkScore(score1, scoreLost1, score2, scoreLost2):
        if score1*scoreLost1*score2*scoreLost2 == 0:
            return 2.5


        main = (score1 + scoreLost2)/2
        client = (score2 + scoreLost1)/2
        div = main + client
        return div/10



    def getWeg():
        weg = [index_1, index_2, index_3]
        wegEnd = []
        Sum = 0
        for tmp in weg:
            Sum += tmp

        for tmp in weg:
            wegEnd.append(tmp / Sum)
        return wegEnd

    def cal():
        winSize = 0
        lostSize = 0
        for one in data:
            info = one[2]
            
            info = json.loads(info)

            allScore = checkScore(int(info['his_main_all_score']), int(info['his_main_all_score']), 
                int(info['his_client_all_score']), int(info['his_client_all_score_lost']))
            score1 = checkScore(int(info['his_main_1_score']), int(info['his_main_1_score_lost']), 
                int(info['his_client_1_score']), int(info['his_client_1_score_lost']))
            score = checkScore(int(info['his_main_main_socre']), int(info['his_main_main_socre_lost']), 
                int(info['his_client_client_socre']), int(info['his_client_client_socre_lost']))
           

            weg = getWeg()
            rate = allScore * weg[0]
            rate += score1 * weg[1]
            rate += score * weg[2]


            if info['main_score'] + info['client_score']  > rate:
                winSize += 1
            elif info['main_score'] - info['client_score'] < rate:
                lostSize += 1

        tmpMin = abs(winSize - lostSize)
        global min
        if tmpMin < min:
            min = tmpMin
            record[gameName] = [min, index_1, index_2, index_3]
        # print(max, index, winSize - lostSize, winSize, lostSize)       

    min = 100
    size = 5
    for i in range(size):
        index_1 = i
        for j in range(size):
            index_2 = j
            for k in range(size):
                index_3 = k

                if index_1 + index_2 + index_3 == 0:
                    continue

                cal()
    # break

for gameName in record:
    dic = {"1": record[gameName][1], "2": record[gameName][2],"3": record[gameName][3]}
    param=json.dumps(dic)
    sql.updateParam("k_gamedic_v2", gameName, param)
    print(gameName, record[gameName])
