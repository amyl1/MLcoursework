# -*- coding: utf-8 -*-
"""ML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17qITrvEvmp9684f7U5XP56qvxpjINgO7

# Import Modules
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.impute import SimpleImputer
from sklearn import svm
from sklearn import tree
from sklearn import linear_model
from sklearn import metrics
from sklearn import model_selection

from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, classification_report, confusion_matrix, roc_curve, roc_auc_score 


from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

"""# Load Data
Excluding any columns that will not be used
"""

df = pd.read_csv("latestdata.csv",low_memory=False)

df=df[['age','country','date_onset_symptoms','date_confirmation','symptoms','outcome','chronic_disease_binary','travel_history_binary']]

print(df.shape)

"""# Mapping Data

Map patient outcome to show severity of illness. Mapped to 0 if the patitent recovered, map to 1 if the patient died
"""

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
    "treated in an intensive care unit (14.02.2020)": 1,
    "unstable": 1,
}
df['outcome']=df['outcome'].map(mapOutcome)

"""Map symptoms to integer"""

mapSymptom = {
    "fever" : 1,
    "Mild to moderate" : 2,
    "Mild:moderate" : 2,
    "cough, fever" : 3,
    "cough" : 4,
    "fever, myalgia" : 5,
    "pneumonia:acute respiratory failure:heart failure" : 6,
    "cardiogenic shock:acute coronary syndrome:heart failure:pneumonia" : 7,
}
df['symptoms']=df['symptoms'].map(mapSymptom)

"""Map chronic disease binary to 0 or 1 based on False or True"""

mapCDB = {
    "TRUE":1,
    "FALSE":0,
    False:0,
    True:1,
}
df['chronic_disease_binary']=df['chronic_disease_binary'].map(mapCDB)

"""Map age ranges to the median of those age ranges (taking the ceiling). If age given in months, round to closest year"""

mapAge = {
    "10-19":15,
    "18-65":42,
    "21-39":30,
    "23-24":24,
    "27-29":28,
    "20-30":25,
    "20-29":25,
    "35-34":35,
    "30-60":45,
    "30-39":35,
    "30-40":35,
    "40-49":45,
    "50-59":55,
    "50-65":58,
    "50-69":60,
    "60-69":65,
    "70-79":75,
    "80-89":85,
    "90-99":95,
    "17-65":41,
    "0-1":1,
    "18-50":34,
    "18-100":59,
    "18 - 100":59,
    "15-88":52,
    "90+":90,
    "60-":60,
    "4 months":0,
    "5 months":0,
    "5 month":0,
    "11 month":1,
    "6 months":1,
    "7 months":1,
    "8 month":1,
    "9 month":1,
    "13 month":1,
    "18 months":2,
    "18 month":2,
    "50-":50,
    "54.9":50,
    "48-49":49,
    "6 weeks":0,
    "74-76":75,
    "50-100":75,
    "26-27":27,
    "0-60":30,
    "22-23":23,
    "50-99":75,
    "60-100":80,
    "35-54":45,
    "87-88":88,
    "55-74":65,
    "40-45":43,
    "11-12":12,
    "5-59":32,
    "65-99":82,
    "14-18":16,
    "70-100":85,
    "47-48":48,
    "30-35":33,
    "0-19":10,
    "70-70":70,
    "37-38":38,
    "38-68":53,
    "0-6":3,
    "0-9":5,
    "16-17":17,
    "40-89":65,
    "13-19":16,
    "60-60":60,
    "80-80":80,
    "0-10":5,
    "0-18":9,
    "19-65":41,
    "60-70":65,
    "40-50":45,
    "12-19":16,
    "18-49":34,
    "41-60":50,
    "61-80":70,
    "18-60":39,
    "60-99":80,
    "40-69":55,
    "30-69":50,
    "54-56":55,
    "18-20":19,
    "17-66":42,
    "20-39":30,
    "65-":60,
    "18-99":59,
    "34-66":50,
    "75-":75,
    "55-":55,
    "18-":18,
    "27-40":34,
    "50-60":55,
    "30-70":50,
    "20-70":45,
    "20-69":45,
    "22-80":51,
    "19-77":48,
    "13-69":41,
    "0-20":10,
    "21-72":47,
    "33-78":56,
    "16-80":48,
    "23-72":48,
    "36-45":40,
    "8-68":38,
    "70-82":76,
    "25-89":57,
    "11-80":46,
    "19-75":94,
    "21-61":41,
    "22-60":41,
    "14-60":37,
    "13-65":39,
    "4-64":34,
    "2-87":45,
    "20-57":39,
    "23-71":47,
    "30-61":45.5,
    "34-44":39,
    "22-66":44,
    "5-56":31,
    "39-77":58,
    "27-58":43,
    "25-59":42,
    "1-42":22,
    "9-69":39,
    "23-84":54,
    "40-41":41,
    "28-35":32,
    "80-":80,
    "21-":21,
    "60-79":70,
    "35-39":37,
    "35-59":47,
    "80+":80,
    "5-14":10,
    "15-34": 25,
    "0-4":2,
    "00-04":2,
    "05-14":10,
    "45-49":47,
    "40-44":42,
    "30-34":32,
    "20-24":22,
    "50-54":52,
    "70-74":72,
    "25-29":27,
    "10-14":12,
    "15-19":17,
    "55-59":57,
    "60-64":62,
    "75-79":77,
    "85+":85,
    "65-69":67,
    "80-84":82,
    "5-9":7,

  }
df['age']=df['age'].replace(mapAge)

"""
Map travel_history_binary to 1 or 0 based on true and false

"""

mapTHB = {
    "TRUE":1,
    "FALSE":0,
    False:0,
    True:1,
}
df['travel_history_binary']=df['travel_history_binary'].replace(mapTHB)

"""Map countires to conitents. Create a new column for continent and drop the country column"""

asia = ["Singapore","China","Vietnam","South Korea","Malaysia","Philippines","Japan","Iran","United Arab Emirates","Nepal"]
southAmerica=["Brazil","Guyana"]
northAmerica=["United States", "Canada"]
europe=["Italy","France","Switzerland","Germany","San Marino","United Kingdom"]
africa=["Zimbabwe","Ethiopia","Gambia","Niger"]
oceania=["Australia"]

continents = {country: 1 for country in asia}
continents.update({country: 2 for country in southAmerica})
continents.update({country: 3 for country in northAmerica})
continents.update({country: 4 for country in europe})
continents.update({country: 5 for country in africa})
continents.update({country: 6 for country in oceania})
df['continent'] = df['country'].map(continents)
df=df[['age','continent','date_onset_symptoms','date_confirmation','symptoms','outcome','chronic_disease_binary','travel_history_binary']]

"""# Combatting Missing Data

Impute age using mean strategy
"""

impAge = SimpleImputer(missing_values=np.nan, strategy='mean')
df['age']=impAge.fit_transform(df[['age']]).ravel()

"""Impute contient using most frequent strategy"""

impCont = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
df['continent']=impCont.fit_transform(df[['continent']]).ravel()

"""Replace NaN with 0 in chronic_disease_binary, symptoms and travel_history_binary.


"""

df['chronic_disease_binary'] = df['chronic_disease_binary'].fillna(0.0)
df['travel_history_binary'] = df['travel_history_binary'].fillna(0)
df['symptoms'] = df['symptoms'].fillna(0)

"""Drop rows with missing outcome"""

df = df[df['outcome'].notna()]

"""# Process Dates
Use pandas.to_datetime to parse the dates
"""

df['date_onset_symptoms'] = pd.to_datetime(df['date_onset_symptoms'], errors='coerce',dayfirst=True)
df['date_confirmation'] = pd.to_datetime(df['date_confirmation'], errors='coerce',dayfirst=True)

"""Calculate the difference between date_onset_symptoms or date_confirmation. Drop any missing rows"""

df['day_diff']=abs(df['date_onset_symptoms']-df['date_confirmation']).dt.days
df = df[df['day_diff'].notna()]

"""Remove date_onset_symptoms or date_confirmation columns"""

df=df[['age','continent','day_diff','outcome','chronic_disease_binary','travel_history_binary','symptoms']]

"""#ROC Curve Function"""

def plot_roc_curve(fpr, tpr):
    plt.plot(fpr, tpr, color='red', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.show()

"""# Split the data into train and test sets"""

from sklearn.preprocessing import OneHotEncoder
x=df[['age','continent','chronic_disease_binary','travel_history_binary','day_diff','symptoms']]
y = df['outcome']
enc = OneHotEncoder(handle_unknown='ignore')
enc.fit(x)
x_enc=enc.transform(x).toarray()
x_train, x_test, y_train, y_test = train_test_split(x_enc, y, test_size=0.3, random_state=42,stratify=y)

print('Train', x_train.shape, y_train.shape)
print('Test', x_test.shape, y_test.shape)

def correlation_matrix(y, x, is_plot=False):
  
  yX = df
  yX_corr = yX.corr(method='pearson')
  yX_abs_corr = np.abs(yX_corr) 
  
  if is_plot:
    plt.figure(figsize=(8, 8))
    plt.imshow(yX_abs_corr, cmap='RdYlGn', interpolation='none', aspect='auto')
    plt.colorbar()
    plt.xticks(range(len(yX_abs_corr)), yX_abs_corr.columns, rotation='vertical')
    plt.yticks(range(len(yX_abs_corr)), yX_abs_corr.columns);
    plt.suptitle('Pearson Correlation Heat Map', fontsize=10)
    plt.show()
  
  return yX, yX_corr, yX_abs_corr

# Build the correlation matrix for the train data
yX, yX_corr, yX_abs_corr = correlation_matrix(y_train, x_train, is_plot=True)

CORRELATION_MIN = 0.05

# Sort features by their pearson correlation with the target value
corr_target = yX_abs_corr['outcome']
corr_target_sort = corr_target.sort_values(ascending=False)

# Only use features with a minimum pearson correlation with the target of 0.04
low_correlation_ftrs = corr_target_sort[corr_target_sort <= CORRELATION_MIN]

print("Removed low correlation features:")
for i,v in enumerate(low_correlation_ftrs):
  print(v, low_correlation_ftrs.index[i])

print("--------")

corr_target_sort = corr_target_sort[corr_target_sort > CORRELATION_MIN]

print("Remaining feature correlations:")
for i,v in enumerate(corr_target_sort):
  feature = corr_target_sort.index[i]
  if feature != 'outcome':
    print(v, feature)

"""# Model 1: Support Vector Machines

Use grid search to find the best parameters
"""

parameters = {'C': [0.1, 1, 10, 100, 1000], 
              'gamma': [0.01, 0.001, 0.0001],
              'kernel': ['rbf']}

svc = svm.SVC(gamma="scale")
clf = GridSearchCV(svc, parameters, cv=5)
clf.fit(x_train, y_train)
parameter_df = pd.DataFrame(clf.cv_results_)

print(parameter_df[['param_C','param_gamma','mean_test_score','std_test_score','rank_test_score']])

print(clf.best_params_)

"""Use these optimal parameters in the model"""

clf = svm.SVC(C=100, gamma=0.01, kernel='rbf', probability=True)
clf.fit(x_train, y_train)

svm_pred = clf.predict(x_test)
#check this
clf.score(x_test, y_test)

print("Accuracy:",metrics.accuracy_score(y_test, svm_pred))
mae = mean_absolute_error(y_test, svm_pred)
print('MAE: %.3f' % mae)

print(confusion_matrix(y_test,svm_pred))
print(classification_report(y_test,svm_pred))

"""RoC curve"""

probs = clf.predict_proba(x_test)
probs = probs[:, 1]
auc = roc_auc_score(y_test, probs)
fpr, tpr, thresholds = roc_curve(y_test, probs)
plot_roc_curve(fpr, tpr)

scoring = 'roc_auc'
results = model_selection.cross_val_score(clf, x_test, y_test, scoring=scoring)
print("AUC: %.3f (%.3f)" % (results.mean(), results.std()))

"""# Model 2 : Decision Tree


"""

tree_model = tree.DecisionTreeClassifier()
tree_model.fit(x_train, y_train)
tree_predict = tree_model.predict(x_test)
mae = mean_absolute_error(y_test, tree_predict)
print("Accuracy:",metrics.accuracy_score(y_test, tree_predict))
print('MAE: %.3f' % mae)
print('Score: %.3f'%tree_model.score(x_test, y_test))

scoring = 'roc_auc'
results = model_selection.cross_val_score(tree_model, x_test, y_test, scoring=scoring)
print("AUC: %.3f (%.3f)" % (results.mean(), results.std()))

probs = tree_model.predict(x_test)
auc = roc_auc_score(y_test, probs)
print('AUC: %.2f' % auc)
fpr, tpr, thresholds = roc_curve(y_test, probs)
plot_roc_curve(fpr, tpr)

print(classification_report(y_test, tree_predict))

"""# Model 3: kNN"""

from sklearn.model_selection import cross_val_score
k_range = range(1, 30)
max_score=0.0
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, x_train, y_train, cv=10, scoring='accuracy')
    if scores.mean() > max_score:
      max_score=scores.mean()
      best_k=k
print(best_k)

knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(x_train, y_train)
knn_predict=knn.predict(x_test)
mae = mean_absolute_error(y_test, knn_predict)
print("Accuracy:",metrics.accuracy_score(y_test, knn_predict))
print('MAE: %.3f' % mae)
print('Score: %.3f'%knn.score(x_test, y_test))

print(classification_report(y_test, knn_predict))

from sklearn import model_selection
scoring = 'roc_auc'
results = model_selection.cross_val_score(knn,  y_test, x_test,scoring=scoring)
print("AUC: %.3f (%.3f)" % (results.mean(), results.std()))

probs = knn.predict_proba(x_test)
probs = probs[:, 1]
auc = roc_auc_score(y_test, probs)
print('AUC: %.3f' % auc)
fpr, tpr, thresholds = roc_curve(y_test, probs)
plot_roc_curve(fpr, tpr)

"""# Comparisons"""

