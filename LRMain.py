#!/usr/bin/env python3
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Import Dataset as ds
ds = pd.read_csv('2100.csv')
ds.drop('Player', axis=1, inplace=True)

# Drop rows with missing values
ds.dropna(inplace=True)

# Prepare the input features and target variable
X = ds.drop('Rank', axis=1).values
y = ds['Rank'].values

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse)
