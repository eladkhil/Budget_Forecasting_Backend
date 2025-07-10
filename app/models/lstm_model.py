import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import Adam

class LSTMModel:
    def __init__(self, input_shape=(10, 1), output_size=1):
        self.model = Sequential()
        self.model.add(LSTM(64, activation='relu', input_shape=input_shape))
        self.model.add(Dense(output_size))
        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

    def train(self, X_train, y_train, epochs=50, batch_size=16):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0)

    def predict(self, X_input):
        return self.model.predict(X_input, verbose=0)
