#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Import Dataset as ds
ds = pd.read_csv('2100.csv')
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

# Step 4: Handle missing values using mean imputation
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# Step 5: Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)

# Step 6: Build and train the model
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train_scaled, y_train)

# Step 7: Evaluate the model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print('Test Accuracy:', accuracy)
