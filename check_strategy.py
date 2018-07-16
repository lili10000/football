# encoding=utf8

class data():
    def __init__(self, time=0, score = 0, small_do ="", else_do=""):
        self.time = time
        self.score = score
        self.small_do = small_do
        self.else_do = else_do
        

class checkStartegy():
    def __init__(self):
        self.startegy = {}

        self.startegy['泰乙']=data(time=80,score=2,small_do="",else_do="买大球")
        self.startegy['美乙']=data(time=80,score=2,small_do="",else_do="买大球")
        self.startegy['瑞典超']=data(time=80,score=2,small_do="",else_do="买大球")
        self.startegy['哈萨甲']=data(time=80,score=2,small_do="",else_do="买大球")
        self.startegy['里约足联B']=data(time=80,score=2,small_do="",else_do="买大球")
        self.startegy['日联杯']=data(time=80,score=2,small_do="",else_do="买大球")  
        self.startegy['越VL']=data(time=80,score=2,small_do="",else_do="买大球")  

        self.startegy['哈萨超']=data(time=80,score=0,small_do="",else_do="买大球")
        self.startegy['美职联']=data(time=80,score=0,small_do="",else_do="买大球")
        self.startegy['天皇杯']=data(time=80,score=0,small_do="",else_do="买大球")



        # 黑名单就是啥也不干
        blackList = data(time=80,score=0,small_do="",else_do="") 
        self.startegy['日足联']=blackList
        self.startegy['赞比亚超']=blackList
        self.startegy['巴圣SB']=blackList
        self.startegy['挪丙2']=blackList
        self.startegy['挪乙1']=blackList
        self.startegy['拉脱V']=blackList
        self.startegy['韩国K2']=blackList
        self.startegy['韩K联']=blackList
        
        

    def check(self,type='',score=0,time=0):
        if self.startegy.__contains__(type) == False:
            return 
        tmp = self.startegy[type]
        if time < tmp.time:
            return ""
        if score < tmp.score:
            return tmp.small_do
        else:
            return tmp.else_do


