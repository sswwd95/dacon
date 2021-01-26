# 실습 다:다 앙상블을 구현하시오.


import numpy as np

#1. 데이터
x1 = np.array([range(100), range(301, 401), range(1,101)])
y1 = np.array([range(711,811),range(1,101), range(201,301)])

x2 = np.array([range(101,201), range(411,511),range(100,200)])
y2 = np.array([range(501,601), range(711,811), range(100)])
y3 = np.array([range(601,701), range(811,911), range(1100,1200)])

x1 = np.transpose(x1)
x2 = np.transpose(x2)
y1 = np.transpose(y1)
y2 = np.transpose(y2)
y3 = np.transpose(y3)


# shape 전부다 100행 3열

from sklearn.model_selection import train_test_split
x1_train, x1_test, y1_train, y1_test, x2_train, x2_test, y2_train, y2_test, y3_train, y3_test= train_test_split (
    x1, x2, y1, y2, y3, shuffle = False, train_size=0.8)

# 2. 모델구성
from tensorflow.keras.models import Sequential, Model
# from tensorflow.keras.layers import Dense, LSTM, Conv2D
from tensorflow.keras.layers import Dense, Input

# 모델1
input1 = Input(shape=(3,))
dense1 = Dense(10,activation='relu')(input1)
dense1 = Dense(5, activation='relu')(dense1)
# output1 = Dense(3)(dense1)

# 모델2
input2 = Input(shape=(3,))
dense2 = Dense(10,activation='relu')(input2)
dense2 = Dense(5, activation='relu')(dense2)
dense2 = Dense(5, activation='relu')(dense2)
dense2 = Dense(5, activation='relu')(dense2)
# output2 = Dense(3)(dense2)

# 모델 병합 / concatenate
from tensorflow.keras.layers import concatenate, Concatenate

merge1 = concatenate([dense1, dense2]) # 제일 끝의 dense 변수명 넣기
middle1 = Dense(30)(merge1)
middle1 = Dense(10)(middle1)
middle1 = Dense(10)(middle1)

# 모델 분기1
output1 = Dense(30)(middle1)
output1 = Dense(7)(output1)
output1 = Dense(3)(output1)

# 모델 분기2
output2 = Dense(15)(middle1)
output2 = Dense(7)(output2)
output2 = Dense(7)(output2)
output2 = Dense(3)(output2)

# 모델 분기3
output3 = Dense(15)(middle1)
output3 = Dense(7)(output3)
output3 = Dense(7)(output3)
output3 = Dense(3)(output3)

# 모델 선언
model = Model(inputs=[input1, input2],
              outputs=[output1, output2, output3])
              # 두개 묶어줄 때는 list [ ] 사용

model.summary()

# 3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam', metrics='mse')
model.fit([x1_train, x2_train], [y1_train, y2_train, y3_train],
          epochs=100, batch_size=1,
          validation_split=0.2, verbose=0)


#4. 평가, 예측
loss = model.evaluate([x1_test, x2_test], 
                      [y1_test, y2_test, y3_test], batch_size = 1)
print("model.metrics_names : ", model.metrics_names)
print(loss)

y1_predict, y2_predict, y3_predict = model.predict([x1_test, x2_test])

print("==================")
print("y1_predict : \n", y1_predict)
print("==================")
print("y2_predict : \n", y2_predict)
print("==================")
print("y3_predict : \n", y3_predict)
print("==================")

# RMSE 구하기
from sklearn.metrics import mean_squared_error
def RMSE(y_test, y_predict) : 
    return np.sqrt(mean_squared_error(y_test, y_predict))
RMSE1 = RMSE(y1_test, y1_predict)
RMSE2 = RMSE(y2_test, y2_predict)
RMSE3 = RMSE(y3_test, y3_predict)
RMSE = (RMSE1 + RMSE2 + RMSE3) /3
print("RMSE1 : ",RMSE1)
print("RMSE2 : ",RMSE2)
print("RMSE3 : ",RMSE3)
print("RMSE : ",RMSE)

# print("RMSE : ", RMSE(y_test, y_predict))


# R2구하기
from sklearn.metrics import r2_score
r2_1 = r2_score(y1_test, y1_predict)
r2_2 = r2_score(y2_test, y2_predict)
r2_3 = r2_score(y3_test, y3_predict)
r2 = (r2_1 + r2_2 + r2_3 )/3

print("R2_1 :  : ", r2_1)
print("R2_2 :  : ", r2_2)
print("R2_3 :  : ", r2_3)
print("R2 :  : ", r2)
