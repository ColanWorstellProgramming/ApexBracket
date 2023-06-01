#!/usr/bin/env python3
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

# Import Dataset as ds
ds = pd.read_csv('2100.csv')
ds.drop('Player', axis=1, inplace=True)

train_ds, test_ds = train_test_split(ds, test_size=0.2, random_state=42)

# Step 3: Prepare the input features and target variable
X_train = train_ds.drop('Rank', axis=1).values
y_train = train_ds['Rank'].values
X_test = test_ds.drop('Rank', axis=1).values
y_test = test_ds['Rank'].values

# Step 4: Handle missing values using mean imputation
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# Step 5: Build and train the model
model = GaussianNB()
model.fit(X_train_imputed, y_train)

# Step 6: Evaluate the model
y_pred = model.predict(X_test_imputed)
accuracy = accuracy_score(y_test, y_pred)
print('Test Accuracy:', accuracy)
