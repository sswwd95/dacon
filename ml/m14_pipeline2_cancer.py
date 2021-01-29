# 모델 RandomForestClassifier

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV # 격자형으로 찾는데 CV까지 하는것
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier #훈련 과정에서 구성한 다수의 결정 트리들을 랜덤하게 학습시켜 분류 또는 회귀의 결과도출에 사용
from sklearn.pipeline import Pipeline, make_pipeline
import warnings
warnings.filterwarnings('ignore')

####코드 실행시간 표시####
import datetime
import time
start = time.time()
#########################

#1. 데이터

dataset = load_breast_cancer()
x = dataset.data
y = dataset.target

print(x.shape,y.shape) 

x_train,x_test,y_train,y_test = train_test_split(
    x, y, random_state=77, shuffle=True, train_size=0.8
)

# 2. 모델구성 
# model = make_pipeline(MinMaxScaler(),RandomForestClassifier()) 
model = make_pipeline(StandardScaler(),RandomForestClassifier())


# 3. 훈련
model.fit(x_train, y_train)

# 4. 평가 예측
result = model.score(x_test,y_test)
print(result)

sec = time.time()-start
times = str(datetime.timedelta(seconds=sec)).split(".")
times = times[0]
print("작업 시간 : ", times) # 작업 시간 :  0:00:09

# 최적의 매개변수 :  RandomForestClassifier(max_depth=12)
# 최종정답률 :  0.9385964912280702
# 작업 시간 :  0:00:05


# MinMaxScaler
# pipe line
# 0.9385964912280702
# 작업 시간 :  0:00:00

# standardscaler
# 0.9298245614035088