#!/usr/bin/env python

import keras as k
import numpy as np
import scipy as sp
from keras.layers import Dense, Activation
from keras import backend as b

model = k.models.Sequential()

model.add(Dense(32, input_shape=(14,), bias=True, activation="tanh"))
model.add(Dense(10, activation="sigmoid"))
model.add(Dense(1, activation="sigmoid"))
model.compile(loss="mean_squared_error",
              optimizer="Adadelta",
              metrics=['mean_squared_error'])

data = np.loadtxt("LowBeta.txt")
#data/=12.0
print(data)
alpha = np.loadtxt("Alpha.txt")


model.fit(data, alpha, batch_size=50, epochs=20000, verbose=0)
P = model.predict(data)
P = np.reshape(P, (50,))
print(P.shape)
print(np.corrcoef(alpha, P))

