from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20

def getResult_1(name):
    data = sql.queryByType(name, "k_163")

    main_win = 0
    client_win = 0
    tie_win = 0
    size = 0

    winCount = 0
    lostCount = 0

    flag_win = False
    flag_lost = False
    changeCount = 0

    if len(data) == 0 :
        return
    size = len(data)
    for one in data :
        offset = 3
        main_score = int(one[2])
        client_score = int(one[3])

        rate_result = one[4]

        rate_win = float(one[8])
        rate_lost = float(one[9])

        rate = float(one[6])
        # if rate_lost > rate_lost_first :

        if rate_result > 0 :
            winCount += 1
            if (main_score - client_score + rate) == 0.25 :
                main_win += (rate_win - 1)*0.5
            else :
                main_win += rate_win - 1
            client_win += -1

        elif rate_result < 0 :
            lostCount +=1 
            if (client_score - main_score + rate) == 0.25 :
                client_win += (rate_lost - 1)*0.5
            else :
                client_win += rate_lost - 1
            main_win += -1



    print( "win",str(round(main_win/size, 2)), "   lost",str(round(client_win/size, 2)),"    ",str(size), winCount, lostCount,"    ",name)



def getResult_3(name, key, key_max, min_win, db_key):
    data = sql.queryByType(name, db_key)

    main_win = 0
    client_win = 0
    tie_win = 0
    size = 0

    winCount = 0
    lostCount = 0

    flag_win = False
    flag_lost = False
    changeCount = 0

    if len(data) == 0 :
        return
    # size = len(data)
    for one in data :
        offset = 3
        main_score = int(one[2])
        client_score = int(one[3])

        result = one[4]
        rate_tie = one[6]

        rate_win = float(one[8])
        rate_lost = float(one[9])

        # rate = float(one[6])
        # if rate_lost > rate_lost_first :

        if rate_win < key or  rate_win > key_max:
            continue
        
        size += 1

        if result > 0 :
           
            winCount += 1
            main_win += rate_win - 1
            client_win += -1
            tie_win += -1
        elif result < 0 :
            lostCount +=1 
            client_win += rate_lost - 1
            main_win += -1
            tie_win += -1
        else :
            tie_win += rate_tie - 1
            main_win += -1
            client_win += -1
    if size == 0 or size < 10 :
        return
    if main_win/size >min_win or client_win/size >min_win or tie_win/size >min_win :
        print("key[",round(key, 2),round(key_max, 2), "]win",str(round(main_win/size, 2)), "   lost",str(round(client_win/size, 2)),"    tie",str(round(tie_win/size, 2)),"    ",str(size), winCount, lostCount,"    ",name)


# db_key = "k_163_16_17"
db_key = "k_163"
# db_key = "k_163_15_16"
# db_key = "k_163_14_15"
def compare(name): 
    # getResult_2(name)
    # return
    min_win = 0.01
    for index in range(10) :
        # print("start", 1 + 0.3*index)
        key = 1 + 0.3*index
        key_max = 1 + 0.3*(index+1)
        # getResult_1(name, key,key_max, min_win) 
        getResult_3(name, key,key_max, min_win, db_key) 
    
    getResult_3(name, 4,100, min_win, db_key) 



# getResult_1("中超")
# compare("J联赛")
# compare("J2联赛")
# compare("日联杯")
# compare("美职联")
# compare("巴甲")
# compare("阿甲")
# compare("挪超")
# compare("瑞典超")
# compare("瑞典甲")
# compare("冰岛超")
# compare("k联赛")
# compare("英超")
# compare("英冠")
# compare("英甲")
# compare("意甲")
# compare("意乙")
# compare("德甲")
# compare("西甲")
# compare("法甲")
# compare("足总杯")
compare("国际A级")