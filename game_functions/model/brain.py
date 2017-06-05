from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam
from keras.layers import Dropout


def keras_model(inputs, dropouts=0.2, opti=1e-6, clipping=1, clipval=10):
    keras_model = Sequential()
    keras_model.add(Dense(128, input_dim=inputs, activation='relu'))
    keras_model.add(Dropout(dropouts))
    keras_model.add(Dense(128, activation='relu'))
    keras_model.add(Dropout(dropouts))
    keras_model.add(Dense(1))
    adam = Adam(lr=opti, clipnorm=clipping, clipvalue=clipval)
    keras_model.compile(loss='mse', optimizer='adam')
    return keras_model
