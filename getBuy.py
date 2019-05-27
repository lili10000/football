from db.mysql import sqlMgr
import time
# from ouToAsia import ouToAsia

sql = sqlMgr('localhost', 'root', '861217', 'football')
now = int(time.time()) 
dataList = sql.queryByTime("k_commend", now)
for data in dataList:
    print(data)


