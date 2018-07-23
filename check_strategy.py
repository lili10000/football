# encoding=utf8
import pymysql as MySQLdb 

class data():
    def __init__(self, time=0, score = 0, small_do ="", else_do=""):
        self.time = time
        self.score = score
        self.small_do = small_do
        self.else_do = else_do
        

class checkStartegy():
    def __init__(self):

        self.db = MySQLdb.connect('localhost', 'root', '861217', 'football', charset="utf8")
        self.cursor = self.db.cursor()
        self.updataStartegy()
        
    def updataStartegy(self):
        SQL = u"select * from k_startegy "
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
            time = obj[1] 
            score = obj[2]
            small_do = obj[3]
            else_do = obj[4]
            self.startegy[type] = data(time=time,score=score,small_do=small_do,else_do=else_do)

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


