# %matplotlib inline
import torch
from IPython import display
from matplotlib import pyplot as plt
import numpy as np
import random
import pandas as pd
from torch.nn import  init
from torch import nn

torch.set_default_tensor_type(torch.FloatTensor)

def prework(datas, labels):
    num = int(datas.shape[1] / 400)
    trainnum = int(num * 3 / 4)
    testnum = num - trainnum

    labels_train = [labels for i in range(trainnum)]
    labels_test = [labels for i in range(testnum)]
    labels_train = torch.tensor(labels_train)
    labels_test = torch.tensor(labels_test)

    features_train = None
    features_test = None


    for i in range(0, trainnum):
        features_part = datas[0][i*400:i*400+400].reshape(1, 400)
        if features_train is None:
            features_train = features_part
        else:
            features_train = torch.cat((features_train, features_part), dim = 0)
    for i in range(0, testnum):
        features_part = datas[0, trainnum*400+i*400:trainnum*400+i*400+400].reshape(1, 400)
        if features_test is None:
            features_test = features_part
        else:
            features_test = torch.cat((features_test, features_part), dim = 0)
    # print(features_train.shape, labels_train.shape, features_test.shape, labels_test.shape)
    return features_train, labels_train, features_test, labels_test

def to_one_hot(label):
    a = [1 if i == label else 0 for i in range(0, 7)]
    return a

def dataframe_to_tensor(datas):
    x = datas['0']
    x = np.array(x)
    x = x.tolist()
    x = torch.unsqueeze(torch.FloatTensor(x), dim=0)
    return x

data_normal = pd.read_csv(r"D:\PythonProject\MachineErrorDetector\Dataset\haveprocessed\normal.csv")
data_DE_gd = pd.read_csv(r"D:\PythonProject\MachineErrorDetector\Dataset\haveprocessed\DE_gd.csv")
data_DE_in = pd.read_csv(r"D:\PythonProject\MachineErrorDetector\Dataset\haveprocessed\DE_in.csv")
data_DE_out = pd.read_csv(r"D:\PythonProject\MachineErrorDetector\Dataset\haveprocessed\DE_out.csv")
data_FE_gd = pd.read_csv(r"D:\PythonProject\MachineErrorDetector\Dataset\haveprocessed\FE_gd.csv")
data_FE_in = pd.read_csv(r"D:\PythonProject\MachineErrorDetector\Dataset\haveprocessed\FE_in.csv")
data_FE_out = pd.read_csv(r"D:\PythonProject\MachineErrorDetector\Dataset\haveprocessed\FE_out.csv")

features_train = []
features_test = []
labels_train = []
labels_test = []

def MakeData():
    a = dataframe_to_tensor(data_normal)
    a = list(prework(dataframe_to_tensor(data_normal), 0))
    features_train = np.array(a[0])
    labels_train = np.array(a[1])
    features_test = np.array(a[2])
    labels_test = np.array(a[3])
    b = dataframe_to_tensor(data_DE_gd)
    b = list(prework(dataframe_to_tensor(data_DE_gd), 1))
    c = dataframe_to_tensor(data_DE_in)
    c = list(prework(dataframe_to_tensor(data_DE_in), 2))
    d = dataframe_to_tensor(data_DE_out)
    d = list(prework(dataframe_to_tensor(data_DE_out), 3))
    e = dataframe_to_tensor(data_FE_gd)
    e = list(prework(dataframe_to_tensor(data_FE_gd), 4))
    f = dataframe_to_tensor(data_FE_in)
    f = list(prework(dataframe_to_tensor(data_FE_in), 5))
    g = dataframe_to_tensor(data_FE_out)
    g = list(prework(dataframe_to_tensor(data_FE_out), 6))
    features_train = np.concatenate([features_train, b[0], c[0], d[0], e[0], f[0], g[0]], axis = 0)
    labels_train = np.concatenate([labels_train, b[1], c[1], d[1], e[1], f[1], g[1]], axis = 0)
    features_test = np.concatenate([features_test, b[2], c[2], d[2], e[2], f[2], g[2]], axis = 0)
    labels_test = np.concatenate([labels_test, b[3], c[3], d[3], e[3], f[3], g[3]], axis = 0)
    features_train = torch.from_numpy(features_train)
    features_test = torch.from_numpy(features_test)
    labels_train = torch.from_numpy(labels_train)
    labels_test = torch.from_numpy(labels_test)
    return features_train, labels_train, features_test, labels_test

a = list(MakeData())
features_train = a[0]
labels_train = a[1]
features_test = a[2]
labels_test = a[3]
print(features_train.shape)
print(labels_train.shape)
print(features_test.shape)
print(labels_test.shape)

class LinearNet(nn.Module):
    def __init__(self):
        super(LinearNet, self).__init__()
        self.linear1 = torch.nn.Linear(400, 256)
        # self.linear2 = torch.nn.Linear(512, 256)
        self.linear3 = torch.nn.Linear(256, 7)
        self.act = nn.ReLU()
    def forward(self, x):
        y = self.act(self.linear1(x))
        # y = self.act(self.linear2(y))
        y = self.act(self.linear3(y))
        return y

net = LinearNet()

for name, param in net.named_parameters():
    if 'weight' in name:
        init.normal_(param, mean = 0, std = 0.01)

batch_size = 512
num_epoches = int(features_train.shape[0] / batch_size)
train_dataset = torch.utils.data.TensorDataset(features_train, labels_train)
train_iter = torch.utils.data.DataLoader(train_dataset, batch_size, shuffle=True)
test_dataset = torch.utils.data.TensorDataset(features_test, labels_test)
test_iter = torch.utils.data.DataLoader(test_dataset, batch_size, shuffle=True)


loss = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(params = net.parameters(), lr = 1)

def evaluate(data_iter, net) :
    acc_sum, n = 0.0, 0.0
    for x, y in data_iter:
        acc_sum += (net(x).argmax(dim= 1) == y).float().sum().item()
        n += x.shape[0]
    return acc_sum / n

for epoch in range(num_epoches):
    train_l_sum = 0.0
    test_acc = 0.0
    train_acc_sum = 0.0
    n = 0.0
    for x, y in train_iter:
        y_hat = net(x)
        l = loss(y_hat, y).sum()
        optimizer.zero_grad()
        l.backward()
        optimizer.step()

        train_l_sum += l.item()
        train_acc_sum += (y_hat.argmax(dim = 1) == y).sum().item()
        n += x.shape[0]
        test_acc = evaluate(test_iter, net)
    print('epoch %d, loss %f, train_acc %f, test_acc %f' % (epoch, train_l_sum / n, train_acc_sum / n, test_acc))