from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
name = None
def getResult(name):
    data = []
    if name == None:
        data = sql.queryByTypeAll("k_rate_check")
    else:
        data = sql.queryByType(name, "k_rate_check")

    if len(data) == 0 :
        return
    print("sum = ", len(data))

    win_size = 0
    lost_size = 0

    main_win_size = 0
    main_lost_size = 0
    client_win_size = 0
    client_lost_size = 0

    for one in data :
        main = one[0]
        client = one[1]
        type_game = one[2]
        buy= one[3]
        rate = float(one[4])
        result =  one[5]
        if '输' in result:
            lost_size += 1
            if '主' in buy:
                main_lost_size += 1
            else:
                client_lost_size += 1
        elif '赢' in result:
            win_size += 1
            if '主' in buy:
                main_win_size += 1
            else:
                client_win_size += 1

    print("win_size:",win_size,"lost_size",lost_size)  
    print("buy_main     win:",main_win_size,"    lost:",main_lost_size)    
    print("buy_client   win:",client_win_size,"  lost",client_lost_size) 

getResult(name)