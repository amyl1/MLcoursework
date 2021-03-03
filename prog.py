import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

X_full = pd.read_csv("data.csv",low_memory=False)
X_full['age_isDigit'] = np.where(X_full['age'].str.isdigit(), ['Yes'],['No'])
for index, row in X_full.iterrows():
    
    if row['age_isDigit']=="No" and '-' in row['age']:
        ages=row['age'].split('-')
        try:
            #take age range and find median
            median=(int(ages[0])+int(ages[1]))/2
            row['age']=math.ceil(median)
        except:
            row['age']='NaN'
#remove rows with NaN
X_full = X_full[X_full['age'].notna()]
X_train, X_test = train_test_split(X_full, test_size=0.33)

print(X_train.head())
print(X_test.head())

"""
print(X_train.shape)
missing_val_count_by_column = (X_train.isnull().sum())
print(missing_val_count_by_column[missing_val_count_by_column > 0])

for col in cols_with_missing:
    X_train_plus[col + '_was_missing'] = X_train_plus[col].isnull()
    Xtest_plus[col + '_was_missing'] = X_test_plus[col].isnull()
"""