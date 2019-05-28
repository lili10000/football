from db.mysql import sqlMgr
import json


def docal():
    sql = sqlMgr('localhost', 'root', '861217', 'football')
    games = sql.queryByTypeAll("k_gamedic_v2")

    index_1 = 1
    index_2 = 1
    index_3 = 1


    record = {}
    for game in games:
        gameName = game[1]
        data = sql.queryByType(gameName, "k_gameInfoDetail")
        # 
        if len(data) == 0 :
            continue
        print(gameName, "   size:", len(data))

        minValue = 100
        # minValue = 100
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

        def cal(minValue):
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
            if tmpMin < minValue:
                minValue = tmpMin
                record[gameName] = [minValue, index_1, index_2, index_3]
            
            return minValue
            # print(max, index, winSize - lostSize, winSize, lostSize)       

        
        size = 5
        for i in range(size):
            index_1 = i
            for j in range(size):
                index_2 = j
                for k in range(size):
                    index_3 = k

                    if index_1 + index_2 + index_3 == 0:
                        continue

                    minValue = cal(minValue)
        # break

    for gameName in record:
        dic = {"1": record[gameName][1], "2": record[gameName][2],"3": record[gameName][3]}
        param=json.dumps(dic)
        sql.updateParam("k_gamedic_v2", gameName, param)
        print(gameName, record[gameName])

# docal()