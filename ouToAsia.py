import time
import sys
for index in range(5):
    print('.', end=' ')
    sys.stdout.flush()
    time.sleep(1)

str = input("请输入：");

class ouToAsia:
    def __init__(self):
        self.map = {}
        self.map[1.13]=[0.75,-3]
        self.map[1.14]=[0.85,-3]
        self.map[1.15]=[0.9,-3]
        self.map[1.16]=[0.95,-3]
        self.map[1.17]=[1,-3]
        self.map[1.18]=[1.075,-3]

        self.map[1.19]=[0.925,-2.5]
        self.map[1.2]=[0.975,-2.5]
        self.map[1.21]=[1.025,-2.5]
        self.map[1.22]=[1.075,-2.5]

        self.map[1.23]=[0.9,-2]
        self.map[1.24]=[0.95,-2]
        self.map[1.25]=[1,-2]
        self.map[1.26]=[1.025,-2]
        self.map[1.27]=[1.075,-2]
        self.map[1.28]=[1.1,-2]

        self.map[1.29]=[0.875,-1.5]
        self.map[1.3]=[0.9,-1.5]
        self.map[1.31]=[0.925,-1.5]
        self.map[1.32]=[0.95,-1.5]
        self.map[1.33]=[0.975,-1.5]
        self.map[1.34]=[1.025,-1.5]
        self.map[1.35]=[1.05,-1.5]
        self.map[1.36]=[1.075,-1.5]
        self.map[1.37]=[1.1,-1.5]

        self.map[1.38]=[0.75,-1]
        self.map[1.39]=[0.775,-1]
        self.map[1.4]=[0.8,-1]
        self.map[1.41]=[0.825,-1]
        self.map[1.42]=[1.05,-1.25]
        self.map[1.43]=[0.85,-1]
        self.map[1.44]=[0.875,-1]
        self.map[1.45]=[0.9,-1]
        self.map[1.46]=[0.925,-1]
        self.map[1.48]=[0.95,-1]
        self.map[1.49]=[0.975,-1]
        self.map[1.5]=[1,-1]
        self.map[1.51]=[1.025,-1]
        self.map[1.53]=[1.05,-1]
        self.map[1.54]=[1.75,-1]
        self.map[1.55]=[1.1,-1]

        self.map[1.57]=[0.85,-0.75]
        self.map[1.58]=[0.875,-0.75]

        self.map[1.6]=[0.9,-0.75]
        self.map[1.62]=[0.925,-0.75]
        self.map[1.63]=[0.95,-0.75]
        self.map[1.65]=[0.975,-0.75]
        self.map[1.67]=[1,-0.75]
        self.map[1.68]=[1.025,-0.75]
        self.map[1.7]=[1.05,-0.75]
        self.map[1.72]=[1.075,-0.75]
        self.map[1.73]=[1.1,-0.75]

        self.map[1.75]=[0.75,-0.5]
        self.map[1.78]=[0.775,-0.5]
        self.map[1.8]=[0.8,-0.5]
        self.map[1.83]=[0.825,-0.5]
        self.map[1.85]=[0.825,-0.5]
        self.map[1.88]=[0.875,-0.5]
        self.map[1.9]=[0.9,-0.5]
        self.map[1.93]=[0.925,-0.5]
        self.map[1.95]=[0.95,-0.5]
        self.map[1.98]=[0.975,-0.5]
        self.map[2]=[1,-0.5]
        self.map[2.03]=[1.025,-0.5]
        self.map[2.05]=[1.05,-0.5]
        self.map[2.08]=[1.075,-0.5]
        self.map[2.1]=[1.1,-0.5]

        self.map[2.13]=[0.85,-0.25]
        self.map[2.17]=[0.875,-0.25]
        self.map[2.2]=[0.9,-0.25]
        self.map[2.23]=[0.925,-0.25]
        self.map[2.27]=[0.95,-0.25]
        self.map[2.3]=[0.975,-0.25]
        self.map[2.33]=[1,-0.25]
        self.map[2.37]=[1.025,-0.25]
        self.map[2.40]=[1.05,-0.25]
        self.map[2.43]=[1.075,-0.25]
        self.map[2.46]=[1.1,-0.25]

        self.map[2.5]=[0.75,0]
        self.map[2.55]=[0.775,0]
        self.map[2.6]=[0.8,0]
        self.map[2.65]=[0.825,0]
        self.map[2.7]=[0.85,0]
        self.map[2.75]=[0.875,0]
        self.map[2.8]=[0.9,0]
        self.map[2.85]=[0.925,0]
        self.map[2.9]=[0.95,0]
        self.map[2.95]=[0.975,0]
        self.map[3]=[1,0]
        self.map[3.05]=[1.025,0]
        self.map[3.1]=[1.05,0]
        self.map[3.15]=[1.075,0]
        self.map[3.2]=[1.1,0]

    def getRate(self, rate):
        reduce = 1.05
        return 1/(reduce*(1-1/(rate*reduce))) 

    def getData(self, rate):
        if rate < 1.3 or rate > 3.5:
            return None
        
        for i in range(5):
            rate = round((int(rate * 100) - 1)/100,2)
            if self.map.__contains__(rate) == True:
                return self.map[rate]

        return None

    

    def getRateResult(self, rate, main_score, client_score):
        data = self.getData(rate)
        if data == None:
            return None
            
        rate = data[0]    
        score = data[1]
        # score = 0

        score = (main_score - client_score) + score
        if score >= 1:
            return rate;
        elif score <= -1:
            return -1
        elif score == -0.75:
            return -1
        elif score == -0.5:
            return -1
        elif score == -0.25:
            return -0.5
        elif score == 0:
            return 0
        elif score == 0.25:
            return 0.5*rate
        elif score == 0.5:
            return rate
        elif score == 0.75:
            return rate
        else :
            return None

    def getWinResult(self, rate, main_score, client_score):
        # data = self.getData(rate)
        # if data == None:
        #     return None
            
        # rate = data[0]    
        # score = data[1]
        score = 0
        score = (main_score - client_score) + score
        if score > 0:
            return 1;
        if score < 0:
            return -1;
        else:
            return 0