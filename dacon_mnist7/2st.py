# warnings.filterwarnings("ignore")
import tensorflow as tf
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from tensorflow.keras.optimizers import RMSprop
# from tensorflow.keras.applications.efficientnet import EfficientNetB7
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten 
from tensorflow.keras.models import Model
from tensorflow.keras import optimizers
# from keras.utils import np_utils
import cv2

import gc
from keras import backend as bek
train = pd.read_csv('../dacon7/train.csv')
# test = pd.read_csv('/content/MyDrive/My Drive/Colab Notebooks/data/test.csv')


from sklearn.model_selection import train_test_split

x_train = train.drop(['id', 'digit', 'letter'], axis=1).values
x_train = x_train.reshape(-1, 28, 28, 1)

x_train = np.where((x_train<=20)&(x_train!=0) ,0.,x_train)

x_train = x_train/255
x_train = x_train.astype('float32')

y = train['digit']
y_train = np.zeros((len(y), len(y.unique())))  # 총 행의수 , 10(0~9)
for i, digit in enumerate(y):
    y_train[i, digit] = 1


train_224=np.zeros([2048,300,300,3],dtype=np.float32)

for i, s in enumerate(x_train):
    converted = cv2.cvtColor(s, cv2.COLOR_GRAY2RGB)
    resized = cv2.resize(converted,(300,300),interpolation = cv2.INTER_CUBIC)
    del converted 
    train_224[1] = resized
    del resized
    bek.clear_session()
    gc.collect()
    plt.imshow(train_224[1])        
    plt.show() 
   

from tensorflow.python.keras.callbacks import ModelCheckpoint
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from sklearn import metrics

datagen = ImageDataGenerator(
        # featurewise_center=True,
        # featurewise_std_normalization=True,
        # zca_whitening=True,
        width_shift_range=0.05,
        height_shift_range=0.05,
        zoom_range=0.15,
        rotation_range = 10,
        validation_split=0.2)
# train_datagen = ImageDataGenerator(
#     rescale = 1./255.,
#                                   #  rotation_range = 10,
#                                    width_shift_range = 0.1,
#                                    height_shift_range = 0.1,
#                                    shear_range = 0.1,
#                                    zoom_range = 0.1
#                                    validation_split=0.1                                   
#                                    )

# train_gen = datagen.flow(x_train,y_train, batch_size=16)
# valid_datagen = ImageDataGenerator(rescale=1./255) 


valgen = ImageDataGenerator(
            # featurewise_center=True,
            # zca_whitening=True,
        )

from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.callbacks import EarlyStopping
def create_model() :
    
  effnet = tf.keras.applications.EfficientNetB3(
      include_top=True,
      weights=None,
      input_shape=(300,300,3),
      classes=10,
      classifier_activation="softmax",
  )
  model = Sequential()
  model.add(effnet)


  model.compile(loss="categorical_crossentropy",
              optimizer=RMSprop(lr=initial_learningrate),
              metrics=['accuracy'])
  return model

initial_learningrate=2e-3 
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import KFold
kfold = RepeatedKFold(n_splits=5, n_repeats=10, random_state=40)
cvscores = []
Fold = 1
results = np.zeros((20480,10) )
def lr_decay(epoch):#lrv
    return initial_learningrate * 0.99 ** epoch

test = pd.read_csv('../dacon7/test.csv')

x_test = test.drop(['id', 'letter'], axis=1).values
x_test = x_test.reshape(-1, 28, 28, 1)
x_test = np.where((x_test<=20)&(x_test!=0) ,0.,x_test)
# x_test = np.where(x_test>=145,255.,x_test)
x_test = x_test/255
x_test = x_test.astype('float32')

test_224=np.zeros([20480,300,300,3],dtype=np.float32)


for i, s in enumerate(x_test):
    converted = cv2.cvtColor(s, cv2.COLOR_GRAY2RGB)
    resized = cv2.resize(converted,(300,300),interpolation = cv2.INTER_CUBIC)
    del converted
    test_224[i] = resized
    del resized

bek.clear_session()
gc.collect()



results = np.zeros( (20480,10),dtype=np.float32)


for train, val in kfold.split(train_224): 
    # if Fold<25:
    #   Fold+=1
    #   continue
    
    initial_learningrate=2e-3  
    es = EarlyStopping(monitor='val_loss', verbose=1, patience=50)      
    filepath_val_acc="../dacon7/check/effi_model_aug"+str(Fold)+".ckpt"
    checkpoint_val_acc = ModelCheckpoint(filepath_val_acc, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max',save_weights_only=True)


    gc.collect()
    bek.clear_session()
    print ('Fold: ',Fold)
    
    X_train = train_224[train]
    X_val = train_224[val]
    X_train = X_train.astype('float32')
    X_val = X_val.astype('float32')
    Y_train = y_train[train]
    Y_val = y_train[val]

    model = create_model()


    training_generator = datagen.flow(X_train, Y_train, batch_size=4,seed=7,shuffle=True)
    validation_generator = valgen.flow(X_val, Y_val, batch_size=4,seed=7,shuffle=True)
    model.fit(training_generator,epochs=150,callbacks=[LearningRateScheduler(lr_decay),es,checkpoint_val_acc],
               shuffle=True,
               validation_data=validation_generator,
               steps_per_epoch =len(X_train)//32
               )
    del X_train
    del X_val
    del Y_train
    del Y_val

    gc.collect()
    bek.clear_session()
    model.load_weights(filepath_val_acc)
    results = results + model.predict(test_224)
    
    Fold = Fold +1
    
submission = pd.read_csv('../dacon7/submission.csv')
submission['digit'] = np.argmax(results, axis=1)
# model.predict(x_test)
submission.head()
submission.to_csv('../dacon7/sub/MY1.csv', index=False)
# np.savetxt('/content/MyDrive/My Drive/Colab Notebooks/data/results.csv',results ,delimiter=',')
 
# submission = pd.read_csv('/content/MyDrive/My Drive/Colab Notebooks/data/submission.csv')
# submission['digit'] = np.argmax(results, axis=1)
# submission.head()
# submission.to_csv('/content/MyDrive/My Drive/Colab Notebooks/kfold_effi_5.csv', index=False) 
