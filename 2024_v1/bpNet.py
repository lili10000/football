import numpy as np
import matplotlib.pyplot as plt
import os
import json
import torch
import torch.nn.functional as Fun
 
#设置超参数
lr=0.02 #学习率
epochs=300 #训练轮数
n_feature=3 #输入特征
n_hidden=20 #隐层节点数
n_output=3 #输出(鸢尾花三种类别)
 

paramsList = []

#1.准备数据
path = os.path.dirname(__file__)
file = "{}\\data\\2.json".format(path)

with open(file, 'r',encoding='utf-8') as f:
    data = f.read()
    tmpList = json.loads(data)
    for result in tmpList:
        input = torch.tensor([float(result["o_home"]), float(result["o_stand"]), float(result["o_guest"])])
        output = torch.tensor([float(result["y_goal"]), float(result["y_up"]), float(result["y_down"])])
        paramsList.append([input, output])




# #将数据类型转换为tensor方便pytorch使用
# x_train=torch.FloatTensor(x_train)
# y_train=torch.LongTensor(y_train)
# x_test=torch.FloatTensor(x_test)
# y_test=torch.LongTensor(y_test)
 
#2.定义BP神经网络
class BPNetModel(torch.nn.Module):
    def __init__(self,n_feature,n_hidden,n_output):
        super(BPNetModel, self).__init__()
        self.hiddden=torch.nn.Linear(n_feature,n_hidden)#定义隐层网络
        self.out=torch.nn.Linear(n_hidden,n_output)#定义输出层网络
    def forward(self,x):
        x=Fun.relu(self.hiddden(x)) #隐层激活函数采用relu()函数
        out=Fun.softmax(self.out(x),dim=1) #输出层采用softmax函数
        return out
#3.定义优化器和损失函数
net=BPNetModel(n_feature=n_feature,n_hidden=n_hidden,n_output=n_output) #调用网络
optimizer=torch.optim.Adam(net.parameters(),lr=lr) #使用Adam优化器，并设置学习率
loss_fun=torch.nn.CrossEntropyLoss() #对于多分类一般使用交叉熵损失函数
 
#4.训练数据
loss_steps=np.zeros(epochs) #构造一个array([ 0., 0., 0., 0., 0.])里面有epochs个0
accuracy_steps=np.zeros(epochs)
 
for epoch in range(epochs):
    for param in paramsList:
        x_train = param[0]
        y_train = param[1]

        y_pred=net(x_train) #前向传播
        loss=loss_fun(y_pred,y_train)#预测值和真实值对比
        optimizer.zero_grad() #梯度清零
        loss.backward() #反向传播
        optimizer.step() #更新梯度
        loss_steps[epoch]=loss.item()#保存loss
        running_loss = loss.item()
        print(f"第{epoch}次训练，loss={running_loss}".format(epoch,running_loss))
        with torch.no_grad(): #下面是没有梯度的计算,主要是测试集使用，不需要再计算梯度了
            x_test = x_train
            y_test = y_train

            y_pred=net(x_test)
            correct=(torch.argmax(y_pred,dim=1)==y_test).type(torch.FloatTensor)
            accuracy_steps[epoch]=correct.mean()
            print("测试鸢尾花的预测准确率", accuracy_steps[epoch])
 
#print("测试鸢尾花的预测准确率",accuracy_steps[-1])
 
#5.绘制损失函数和精度
fig_name="Iris_dataset_classify_BPNet"
fontsize=15
fig,(ax1,ax2)=plt.subplots(2,figsize=(15,12),sharex=True)
ax1.plot(accuracy_steps)
ax1.set_ylabel("test accuracy",fontsize=fontsize)
ax1.set_title(fig_name,fontsize="xx-large")
ax2.plot(loss_steps)
ax2.set_ylabel("train lss",fontsize=fontsize)
ax2.set_xlabel("epochs",fontsize=fontsize)
plt.tight_layout()
plt.savefig(fig_name+'.png')
plt.show()
 
 
 