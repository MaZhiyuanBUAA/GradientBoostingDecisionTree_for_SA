# -*- coding: utf-8 -*-
'''
Created on Jul 10, 2016

@author: shawn
'''
import sys
from toolkits import feature1
from toolkits import feature2
from toolkits import feature3
from toolkits import feature4
from toolkits import feature5
from toolkits import feature6
import redis

from sklearn.externals import joblib
from toolkits.tree_classify import loadX,classify


class predict(object):
	def __init__(self,pyPath,host,port):
		self.clf = joblib.load(pyPath + "/train_model.m")
		self.r = redis.Redis(host=host,port=port)
        	self.extractF1 = feature1.feature1(pyPath)
        	self.extractF5 = feature5.feature5(pyPath)
		self.extractF2 = feature2.feature2()
		self.extractF3 = feature3.feature3()
		self.extractF4 = feature4.feature4()
		self.extractF6 = feature6.feature6(pyPath)
	def predict(self,tSCRedisKey,tSPRedisKey,tSFKey,pDataId):
		predict_sessions = self.r.hget(tSCRedisKey, pDataId)
		if not predict_sessions:
			print "Error: not session content in redis with id " + pDataId
			sys.exit(1)
		# get feature values
		X1 = self.extractF1.extractF1(predict_sessions)

		X2 = self.extractF2.extractF2(predict_sessions)
		     
		X3 = self.extractF3.extractF3(predict_sessions)
		     
		X4 = self.extractF4.extractF4(predict_sessions)

		X5 = self.extractF5.extractF5(predict_sessions)
		  
		X6 = self.extractF6.extractF6(predict_sessions)

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
				if line[0] == '#':
					sessionId  = line[1:]
					if sessionId:
						r.hset(tSFKey, sessionId.strip(), str(X[index]));
						r.expire(tSFKey, 30*60)
						index = index + 1
		# from tree_classify import plot_roc
		#clf = joblib.load(pyPath + "/train_model.m")
		if(len(X) > 0):
			X_test = loadX(X)
			H = classify(X_test,self.clf)
			R = []
			for proba in H:
				if proba[1] > 0.74:
					R.append(1)
				else: 
					R.append(0)
			self.r.hset(tSPRedisKey, pDataId, str(R));
			self.r.expire(tSPRedisKey, 30*60)
			return str(R)
