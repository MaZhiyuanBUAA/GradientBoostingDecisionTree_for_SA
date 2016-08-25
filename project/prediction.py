# -*- coding: utf-8 -*-
'''
Created on Jul 10, 2016

@author: shawn
'''
import sys
from bin import feature1
from bin import feature2
from bin import feature3
from bin import feature4
from bin import feature5
from bin import feature6
import redis

from sklearn.externals import joblib
from bin.tree_classify import loadX
from tree_classify import classify

pyPath = sys.argv[1]
redisHost = sys.argv[2]
redisPort = sys.argv[3]
tenantSessionContentRedisKey = sys.argv[4]
tenantSessionPredictionRedisKey = sys.argv[5]
tenantSessionFeatureKey = sys.argv[6]
predictionDataId = sys.argv[7]

# get session content from redis
r = redis.Redis(host=redisHost,port=redisPort)
predict_sessions = r.hget(tenantSessionContentRedisKey, predictionDataId)

if not predict_sessions:
    print "Error: not session content in redis with id " + predictionDataId
    sys.exit(1)
# get feature values
X1 = feature1.extractF1(pyPath, predict_sessions)

X2 = feature2.extractF2(pyPath, predict_sessions)
     
X3 = feature3.extractF3(pyPath, predict_sessions)
     
X4 = feature4.extractF4(pyPath, predict_sessions)

X5 = feature5.extractF5(pyPath, predict_sessions)
  
X6 = feature6.extractF6(pyPath, predict_sessions)

# assemble feature values
X = []
sessionCount = len(X1)
if sessionCount > 0 :
    for i in xrange(0, sessionCount):
        X.append(X1[i] + X2[i] + X3[i] + X4[i] + X5[i] + X6[i])

    # get all session ids and put feature values in redis
    lines = predict_sessions.split('\r\n')
    index = 0;
    for line in lines:
        if not line and not line.strip():
            continue
        if line[0] == '#' :
           sessionId  = line[1:]
           if sessionId:
               r.hset(tenantSessionFeatureKey, sessionId.strip(), str(X[index]));
               r.expire(tenantSessionFeatureKey, 30*60)
               index = index + 1
    
    
# from tree_classify import plot_roc
clf = joblib.load(pyPath + "/train_model.m")
if(len(X) > 0):
    X_test = loadX(X)
    H = classify(X_test,clf)
    R = []
    for proba in H:
        if proba[1] > 0.74:
            R.append(1)
        else: 
            R.append(0)
    r.hset(tenantSessionPredictionRedisKey, predictionDataId, str(R));
    r.expire(tenantSessionPredictionRedisKey, 30*60)
    print predictionDataId
