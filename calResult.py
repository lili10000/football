from db.mysql import sqlMgr
import time

sql = sqlMgr('localhost', 'root', '861217', 'football')
data = sql.queryByTypeAll("k_commend")
total = 0
# size = len(data)
size = 0
# print("size:",size)
winBig = 0
oneWin = 0

check = 0
checkSize = 0
info = {}
orInfo = {}
checkInfo = {}
normal = 0
normalSize = 0
for one in data:
    result = one[5]
    type = one[3]
    id = one[0]
    total += result

    if not info.__contains__(type) :
        info[type] = 0
        orInfo[type] = 0
        checkInfo[type] = [0,0,0,0]
    orInfo[type] += 1

    if result == 3:
        winBig += 1
    elif result == 1:
        oneWin += 1
    # elif result < 0:
    #     pass
    # else:
    #     continue
    # if type 

    size += 1

    # if "小" in type:
    winFlag = False
    bigFlag = False
    if "大" in type:
        bigFlag = True
    if "赢" in type:
        winFlag = True
    #     continue

    # checkSize += 1
    id = id[:-3]
    # id = "{}_{}".format(tmpList[1],tmpList[1])

    datas = sql.queryByGameId("k_corner", id)
    if len(datas) == 0:
        continue
    mainScore = datas[0][2]
    clientScore = datas[0][3]
    rateScore = float(datas[0][11])
    dan = ((mainScore + clientScore)%2 == 1)
    dou = (mainScore*clientScore != 0)

    if dan:
        checkInfo[type][0] += 1
    else:
        checkInfo[type][1] += 1
    
    if dou:
        checkInfo[type][2] += 1
    else:
        checkInfo[type][3] += 1

    if bigFlag == False:
        continue

    # checkBig = (bigFlag and dou) or (bigFlag == False and dou == False)
    checkBig = (bigFlag and dou) 
    if checkBig:
        normal += 1
        normalSize += 1
    elif mainScore + clientScore - rateScore == 0:
        pass
    else:
        normal -= 1

    # if (bigFlag and winFlag and dan ) or (bigFlag == False  and winFlag == False and dan == False):
    #     normal += 1
    #     normalSize += 1
    # else:
    #     normal -= 1


    # checkWin = (winFlag and (mainScore - clientScore + rateScore) > 0) or (bigFlag == False and (mainScore - clientScore + rateScore) < 0)
    # if checkWin:
    #     normal += 1
    # elif mainScore - clientScore + rateScore == 0:
    #     pass
    # else:
    #     normal -= 1


    # if dou and dan == False:
    #     check += 2
    #     checkSize += 1
    # else:
    #     check -= 1
    
    condi_1 = not dan
    condi_2 = dou


    # condi_1 = False
    # condi_2 = False

    # if "赢大" in type:
    #     condi_1 = dan
    #     condi_2 = dou
    # elif "赢小" in type:
    #     condi_1 = not dan
    #     condi_2 = not dou
    # elif "输大" in type:
    #     condi_1 = dan
    #     condi_2 = dou
    # elif "输小" in type:
    #     condi_1 = not dan
    #     condi_2 = not dou


    if condi_1:
        check += 1
        checkSize += 1
        info[type] += 1
    else:
        check -= 1
        info[type] -= 1

    if condi_2:
        check += 1
        checkSize += 1
        info[type] += 1
    else:
        check -= 1
        info[type] -= 1
    
    # if checkBig:
    #     check += 1
    # else:
    #     check -= 1


print(size, checkSize, "check:", check, round(checkSize/size, 2))
# print(orInfo)
outInfo = ""
for key in orInfo:
    outInfo += "{}  {}  ".format(key, round(orInfo[key]/size, 2))

print(outInfo)

outInfo = ""
for key in info:
    outInfo += "{}  {}  ".format(key, round(info[key]/check, 2))

print(outInfo)
# print(checkInfo)
print(normal, normalSize)
# print(size, total, round(total/(1*size), 2), "双胜",winBig,round(winBig/size, 2), "单胜",oneWin, round(oneWin/size, 2))   
# print(size, total, round(total/size, 2), "赢大",winBig,round(winBig/size, 2), "单胜",oneWin, round(oneWin/size, 2))