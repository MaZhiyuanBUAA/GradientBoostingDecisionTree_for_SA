# -*- coding: utf-8 -*-
"""
Created on Thu May 05 21:00:552 2016

@author: Richard
"""
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib

import numpy as np


def feature_scaling(X):
    m,n = np.shape(X)
    max_value=[]
    for j in xrange(n):
        max_value.append(0.0)
    for i in xrange(m):
        for j in xrange(n):
            if abs(X[i][j]) >= max_value[j]:
                max_value[j] = abs(X[i][j])
    for i in xrange(m):
        for j in xrange(n):
            if max_value[j] == 0:
                X[i][j] == 0
            else:
                X[i][j] = float(X[i][j])/max_value[j] 
    return X

def loadX(X_test):
    X = []
    #get x
#     file_x = open(file_name1)
#     lines = file_x.readlines()
    for line in X_test:
        Array = []
        #基准
        line = line.strip()
        x = line.split(' ')
        for i in xrange(100):
            e = x[i].strip()
            value = float(e)
            Array.append(value)
        X.append(Array)
    #Feature Scaling
    X = feature_scaling(X)
#     file_x.close()
    return X
    

def load(file_name1,file_name2):
    X = []
    Y = []
    #get x
    file_x = open(file_name1)
    lines = file_x.readlines()
    for line in lines:
        Array = []
        #基准
        line = line.strip()
        x = line.split(' ')
        for i in xrange(100):
            e = x[i].strip()
            value = float(e)
            Array.append(value)
        X.append(Array)
    #Feature Scaling
    X = feature_scaling(X)
    file_x.close()
    
    #get y
    file_y = open(file_name2)
    lines = file_y.readlines()
    for line in lines:
        Array = []
        y = line.strip()
        Array.append(float(y))
        Y.append(Array)
    return X,Y
    
def sigmoid(z):
    return 1.0/(1 + np.exp(-z))

def plot_roc(h,y):
    c1 = 0
    c0 = 0
    for i in y:
        if i[0] == 1.0:
            c1 += 1
        if i[0] == 0.0:
            c0 += 1
    x = []
    y = []
    for i in xrange(100):
        TP = 0.0
        TN = 0.0
        FP = 0.0
        FN = 0.0
        valve = 0.01*i
        for j in xrange(c1):
            if h[j][1] > valve:
                TP += 1
            else:
                FN += 1
        for j in xrange(c1,c1+c0):
            if h[j][1] > valve:
                FP += 1 
            else:
                TN += 1
        TPR = TP/(TP+FN)
        FPR = FP/(FP+TN)
        x.append(FPR)
        y.append(TPR)
    
    count = 0.0
    print '1:',c1,'  0:',c0
    for i in xrange(c1):
        for j in xrange(c0):
            if h[i][1] > h[c1+j][1]:
                count += 1.0
            if h[i][1] == h[c1+j][1]:
                count += 0.5
    print 'AUC:',count/(c1*c0)
    

def tree_training(dataArray,labelArray):
    X = np.mat(dataArray)
    Y = np.mat(labelArray)
#     Z = np.array(labelArray).ravel()
    m,n = np.shape(X)
    print m,n
    m,k = np.shape(Y)
    print m,k
    #use GBDT to classify
    clf = GradientBoostingClassifier(learning_rate = 0.06 ,n_estimators =100,
        max_features = 'log2',min_samples_leaf=2)
    clf.fit(X,np.asarray(Y).ravel())
    return clf    
    
def classify(X,clf):
    return clf.predict_proba(X)


def train_model(fileX, fileY):
    X, Y = load(fileX, fileY)
    clf = tree_training(X, Y)
    joblib.dump(clf, "train_model.m", compress=3)

