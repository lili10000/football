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
        type_game = one[2]
        main_rank = one[3]
        client_rank = one[4]
        main_score = one[5]
        client_score = one[6]
        rate = float(one[7])

        tmp = main_rank - client_rank
        rateValid = 0
        if  tmp <= -10:
            rateValid = -0.75
        elif tmp <= -5:
            rateValid = -0.5
        elif tmp <= 0:
            rateValid = -0.25
        elif tmp <= 5:
            rateValid = 0.25
        elif tmp <= 10:
            rateValid = 0.5  
        else:
            rateValid = 0.75

        rateValid -= 0.5
        
        rateTmp = rateValid - rate
        # if abs(rateTmp) < 0.5:
        #     continue

        
        rate_compare = 0.5

        for index in range(1):
            rate_compare = index * 0.25

            rate_compare = 0.5

            if abs(rateTmp) != rate_compare :
                continue

            if rate == 0.25 or rate <= -0.75:
                rate_compare = index * 0.25
            else:
                continue


            buyMain = False
            re_rate_compare = -1 *rate_compare
            if rateTmp <= re_rate_compare:
                buyMain = True

            # rate_compare = rate

            if result_slice.__contains__(rate_compare) == False:
                result_slice[rate_compare] = DataSize()

            main_win = True
            result = False
            if main_score - client_score + rate < 0:
                if buyMain:
                    result_slice[rate_compare].main_lost_size += 1
                else:
                    result_slice[rate_compare].client_win_size += 1
            elif main_score - client_score + rate == 0:
                continue
            else:
                if buyMain:
                    result_slice[rate_compare].main_win_size += 1
                else:
                    result_slice[rate_compare].client_lost_size += 1


        # if '输' in result:
        #     lost_size += 1
        #     if '主' in buy:
        #         result_slice[rate].main_lost_size += 1
        #     else:
        #         result_slice[rate].client_lost_size += 1
        # elif '赢' in result:
        #     win_size += 1
        #     if '主' in buy:
        #         result_slice[rate].main_win_size += 1
        #     else:
        #         result_slice[rate].client_win_size += 1

    # print("main_win_size:",main_win_size,"main_lost_size",main_lost_size)  
    key_list = sorted(result_slice.keys())
    for key in key_list:
        # print("分布 rate:",rate)
        gain_main = 0
        gain_client = 0
        main_sum = result_slice[key].main_win_size + result_slice[key].main_lost_size
        client_sum = result_slice[key].client_win_size + result_slice[key].client_lost_size
        if main_sum > 0:
            gain_main = round(2*result_slice[key].main_win_size/main_sum - 1,2)
        if client_sum > 0:
            gain_client = round(2*result_slice[key].client_win_size/client_sum -1 ,2)

        print("分布 rate:",key,"buy_main     win:",result_slice[key].main_win_size, "    lost:",result_slice[key].main_lost_size,"  gain:",gain_main)
        print("分布 rate:",key,"buy_client   win:",result_slice[key].client_win_size,"  lost",result_slice[key].client_lost_size,"  gain:",gain_client) 

getResult(name)