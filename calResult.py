from db.mysql import sqlMgr
import time

sql = sqlMgr('localhost', 'root', '861217', 'football')
data = sql.queryByTypeAll("k_commend")
total = 0
# size = len(data)
size = 0
# print("size:",size)
for one in data:
    result = one[5]
    if result == 1:
        total += 4
    elif result == 0.5:
        total += 1
    elif result < 0:
        total += -1
    else:
        continue

    size += 1
    
print(size, total, round(total/size, 2))