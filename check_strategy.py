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
        timeCheck = 80

        self.startegy['泰乙']=data(time=timeCheck,score=2,small_do="",else_do="买大球")
        self.startegy['美乙']=data(time=timeCheck,score=2,small_do="",else_do="买大球")
        self.startegy['哈萨甲']=data(time=timeCheck,score=2,small_do="",else_do="买大球")
        self.startegy['里约足联B']=data(time=timeCheck,score=2,small_do="",else_do="买大球")
        self.startegy['日联杯']=data(time=timeCheck,score=2,small_do="",else_do="买大球")  
        self.startegy['越VL']=data(time=timeCheck,score=2,small_do="",else_do="买大球")  
        self.startegy['韩甲挑']=data(time=timeCheck,score=2,small_do="",else_do="买大球")  
        self.startegy['冰岛女甲']=data(time=timeCheck,score=2,small_do="买小球",else_do="买大球")  

        self.startegy['智利乙']=data(time=timeCheck,score=2,small_do="",else_do="买大球") 
        self.startegy['俄甲']=data(time=timeCheck,score=2,small_do="",else_do="买大球")   
         
        self.startegy['墨女超']=data(time=timeCheck,score=2,small_do="买小球",else_do="买大球")  
        self.startegy['印IFA盾']=data(time=timeCheck,score=2,small_do="",else_do="买大球")  

        self.startegy['韩国女K']=data(time=timeCheck,score=1,small_do="",else_do="买大球")  


        self.startegy['瑞典北甲']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['哈萨超']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['美职联']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['天皇杯']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['爱沙杯']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        
        self.startegy['英友谊']=data(time=75,score=0,small_do="",else_do="买大球")
        
        self.startegy['中甲']=data(time=80,score=2,small_do="买小球",else_do="")
        self.startegy['苏联杯']=data(time=80,score=3,small_do="买小球",else_do="")
        self.startegy['阿根廷杯']=data(time=80,score=3,small_do="买小球",else_do="")
        

        # 黑名单就是啥也不干
        blackList = data(time=timeCheck,score=0,small_do="",else_do="") 

        self.startegy['日职丙']=blackList
        self.startegy['日足联']=blackList
        self.startegy['赞比亚超']=blackList
        self.startegy['巴圣SB']=blackList
        self.startegy['挪丙2']=blackList
        self.startegy['挪乙1']=blackList
        self.startegy['拉脱V']=blackList
        self.startegy['韩国K2']=blackList
        self.startegy['韩K联']=blackList
        self.startegy['印尼超']=blackList
        self.startegy['新加坡U19']=blackList
        self.startegy['瑞典超']=blackList
        self.startegy['欧锦赛 U19']=blackList
        self.startegy['丹超']=blackList
        self.startegy['冰岛超']=blackList
        self.startegy['厄瓜锦']=blackList
        self.startegy['欧罗巴']=blackList
	self.startegy['印尼杯']=blackList
	self.startegy['中超']=blackList

        
        
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


