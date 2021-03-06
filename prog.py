# -*- coding: utf-8 -*-
"""ML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17qITrvEvmp9684f7U5XP56qvxpjINgO7

# Import Modules
"""

import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

"""# Load Data"""

df = pd.read_csv("latestdata.csv",low_memory=False)
df=df[['age','country','date_onset_symptoms','date_admission_hospital','date_confirmation','symptoms','outcome']]
#df = df.dropna(how='any', subset=['symptoms','outcome'])
#print(df.head(30))

"""# Mapping Data"""

mapOutcome = {
    "Alive": 0,
    "Critical condition": 1, 
    "Dead": 1,
    "Death": 1,
    "Deceased": 1,
    "Died": 1,
    "Discharged": 0,
    "Discharged from hospital": 0,
    "Hospitalised": 0,
    "Migrated": 0, 
    "Migrated_Other": 0,
    "Receiving Treatment": 0,
    "Recovered": 0,
    "Stable": 0,
    "Symptoms only improved with cough. Currently hospitalized for follow-up.": 0,
    "Under treatment": 0,
    "critical condition": 1,
    "critical condition, intubated as of 14.02.2020": 1,
    "dead": 1,
    "death": 1,
    "died": 1,
    "discharge": 0,
    "discharged": 0,
    "https://www.mspbs.gov.py/covid-19.php": 0,
    "not hospitalised": 0,
    "recovered": 0,
    "recovering at home 03.03.2020" : 0,
    "released from quarantine": 0,
    "severe": 1,
    "severe illness": 1,
    "stable": 0,
    "stable condition": 0,
    "treated in an intensive care unit (14.02.2020)": 0,
    "unstable": 0,
}

df['outcome']=df['outcome'].map(mapOutcome)
mapSymptom = {
    "fever" : [1],
    "Mild to moderate" : [3],
    "Mild:moderate" : [3],
    "cough, fever" : [1,2],
    "cough" : [2],
    "fever, myalgia" : [1],
    "pneumonia:acute respiratory failure:heart failure" : [4,5],
    "cardiogenic shock:acute coronary syndrome:heart failure:pneumonia" : [4,5,6]
}
df['symptoms']=df['symptoms'].map(mapSymptom)
#drop rows with values missing in these two columns
df=df.dropna(subset=['symptoms'])
df=df.dropna(subset=['outcome'])

"""Map age ranges to the median of those age ranges. Change ages in months to 0."""

#df1 = df['age'].str.contains("-")
#print(df1.value_counts())
print(df.head(20))