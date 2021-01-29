
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#1. 데이터
dataset = load_boston()
x_train,x_test,y_train,y_test = train_test_split(dataset.data,dataset.target,train_size = 0.8, random_state = 33)

#2. 모델
model = DecisionTreeRegressor(max_depth = 4)

#3. 훈련
model.fit(x_train, y_train)

#4. 평가 예측
acc = model.score(x_test,y_test)

print(model.feature_importances_)
print('기존 acc : ', acc)
'''
def plot_feature_importances_dataset(model):
    n_features = dataset.data.shape[1]
    plt.barh(np.arange(n_features), model.feature_importances_, align = 'center')
    plt.yticks(np.arange(n_features), dataset.feature_names)
    plt.xlabel("Feature Importances")
    plt.ylabel("Features")
    plt.ylim(-1, n_features)

plot_feature_importances_dataset(model)
plt.show()
'''
####### 여기까지가 기존!!

####### 30개 동안 0이 아닌칼럼만 더해줌!!
####### 피쳐네임은 피쳐라는 리스트에 더해줌!!!
fi = model.feature_importances_
new_data = []
feature = []
for i in range(len(fi)):
    if fi[i] != 0:
        new_data.append(dataset.data[:,i])
        feature.append(dataset.feature_names[i])

new_data = np.array(new_data)
new_data = np.transpose(new_data)
x_train,x_test,y_train,y_test = train_test_split(new_data,dataset.target,train_size = 0.8, random_state = 33)

#2. 모델
model = DecisionTreeRegressor(max_depth = 4)

#3. 훈련
model.fit(x_train, y_train)

#4. 평가 예측
acc = model.score(x_test,y_test)

print(model.feature_importances_)
print('feature 제거 acc : ', acc)

####### dataset >> new_data 로 바꾸고 featurename 부분을 feature 리스트로 바꿔줌!!!
def plot_feature_importances_dataset(model):
    n_features = new_data.shape[1]
    plt.barh(np.arange(n_features), model.feature_importances_, align = 'center')
    plt.yticks(np.arange(n_features), feature)
    plt.xlabel("Feature Importances")
    plt.ylabel("Features")
    plt.ylim(-1, n_features)

plot_feature_importances_dataset(model)
plt.show()

# [0.03105639 0.         0.         0.         0.02383042 0.63787124
#  0.         0.10120718 0.         0.         0.00565641 0.
#  0.20037834]
# 기존 acc :  0.6604355946809267

# [0.03105639 0.02383042 0.63787124 0.10120718 0.00493084 0.20110392]
# feature 제거 acc :  0.6955033333974212