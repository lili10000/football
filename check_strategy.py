# encoding=utf8
import pymysql as MySQLdb 

class data():
    def __init__(self, time=0, score = 0, small_do ="", else_do=""):
        self.time = time
        self.score = score
        self.small_do = small_do
        self.else_do = else_do

class data_v2():
    def __init__(self, rate=0, score = 0, small_do ="", else_do=""):
        self.rate = rate
        self.score = score
        self.small_do = small_do
        self.else_do = else_do

class checkStartegy():
    def __init__(self):

        self.db = MySQLdb.connect('localhost', 'root', '861217', 'football', charset="utf8")
        self.cursor = self.db.cursor()
        self.updataStartegy()
        self.blackList = self.initBlackList()
        
    def initBlackList(self):
        blackList = []
        blackList.extend(['巴','澳','新','美','国际','英U23发展','苏格兰后备','比利时后','英超2','荷后备','墨女超','波兰乙','友谊'])


        return blackList


    def updataStartegy(self):
        # SQL = u"select * from k_startegy "
        SQL = u"select * from k_startegy_v2 "
        SQL.encode('utf-8')
        try:  
            self.cursor.execute(SQL)
            self.results = self.cursor.fetchall()
        except Exception as e:
            print( repr(e))
            return

        self.startegy = {}
        for obj in self.results:        
            type = str(obj[0])
            rate = obj[1] 
            score = obj[2]
            small_do = obj[3]
            else_do = obj[4]
            self.startegy[type] = data_v2(rate=rate,score=score,small_do=small_do,else_do=else_do)

    def check(self,type='',score=0,time=0):
        
        self.updataStartegy()
        if self.startegy.__contains__(type) == False:
            return
        tmp = self.startegy[type]
        if time < tmp.time:
            return ""
        if score < tmp.score:
            return tmp.small_do
        else:
            return tmp.else_do

    def check_v2(self,type='',score=0, rate=0):
        self.updataStartegy()
        if self.startegy.__contains__(type) == False:
            return
        tmp = self.startegy[type]

        if score >= tmp.score:
            return ''
        if rate - score < tmp.rate:
            return tmp.small_do
        else:
            return tmp.else_do

    def check_v3(self,type=''):
        for blackName in self.blackList:
            if blackName in type:
                return True
        return False