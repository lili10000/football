from db.mysql import sqlMgr
import time
# from ouToAsia import ouToAsia

sql = sqlMgr('localhost', 'root', '861217', 'football')
data = sql.queryByTypeAll("k_commend")



def cal(ver, caltype):
    size = 1
    if caltype == 1:
        size = 7
    if caltype == 2:
        size = 6

    for i in range(size):
        sum = {}
        typeSum = {}
        for one in data :
            timeCreate = int(one[1])
            type = one[3]
            result = int(one[5])
            buyBig = int(one[4])
            version = int(one[6])
            if version != ver:
                continue

            if result == 0 :
                continue

            timeStruct = time.localtime(timeCreate)
            # print(timeStruct)

            if caltype == 1:
                if timeStruct.tm_wday != i:
                    continue
            
            if caltype == 2:
                if timeStruct.tm_hour > 4*(i+1) or timeStruct.tm_hour < 4*i:
                    continue

            if "球" in type and ver == 5:
                continue

            if sum.__contains__(type) == False:
                sum[type] = {-1:0, 1:0, "sum":0}
            sum[type][buyBig] += result
            sum[type]["sum"] += 1
            if typeSum.__contains__(buyBig) == False:
                typeSum[buyBig] = 0
            typeSum[buyBig] += 1

        for index in sum:
            # print(ver, index, sum[index], round(index/sum[index], 2))
            # print(i+1," | ",ver, index, sum[index][1]+sum[index][-1], round( (sum[index][1]+sum[index][-1]) *100/sum[index]["sum"] , 2),"%    ",sum[index])
            print(i+1," | ",ver, index, sum[index][1]+sum[index][-1], round( (sum[index][1]+sum[index][-1]) *100/sum[index]["sum"] , 2),"%    ",sum[index],
            round(sum[index][-1]/typeSum[-1],2), round(sum[index][1]/typeSum[1], 2))


# cal(5)
# cal(4, 0)

for i in range(3):
    cal(5, i)
    print(" ")
    # cal(4, i)
    # print(" ")



# cal(6, False)
# cal(5, False)
# cal(4)
# cal(3)
# cal(2)

    