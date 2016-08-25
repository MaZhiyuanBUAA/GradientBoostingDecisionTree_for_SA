# -*- coding: utf-8 -*-
'''
Created on Jul 10, 2016

@author: shawn
'''
import sys,os,re
import numpy as np
from bin import feature1_bf
from bin import feature2
from bin import feature3
from bin import feature4
from bin import feature5
from bin import feature6
import redis,time

from sklearn.externals import joblib
from bin.tree_classify import loadX,classify


class predict(object):
	def __init__(self,pyPath,host,port):
		self.clf = joblib.load(pyPath +os.path.sep+"project/train_model.m")
		self.r = redis.Redis(host=host,port=port)
        	self.extractF1 = feature1_bf.feature1(pyPath)
        	self.extractF5 = feature5.feature5(pyPath)
		self.extractF2 = feature2.feature2()
		self.extractF3 = feature3.feature3()
		self.extractF4 = feature4.feature4()
		self.extractF6 = feature6.feature6(pyPath)
	def predict(self,tSCRedisKey,tSPRedisKey,tSFKey,pDataId):
		time0 = time.time()
		predict_sessions = self.r.hget(tSCRedisKey, pDataId)
		if not predict_sessions:
			print "Error: not session content in redis with id " + pDataId
			sys.exit(1)
		# get feature values
		pattern = re.compile(r'#[0-9]+\n')
		sessionId = pattern.findall(predict_sessions)
		dialogs = re.split(r'#[0-9]+\n',predict_sessions)
		try:
			dialogs.remove('')
		except:
			print 'attention,mybe some error in dialogs ...'
		if len(sessionId)!=len(dialogs):
			return IOError,'Error in etracting dialogs:session number %f,dialogs number %f'%(len(sessionId),len(dialogs))
		dialogs = [ele.strip().split('\n') for ele in dialogs]
		time1 = time.time()
		print 'extract dialogs: %f seconds'%(time1-time0)
		X1 = self.extractF1.extractF1(dialogs)
		tf1 = time.time()
		print 'f1:%f'%(tf1-time1)
		X2 = self.extractF2.extractF2(dialogs)
		tf2 = time.time()
		print 'f2:%f'%(tf2-tf1)
		X3 = self.extractF3.extractF3(dialogs)
		tf3 = time.time()
		print 'f3:%f'%(tf3-tf2)
		X4 = self.extractF4.extractF4(dialogs)
		tf4 = time.time()
		print 'f4:%f'%(tf4-tf3)
		X5 = self.extractF5.extractF5(dialogs)
		tf5 = time.time()
		print 'f5:%f'%(tf5-tf4)
		X6 = self.extractF6.extractF6(dialogs)
		tf6 = time.time()
		print 'f6:%f'%(tf6-tf5)
		# assemble feature values
		#time2 = time.time()
		#print 'extract feature: %f seconds'%(time2-time1)
		X = []
		for i,session in enumerate(sessionId):
			sessionFeature = np.hstack((X1[i],X2[i],X3[i],X4[i],X5[i],X6[i]))
			sessionFeature = sessionFeature/sessionFeature.max()
			X.append(sessionFeature)
			# get all session ids and put feature values in redis
			self.r.hset(tSFKey, session.strip(), str(sessionFeature));
			self.r.expire(tSFKey, 30*60)

		#from tree_classify import plot_roc
		#clf = joblib.load(pyPath + "/train_model.m")
		H = classify(X,self.clf)
		R = []
		for proba in H:
			if proba[1] > 0.74:
				R.append(1)
			else: 
				R.append(0)
		self.r.hset(tSPRedisKey, pDataId, str(R));
		self.r.expire(tSPRedisKey, 30*60)
		#print 'predict: %f seconds'%(time.time()-time2)
		return str(R)
if __name__ == '__main__':
	prediction = predict('/home/easemob/work2/gbdt','127.0.0.1',6379)
	print prediction.predict('testSession002','testPrediction','testResult','testContent')
	#print prediction.predict('testSession003','testPrediction','testResult','testContent')
