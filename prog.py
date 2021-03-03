import pandas as pd
from sklearn.model_selection import train_test_split
X_full = pd.read_csv("data.csv",low_memory=False)
X_train, X_test = train_test_split(X_full, test_size=0.33)
print(X_train.head())
print(X_test.head())