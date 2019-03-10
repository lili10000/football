from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')

name = None
# name = "英超"


def getResult(name):
    data = []
    if name == None:
        data = sql.queryByTypeAll("k_corner")
    else:
        data = sql.queryByType(name, "k_corner")

    if len(data) == 0 :
        return
    print("sum = ", len(data))

    win_size = 0
    lost_size = 0

    main_win_size = 0
    main_lost_size = 0
    client_win_size = 0
    client_lost_size = 0



    class DataSize:
        def __init__(self):  
            self.main_win_size = 0     
            self.main_lost_size = 0    
            self.client_win_size = 0     
            self.client_lost_size = 0        


    result_slice = {}
    for one in data :
        main = one[0]
        client = one[1]
        main_score = one[2]
        client_score = one[3]
        rate = float(one[4])
        gameType = one[5]
        gameTime = one[9]

        sql.updateId(main,gameTime, 'k_corner')



                





            





getResult(name)