from db.mysql import sqlMgr
# from ouToAsia import ouToAsia

sql = sqlMgr('localhost', 'root', '861217', 'football')
data = sql.queryByTypeAll("k_commend")



def cal(ver):
    sum = {}
    for one in data :
        type = one[2]
        result = int(one[4])
        buyBig = int(one[3])
        version = int(one[5])
        if version != ver:
            continue

        if result == 0 :
            continue
        if sum.__contains__(type) == False:
            sum[type] = {-1:0, 1:0, "sum":0}
        sum[type][buyBig] += result
        sum[type]["sum"] += 1

    for index in sum:
        # print(ver, index, sum[index], round(index/sum[index], 2))
        print(ver, index, sum[index][1]+sum[index][-1], round( (sum[index][1]+sum[index][-1]) *100/sum[index]["sum"] , 2),"%    ",sum[index])


cal(5)
cal(6)
# cal(4)
# cal(3)
# cal(2)
# cal(1)
    