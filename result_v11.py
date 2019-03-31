from db.mysql import sqlMgr
# from ouToAsia import ouToAsia

sql = sqlMgr('localhost', 'root', '861217', 'football')
data = sql.queryByTypeAll("k_commend")

sum = {}
for one in data :
    type = one[2]
    result = int(one[4])
    if result == 0 :
        continue
    if sum.__contains__(type) == False:
        sum[type] = 0
    sum[type] += result

for index in sum:
    print(index, sum[index])
    