#Machine learning model. Linear regression

import numpy as numpy
import pandas as pd
import matplotlib.pyplot as plt 
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle

#Import data into pandas data frame
datafile = "trainingCases.csv"
data = pd.read_csv(datafile)

#Drop index column and columns with NaN - not sure how to incoroporate features
#that every training case does not have
data = data.drop(['Unnamed: 0'], axis = 1)

#Create linear regression object
lm = LinearRegression()

#Create features data frame
X = data.drop(['timeToAdoption'], axis = 1)

X_train, X_test, Y_train, Y_test = train_test_split(X, data.timeToAdoption, test_size = .33, random_state = 5)
#Linear regression on training examples
#And y value timeToAdoption
lm.fit(X_train, Y_train)

#Export model to a file for further use
filename = 'finalizedmodel.sav'
pickle.dump(lm, open(filename, 'wb'))

#Test model 
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, Y_test)
print(result)