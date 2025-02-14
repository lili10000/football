from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import ExtraTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.model_selection import train_test_split
import json
import os
import numpy as np

inputList = []
outputList = []

#1.准备数据
path = os.path.dirname(__file__)
file = "{}\\data\\36.json".format(path)
with open(file, 'r',encoding='utf-8') as f:
    data = f.read()
    tmpList = json.loads(data)
    for result in tmpList:
        input = [float(result["o_home"]), float(result["o_stand"]), float(result["o_guest"])]
        # output = [float(result["y_goal"])]
        output = [float(result["score_goal"])]
        inputList.append(input)
        outputList.append(output)

a=np.array(inputList)
b=np.array(outputList)

x_train,x_test,y_train,y_test = train_test_split(a,b,test_size=0.2)


clf = Ridge() # good
rf = clf.fit (x_train, y_train.ravel())
y_pred = rf.predict(x_test)
# print(y_pred)

print("结果如下：")
print("训练集分数：",rf.score(x_train,y_train))
print("验证集分数：",rf.score(x_test,y_test))
