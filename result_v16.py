from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
data = sql.queryByTypeAll("k_endScore")

print("sum = ", len(data))



class sumData:
    def __init__(self):
        self.haveSum = 0
        self.NoSum = 0

dataSum = len(data)
gameSum = 0
# dataMax = sumData()

big = True
# big = False
rateMax = 100
rateMin = -1



for i in range(1):
    for j in range(1):
        # compareRate = (i+1)*0.25
        # compareRate = 1.5

        # compareScore = j
        # compareScore = 0

        result_slice = {}
        for one in data :
            # main = one[0]
            name = one[1]
            rate = one[2]
            hostScore = one[3]
            guestScore = one[4]
            haveScore = one[5]

            mainRate = one[6] 
            clientRate = one[7]
            socreTime = one[8]

            scoreSum = hostScore + guestScore
            keyTmp = rate - scoreSum


            # if '沙特' in name:
            #     gameSum += 1
            # else:
            #     continue

            tmpSlice = name.split(' ')
            name = tmpSlice[0]
            key = name

            # if (keyTmp == compareRate ) and (scoreSum == compareScore):
            #     gameSum += 1
            # else:
            #     continue 


            # key = int (socreTime / 60)
            # if key > 10:
            #     key = 10



            if result_slice.__contains__(key) == False:
                result_slice[key] = sumData()
            
            tmp = result_slice[key]

            if haveScore == 1:
                tmp.haveSum += 1
            else:
                tmp.NoSum += 1
            
            # if key == 0.25:
            #     print (one)

            result_slice[key] = tmp

        # print ("gameSum",gameSum)
        # key_list = sorted(result_slice.keys())


        sql.cleanAll("k_nameRate")
        for key in result_slice:

            rate = -1
            dataTmp = result_slice[key]
            gameSum = dataTmp.NoSum + dataTmp.haveSum
            if dataTmp.haveSum != 0 and dataTmp.NoSum != 0 and gameSum > 10:
                rate = round(dataTmp.NoSum/dataTmp.haveSum, 2)
            else:
                continue
            
            if rate != -1 and (rate <= 2 ):
                input = "'"+ key + "','"  + str(rate) + "','"  + str(dataTmp.haveSum) + "','"  + str(dataTmp.NoSum) +"'"
                sql.insert(input, "k_nameRate")



            # rateMax = 2
            # if rate < rateMax :
            #     rateMax = rate
            #     print("买大 key", key, "    rate:", rate, "    haveSum:", dataTmp.haveSum, "NoSum:", dataTmp.NoSum)
            # rateMin = 6
            # if rate > rateMin :
            #     rateMin = rate
            #     print("买小 key", key, "    rate:", rate, "    haveSum:", dataTmp.haveSum, "NoSum:", dataTmp.NoSum)
