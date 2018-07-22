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

        self.startegy['西澳U20']=data(time=timeCheck,score=3,small_do="",else_do="买大球")
        
        self.startegy['美乙']=data(time=timeCheck,score=2,small_do="",else_do="买大球")
        self.startegy['哈萨甲']=data(time=timeCheck,score=2,small_do="",else_do=">2.5 买大球")
        self.startegy['里约足联B']=data(time=timeCheck,score=2,small_do="",else_do="买大球")
         
        self.startegy['越VL']=data(time=timeCheck,score=2,small_do="",else_do="买大球")  
        self.startegy['韩甲挑']=data(time=timeCheck,score=2,small_do="",else_do="买大球")  
        self.startegy['智利乙']=data(time=timeCheck,score=2,small_do="",else_do="买大球") 
        self.startegy['俄甲']=data(time=timeCheck,score=2,small_do="",else_do="买大球")   
        self.startegy['南俱杯']=data(time=timeCheck,score=2,small_do="",else_do="买大球") 
        self.startegy['澳昆士兰']=data(time=timeCheck,score=2,small_do="",else_do="买大球") 
        self.startegy['西澳超']=data(time=timeCheck,score=2,small_do="",else_do="买大球") 
        self.startegy['澳塔超']=data(time=timeCheck,score=2,small_do="",else_do="买大球") 
        self.startegy['澳新联2']=data(time=timeCheck,score=2,small_do="",else_do="买大球") 
        self.startegy['澳维超2']=data(time=timeCheck,score=2,small_do="",else_do="买大球") 
        self.startegy['澳布甲']=data(time=timeCheck,score=2,small_do="",else_do="买大球") 



        self.startegy['冰岛女甲']=data(time=timeCheck,score=2,small_do="买小球",else_do="买大球")  
        self.startegy['墨女超']=data(time=timeCheck,score=2,small_do="买小球",else_do="买大球")  
        self.startegy['印IFA盾']=data(time=timeCheck,score=2,small_do="",else_do="买大球")  

        self.startegy['韩国女K']=data(time=timeCheck,score=1,small_do="",else_do="买大球") 
        self.startegy['南澳女超']=data(time=timeCheck,score=1,small_do="",else_do="买大球")  
    
        self.startegy['瑞典北甲']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['哈萨超']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['美职联']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['天皇杯']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['爱沙杯']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['菲足联']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['澳维女超']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['澳西甲']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['泰D3']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['奥地利杯']=data(time=timeCheck,score=0,small_do="",else_do="买大球")
        self.startegy['马来F杯']=data(time=timeCheck,score=0,small_do="",else_do="买大球")


        self.startegy['南澳州联1']=data(time=75,score=0,small_do="",else_do="买大球")
        self.startegy['英友谊']=data(time=75,score=0,small_do="",else_do="买大球")
          
        self.startegy['苏联杯']=data(time=75,score=3,small_do="买小球",else_do="")
        self.startegy['阿根廷杯']=data(time=75,score=3,small_do="买小球",else_do="")
        
        self.startegy['日联杯']=data(time=timeCheck,score=2,small_do="",else_do="买大球") 

        # 白名单就是买小
        whiteList = ['日职乙','中甲','泰超']
        for key in whiteList:
            self.startegy[key]=data(time=75,score=0 ,small_do=" 白名单",else_do="白名单") 
        
        # 黑名单就是啥也不干
        black = ['日职联','墨秋联','澳威北超','南澳超','澳新女','日女挑联','欧洲友谊'
        ,'日职丙','新加坡联','奥地利A杯','捷U21','马来超','丹超','白俄后','泰乙']
        blackList = data(time=timeCheck,score=0,small_do="",else_do="") 
        for key in black:
            self.startegy[key]=blackList

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
        self.startegy['越V2联']=blackList
        self.startegy['斐济杯']=blackList
        self.startegy['印尼L2']=blackList
        self.startegy['加尔联']=blackList
        self.startegy['澳维超']=blackList
        self.startegy['巴西乙']=blackList
        self.startegy['智利甲']=blackList
        self.startegy['澳昆U20']=blackList
        self.startegy['澳布超后']=blackList
        self.startegy['中甲']=blackList
        self.startegy['澳洲特区超']=blackList
        self.startegy['捷2L']=blackList
        self.startegy['澳亚布超']=blackList
        
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


