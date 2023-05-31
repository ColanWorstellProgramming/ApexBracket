#!/usr/bin/env python3
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras

#Import Dataset as ds
ds = pd.read_csv('1000.csv')
ds.drop('Player', axis=1, inplace=True)

train_ds = ds.sample(frac=0.8, random_state=42)  # 80% for training
test_ds = ds.drop(train_ds.index)  # Remaining 20% for testing


# Step 3: Prepare the input features and target variable
X_train = train_ds.drop('Rank', axis=1).values
y_train = train_ds['Rank'].values
X_test = test_ds.drop('Rank', axis=1).values
y_test = test_ds['Rank'].values
X_train = X_train.astype('float32')
y_train = y_train.astype('float32')

# Step 4: Build and train the model
model = keras.Sequential([
    keras.layers.Dense(32, activation='relu', input_shape=(10,)),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=5, batch_size=1)

# Step 5: Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print('Test Loss:', loss)
print('Test Accuracy:', accuracy)
