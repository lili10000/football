# encoding=utf8
from db.mysql import sqlMgr

class commend:
    def __init__(self):
        self.sql = sqlMgr('localhost', 'root', '861217', 'football')
        self.key = "k_commend"
        self.CornerKey = "角"
        self.ScoreKey = "球"
        self.rateKey = "让"

    def add(self, main, time, type):
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

        id = "{}_{}_{}".format(main, time, type)


        info = "'{}', '{}', '{}','{}','{}'".format(id, time, type, buyBig, 0)
        self.sql.insert(info, self.key)

    def check(self, main, time, main_score, client_score, rate, scoreRate, corner=0, cornerRate=0):
        def checkRate(main, main_score, client_score,rate):
            type = self.rateKey
            id = "{}_{}_{}".format(main, time,type)
            retn = self.sql.queryCountByID(self.key, id, type)
            if retn == None or retn[0][0] == 0:
                return
        
            rateResult = 0
            if main_score - client_score + rate > 0:
                rateResult = 1
            elif main_score - client_score + rate < 0:
                rateResult = -1
            else:
                return
            self.sql.updateCommend(id, type, rateResult, self.key)

        def checkScore(main_score, client_score, scoreRate):
            if scoreRate == "-":
                return
            scoreRate = float (scoreRate)

            type = self.ScoreKey
            id = "{}_{}_{}".format(main, time,type)
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
            self.sql.updateCommend(id, type, rateResult, self.key)
        
        def checkCorner(main, time, corner, cornerRate):
            if cornerRate == "-":
                return
            cornerRate = float (cornerRate)

            type = self.CornerKey
            id = "{}_{}_{}".format(main, time,type)
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
            self.sql.updateCommend(id, type, rateResult, self.key)


        checkRate(main, main_score, client_score,rate)
        checkScore(main_score, client_score, scoreRate)
        checkCorner(main, time, corner, cornerRate)
        




