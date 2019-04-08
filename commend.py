# encoding=utf8
from db.mysql import sqlMgr

class commend:
    def __init__(self):
        self.sql = sqlMgr('localhost', 'root', '861217', 'football')
        self.key = "k_commend"
        self.CornerKey = "角"
        self.ScoreKey = "球"
        self.rateKey = "让"

    def __insertData(self,id, type, info, logInfo):

        retn = self.sql.queryCountByID(self.key, id, type)
        if retn == None or retn[0][0] == 0:
            with open(r"buyPerDay.txt", 'a') as f:
                logInfo = "{}   {}\n".format(id, logInfo)
                f.write(logInfo)
                print(logInfo)
            self.sql.insert(info, self.key)

    def add(self, main, time, type, version=0, rate=None, logInfo="", id=""):
        buyBig = -1
        if "大" in type or "胜" in type:
            buyBig = 1
        elif "小" in type or "负" in type:
            buyBig = -1


        if self.CornerKey in type:
            type = self.CornerKey
        elif self.ScoreKey in type:
            type = self.ScoreKey
        elif self.rateKey in type:
            type = self.rateKey
        else:
            return


        id_key = "{}_{}_{}".format(main, id, type)


        info = "'{}', '{}', '{}','{}','{}', '{}'".format(id_key, time, type, buyBig, 0, version)
        self.__insertData(id_key, type, info, logInfo)

        if (rate != None) and ("让" in type):
            if rate == "-" or rate == "-\n" :
                return
            rate = float(rate)

            id_key = "{}_{}_{}".format(main, id, self.ScoreKey)

            if (rate < 0 and buyBig == 1) or  (rate > 0 and buyBig == -1): # 买强队赢买大
                info = "'{}', '{}', '{}','{}','{}', '{}'".format(id_key, time, self.ScoreKey, 1, 0, version)
                logInfo = logInfo.replace("让胜", "大球")
                logInfo = logInfo.replace("让输", "大球")
                self.__insertData(id_key, type, info, logInfo)

            if (rate < 0 and buyBig == -1) or  (rate > 0 and buyBig == 1): # 买弱队赢买小
                info = "'{}', '{}', '{}','{}','{}', '{}'".format(id_key, time, self.ScoreKey, -1, 0, version)
                logInfo = logInfo.replace("让胜", "小球")
                logInfo = logInfo.replace("让输", "小球")
                self.__insertData(id_key, type, info, logInfo)



    def check(self, main, time, main_score, client_score, rate, scoreRate, corner=0, cornerRate=0,  id=0):
        time = int(time / 10000)
        time = str(time) + '....' 


        def checkRate(main, main_score, client_score,rate, id):
            type = self.rateKey
            id = "{}_{}_{}".format(main, id, type)

            retn = self.sql.queryCountByID(self.key, id, type)
            if retn == None or retn[0][0] == 0:
                return
        
            rateResult = 0
            if main_score - client_score + float(rate) > 0:
                rateResult = 1
            elif main_score - client_score + float(rate)  < 0:
                rateResult = -1
            else:
                return

            retn = self.sql.queryById(self.key, id)
            rateResult = rateResult * retn[0][3]
            self.sql.updateCommend(id, type, rateResult, self.key)

        def checkScore(main_score, client_score, scoreRate, id):
            if scoreRate == "-":
                return
            scoreRate = float (scoreRate)

            type = self.ScoreKey
            id = "{}_{}_{}".format(main, id, type)
            retn = self.sql.queryCountByID(self.key, id, type)
            if retn == None or retn[0][0] == 0:
                return
        
            rateResult = 0
            if main_score + client_score - scoreRate > 0:
                rateResult = 1
            elif main_score + client_score - scoreRate < 0:
                rateResult = -1
            else:
                return
            retn = self.sql.queryById(self.key, id)
            rateResult = rateResult * retn[0][3]
            self.sql.updateCommend(id, type, rateResult, self.key)
        
        def checkCorner(main, time, corner, cornerRate, id):
            if cornerRate == "-":
                return
            cornerRate = float (cornerRate)

            type = self.CornerKey

            id = "{}_{}_{}".format(main, id, type)
            retn = self.sql.queryCountByID(self.key, id, type)
            if retn == None or retn[0][0] == 0:
                return
        
            rateResult = 0
            if corner - cornerRate > 0:
                rateResult = 1
            elif corner - cornerRate < 0:
                rateResult = -1
            else:
                return
            retn = self.sql.queryById(self.key, id)
            rateResult = rateResult * retn[0][3]
            self.sql.updateCommend(id, type, rateResult, self.key)


        checkRate(main, main_score, client_score,rate, id)
        checkScore(main_score, client_score, scoreRate, id)
        checkCorner(main, time, corner, cornerRate, id)
        




