from db.mysql import sqlMgr
import time

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
            saveTime = one[9]


            # key = '澳'
            # if key in name:
            #     gameSum += 1
            # else:
            #     continue

            if saveTime == None:
                continue
            timeArray = time.localtime(saveTime)
            hour = timeArray[3]
            key = hour
            

            if result_slice.__contains__(key) == False:
                result_slice[key] = sumData()
            
            tmp = result_slice[key]

            if haveScore == 1:
                tmp.haveSum += 1
            else:
                tmp.NoSum += 1
            

            result_slice[key] = tmp

        # print ("gameSum",gameSum)
        
        key_list = sorted(result_slice.keys())

        for key in key_list:

            rate = -1
            dataTmp = result_slice[key]
            gameSum = dataTmp.NoSum + dataTmp.haveSum
            if dataTmp.haveSum != 0 and dataTmp.NoSum != 0 and gameSum > 10:
                rate = round(dataTmp.NoSum/dataTmp.haveSum, 2)
            else:
                continue
            
            if rate != -1 and rate < 2 :
                print("hour:",key," 比率:",rate, "gameSum",gameSum)
                

