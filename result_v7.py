from db.mysql import sqlMgr

sql = sqlMgr('localhost', 'root', '861217', 'football')
sizeMin = 20


def getResult_1(gameName, mainName, clientName, type):
    data = sql.queryTeamDataMain(gameName, mainName, "k_163")

    mainScore = []
    main_0_score = 0
    main_1_score = 0
    main_2_score = 0
    main_3_score = 0
    main_3_more_score = 0

    clientScore = []
    client_0_score = 0
    client_1_score = 0
    client_2_score = 0
    client_3_score = 0
    client_3_more_score = 0

    for one in data :
        main_score = int(one[2])
        client_score = int(one[3])

        mainScore.append(main_score)
        if main_score == 0 :
            main_0_score += 1
        elif main_score == 1 :
            main_1_score += 1
        elif main_score == 2 :
            main_2_score += 1
        elif main_score == 3 :
            main_3_score += 1
        else :
            main_3_more_score += 1

    data = sql.queryTeamDataClient(gameName, clientName, "k_163")
    for one in data :
        main_score = int(one[2])
        client_score = int(one[3])

        clientScore.append(client_score)
        if client_score == 0 :
            client_0_score += 1
        elif client_score == 1 :
            client_1_score += 1
        elif client_score == 2 :
            client_2_score += 1
        elif client_score == 3 :
            client_3_score += 1
        else :
            client_3_more_score += 1
    
    if len(mainScore) > 0 :
        main_0 = main_0_score / len(mainScore)
        main_1 = main_1_score / len(mainScore)
        main_2 = main_2_score / len(mainScore)
        main_3 = main_2_score / len(mainScore)
        main_3_more = main_3_more_score / len(mainScore)
    else :
        return

    if len(clientScore) > 0 :
        client_0 = client_0_score / len(clientScore)
        client_1 = client_1_score / len(clientScore)
        client_2 = client_2_score / len(clientScore)
        client_3 = client_3_score / len(clientScore)
        client_3_more = client_3_more_score / len(clientScore)
    else :
        return

    mainMean = round(sum(mainScore)/len(mainScore),3)
    clientMean = round(sum(clientScore)/len(clientScore),3)
    print("主队", mainMean, len(mainScore), "客队", clientMean, len(clientScore), "进球", mainMean+ clientMean)

    # print("<= 1", round(main_0*client_0 + main_0*client_1 + main_1*client_0, 3))
    rate_1 = round(main_0*client_0 + main_0*client_1 + main_1*client_0, 3)
    rate_2 = round(rate_1 + main_0*client_2 + main_2*client_0, 3)
    rate_3 = round(rate_2 + main_0*client_3 + main_3*client_0 + main_1*client_2 + main_2*client_1, 3)
    print("<= 1", rate_1)
    print("<= 2", rate_2)
    print("<= 3", rate_3)

    # print("进球", round(sum(mainScore)/len(mainScore) + sum(clientScore)/len(clientScore) ,3))


def getResult_2(gameName, mainName, clientName, type):
    data = sql.queryTeamDataMain(gameName, mainName, "k_163")

    mainScore = []
    main_0_score = 0
    main_1_score = 0
    main_2_score = 0
    main_3_score = 0
    main_3_more_score = 0

    clientScore = []
    client_0_score = 0
    client_1_score = 0
    client_2_score = 0
    client_3_score = 0
    client_3_more_score = 0

    for one in data :
        main_score = int(one[2])
        client_score = int(one[3])

        rate_win = float(one[8])
        rate_lost = float(one[9])

        if type == 1 and rate_win > 2:
            continue
        elif type == 2 and rate_lost > 2:
            continue
        elif type == 3 and ((rate_win < 2) or (rate_lost < 2)):
            continue

        mainScore.append(main_score)
        if main_score == 0 :
            main_0_score += 1
        elif main_score == 1 :
            main_1_score += 1
        elif main_score == 2 :
            main_2_score += 1
        elif main_score == 3 :
            main_3_score += 1
        else :
            main_3_more_score += 1

    data = sql.queryTeamDataClient(gameName, clientName, "k_163")
    for one in data :
        main_score = int(one[2])
        client_score = int(one[3])

        rate_win = float(one[8])
        rate_lost = float(one[9])

        if type == 1 and rate_win > 2:
            continue
        elif type == 2 and rate_lost > 2:
            continue
        elif type == 3 and ((rate_win < 2) or (rate_lost < 2)):
            continue

        clientScore.append(client_score)
        if client_score == 0 :
            client_0_score += 1
        elif client_score == 1 :
            client_1_score += 1
        elif client_score == 2 :
            client_2_score += 1
        elif client_score == 3 :
            client_3_score += 1
        else :
            client_3_more_score += 1


    main_0 = 0
    main_1 = 0
    main_2 = 0
    main_3 = 0
    main_3_more = 0
    if len(mainScore) > 0 :
        main_0 = main_0_score / len(mainScore)
        main_1 = main_1_score / len(mainScore)
        main_2 = main_2_score / len(mainScore)
        main_3 = main_2_score / len(mainScore)
        main_3_more = main_3_more_score / len(mainScore)
    else :
        return

    client_0 = 0
    client_1 = 0
    client_2 = 0
    client_3 = 0
    client_3_more = 0
    if len(clientScore) > 0 :
        client_0 = client_0_score / len(clientScore)
        client_1 = client_1_score / len(clientScore)
        client_2 = client_2_score / len(clientScore)
        client_3 = client_3_score / len(clientScore)
        client_3_more = client_3_more_score / len(clientScore)
    else :
        return

    mainMean = round(sum(mainScore)/len(mainScore),3)
    clientMean = round(sum(clientScore)/len(clientScore),3)
    print("主队", mainMean, len(mainScore), "客队", clientMean, len(clientScore), "进球", mainMean+ clientMean)

    # print("<= 1", round(main_0*client_0 + main_0*client_1 + main_1*client_0, 3))
    rate_1 = round(main_0*client_0 + main_0*client_1 + main_1*client_0, 3)
    rate_2 = round(rate_1 + main_0*client_2 + main_2*client_0, 3)

    # print(main_0*client_3)
    # print(main_3, client_0, main_3*client_0)
    # print(main_1*client_2)
    # print(main_2, client_1, main_2*client_1)
    rate_3 = round(rate_2 + main_0*client_3 + main_3*client_0 + main_1*client_2 + main_2*client_1, 3)
    print("<= 1", rate_1)
    print("<= 2", rate_2)
    print("<= 3", rate_3)


def compare(name, main, clien, type):
    getResult_1(name, main, clien, type)
    getResult_2(name, main, clien, type)


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
# compare("国际A级")
# compare("世界杯欧洲预选赛")
# compare("澳A联")
# compare("西乙")
# compare("芬超")
# compare("瑞典甲")
# compare("巴乙")
# compare("爱超")
# compare("欧U21")
compare("巴乙", "维拉诺瓦", "塞阿拉", 1)
