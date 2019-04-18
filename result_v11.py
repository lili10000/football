from db.mysql import sqlMgr
import time
# from ouToAsia import ouToAsia

sql = sqlMgr('localhost', 'root', '861217', 'football')
data = sql.queryByTypeAll("k_commend")



def cal(ver):
    for i in range(1):
        sum = {}
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

            # if timeStruct.tm_wday != i:
            #     continue

            if "球" in type:
                continue

            if sum.__contains__(type) == False:
                sum[type] = {-1:0, 1:0, "sum":0}
            sum[type][buyBig] += result
            sum[type]["sum"] += 1

        for index in sum:
            # print(ver, index, sum[index], round(index/sum[index], 2))
            print(i+1," | ",ver, index, sum[index][1]+sum[index][-1], round( (sum[index][1]+sum[index][-1]) *100/sum[index]["sum"] , 2),"%    ",sum[index])


# cal(5)
cal(6)
# cal(4)
# cal(3)
# cal(2)
cal(5)
    