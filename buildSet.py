#coding:utf-8

import numpy as np
import re,cPickle,random
from project.bin import feature1,feature2,feature3,feature4,feature5,feature6

class extractFeature(object):
	def __init__(self,pyPath):
		#self.clf = joblib.load(pyPath +os.path.sep+"project/train_model.m")
		#self.r = redis.Redis(host=host,port=port)
        	self.extractF1 = feature1.feature1(pyPath)
        	self.extractF5 = feature5.feature5(pyPath)
		self.extractF2 = feature2.feature2()
		self.extractF3 = feature3.feature3()
		self.extractF4 = feature4.feature4()
		self.extractF6 = feature6.feature6(pyPath)
	def extract(self,dialogs):
		length = len(dialogs)
		F = []
		X1 = self.extractF1.extractF1(dialogs)
		#tf1 = time.time()
		#print 'f1:%f'%(tf1-time1)
		X2 = self.extractF2.extractF2(dialogs)
		#tf2 = time.time()
		#print 'f2:%f'%(tf2-tf1)
		X3 = self.extractF3.extractF3(dialogs)
		#tf3 = time.time()
		#print 'f3:%f'%(tf3-tf2)
		X4 = self.extractF4.extractF4(dialogs)
		#tf4 = time.time()
		#print 'f4:%f'%(tf4-tf3)
		X5 = self.extractF5.extractF5(dialogs)
		#tf5 = time.time()
		#print 'f5:%f'%(tf5-tf4)
		X6 = self.extractF6.extractF6(dialogs)
		for i in range(length):
			F.append(np.hstack((X1[i],X2[i],X3[i],X4[i],X5[i],X6[i])))
		return F
def txt2vec():
	f = file('Sent.txt')
	data = f.read()
	f.close()
	pattern = re.compile(r'#[0-9]+#[0-9]\n')
	sessionId = pattern.findall(data)
	y = [int(ele[-2]) for ele in sessionId]
	dialogs = re.split(r'#[0-9]+#[0-9]\n',data)
	dialogs.remove('')
	dialogs = [ele.strip().split('\n') for ele in dialogs]
	if len(y)!=len(dialogs):
		print 'some error in dialogs'
	ef = extractFeature('/home/easemob/work2/gbdt')
	x = ef.extract(dialogs)
	f = file('data.pkl','w')
	cPickle.dump((x,y),f)
	f.close()

def sepFR():
	f = file('data.pkl','r')
	data = cPickle.load(f)
	f.close()
	l_data = len(data)
	x,y = data
	fs_x = list()
	rs_x = list() 
	
	for ind,ele in enumerate(y):
		if ele == 1:
			fs_x.append(x[ind])
		if ele == 5:
			rs_x.append(x[ind])
	f = file('fx.pkl','w')
	cPickle.dump(fs_x,f)
	f.close()
	f = file('rx.pkl','w')
	cPickle.dump(rs_x,f)
	f.close()
def buildFset():
	f = file('fx.pkl','r')
	fs_x = cPickle.load(f)
	f.close()
	l = len(fs_x)
	index = [i for i in range(l)]
	random.shuffle(index)
	ftrain_ind = index[:int(l*0.7)]
	fvalide_ind = index[int(l*0.7):int(l*0.85)]
	ftest_ind = index[int(l*0.85):]
	
	ftrain,fvalide,ftest = list(),list(),list()
	for i in ftrain_ind:
		ftrain.append(fs_x[i])
	for i in fvalide_ind:
		fvalide.append(fs_x[i])
	for i in ftest_ind:
		ftest.append(fs_x[i])
	f = file('ftrain.pkl','w')
	cPickle.dump(ftrain,f)
	f.close()
	f = file('fvalide.pkl','w')
	cPickle.dump(fvalide,f)
	f.close()
	f = file('ftest.pkl','w')
	cPickle.dump(ftest,f)
	f.close()
def buildRset():
	f = file('rx.pkl','r')
	fs_x = cPickle.load(f)
	f.close()
	l = len(fs_x)
	index = [i for i in range(l)]
	random.shuffle(index)
	rtrain_ind = index[:int(l*0.7)]
	rvalide_ind = index[int(l*0.7):int(l*0.85)]
	rtest_ind = index[int(l*0.85):]
	
	rtrain,rvalide,rtest = list(),list(),list()
	for i in rtrain_ind:
		rtrain.append(fs_x[i])
	for i in rvalide_ind:
		rvalide.append(fs_x[i])
	for i in rtest_ind:
		rtest.append(fs_x[i])
	f = file('rtrain.pkl','w')
	cPickle.dump(rtrain,f)
	f.close()
	f = file('rvalide.pkl','w')
	cPickle.dump(rvalide,f)
	f.close()
	f = file('rtest.pkl','w')
	cPickle.dump(rtest,f)
	f.close()
if __name__=='__main__':
	#txt2vec()
	#sepFR()
	#buildFset()
	buildRset()
