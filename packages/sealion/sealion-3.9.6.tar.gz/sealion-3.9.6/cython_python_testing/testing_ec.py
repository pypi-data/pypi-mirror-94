from sealion.ensemble_learning import EnsembleClassifier
from sealion.decision_trees import DecisionTree
from regression_gd import SoftmaxRegression
from sealion.regression import LogisticRegression

log_reg = LogisticRegression()
softmax = SoftmaxRegression(2)
dt = DecisionTree()

import numpy as np
import pandas as pd
data = pd.read_csv('/users/anish/downloads/breast-cancer-wisconsin.data')

def data_collection(data) :
    training_data = data[['ID', 'clump_thickness','cell_uniformity', 'shape_uniformity', 'chromatin','nucleoli']]
    labels = data['class']

    training_data = training_data.drop(['ID', 'chromatin'], axis = 1)
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    training_data = training_data._get_numeric_data()

    training_data = scaler.fit_transform(training_data)

    training_data, labels = np.array(training_data), np.array(labels)

    split = 30
    x_test, y_test = training_data[:split], labels[:split]
    x_train,y_train = training_data[split:], labels[split:]

    x_train, y_train, x_test, y_test = np.array(x_train, dtype = float), np.array(y_train, dtype = float), np.array(x_test, dtype = float), np.array(y_test, dtype = float)
    y_train, y_test = y_train/2 - 1, y_test/2 - 1

    return x_train,x_test, y_train, y_test

x_train, x_test, y_train, y_test = data_collection(data)

ec = EnsembleClassifier({'sfmx' : softmax, "log" : log_reg, "dt" : log_reg}, classification = True)
ec.fit(x_train, y_train)
ec.evaluate(x_test, y_test)
