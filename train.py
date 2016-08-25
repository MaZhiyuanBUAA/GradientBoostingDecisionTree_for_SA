#coding:utf-8
import cPickle,random
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib
import numpy as np
import matplotlib.pyplot as plt
#from sklearn import metrics
from sklearn.metrics import roc_auc_score,roc_curve
def loadTrainSet():
	f = file('ftrain.pkl','r')
	ftrain = cPickle.load(f)
	f.close()
	lf = len(ftrain)
	f = file('rtrain.pkl','r')
	rtrain = cPickle.load(f)
	f.close()

	rtrain = random.sample(rtrain,lf)

	trainSet = list()
	for ele in ftrain:
		trainSet.append((ele,1))
	for ele in rtrain:
		trainSet.append((ele,0))
	random.shuffle(trainSet)
	X,Y=list(),list()
	for ele in trainSet:
		X.append(ele[0])
		Y.append(ele[1])
	return (X,Y)

def loadValideSet(size):
	f = file('fvalide.pkl','r')
	fvalide = cPickle.load(f)
	fvalide = random.sample(fvalide,size)
	f.close()
	f = file('rvalide.pkl','r')
	rvalide = cPickle.load(f)
	f.close()
	rvalide = random.sample(rvalide,size)
	
	return (fvalide,rvalide)

def loadTestSet(size):
	f = file('ftest.pkl','r')
	ftest = cPickle.load(f)
	fvalide = random.sample(ftest,size)
	f.close()
	f = file('rtest.pkl','r')
	rtest = cPickle.load(f)
	f.close()
	rtest = random.sample(rtest,size)
	
	return (ftest,rtest)

def perform(clf,fvalide,rvalide):
	TPR = clf.score(fvalide,np.zeros(len(fvalide)))
	FPR = clf.score(rvalide,np.zeros(len(rvalide)))
	return (TPR,FPR)
def train():
	clf = GradientBoostingClassifier(learning_rate = 0.06 ,n_estimators =100,max_features = 'log2',min_samples_leaf=2)
	X,Y = loadTrainSet()
	clf.fit(X,Y)
	joblib.dump(clf,'train000.m',compress=3)
	fvalide,rvalide = loadValideSet(150)
	print perform(clf,fvalide,rvalide)
def optimisation(clf,fvalide,rvalide,eps):
	r1 = clf.predict_proba(fvalide)
	r0 = clf.predict_proba(rvalide)
	res = np.zeros(2)
	#return r1,r0
	for ele in r1:
		if ele[1] > eps:
			res[0]+=1
	for ele in r0:
		if ele[1] > eps:
			res[1]+=1
	
	pre = res[0]/sum(res)
	recall = res[0]/len(r1)
	return (pre,recall,2*pre*recall/(pre + recall))

def plot_roc(clf):
	roc = list()
	fvalide,rvalide = loadValideSet(150)
	r1 = clf.predict_proba(fvalide)
	r0 = clf.predict_proba(rvalide)
	y = list()
	for ele in r1:
		y.append((1,ele[1]))
	for ele in r0:
		y.append((0,ele[1]))
	#y.sort(key=lambda x:x[1])
	y_true,y_score = list(),list()
	for ele in y:
		y_true.append(ele[0])
		y_score.append(ele[1])
	fpr, tpr, thresholds = roc_curve(y_true, y_score, pos_label=1)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(fpr,tpr,'b')
	#ax.xlabel('fpr')
	#ax.ylabel('tpr')
	fig.savefig('roc.png')
	auc = roc_auc_score(y_true, y_score)
	return auc
if __name__=='__main__':
	#train()
	clf = joblib.load('train_model.m')
	
	fvalide,rvalide = loadValideSet(150)
	eps = 0.2#0.388,f1=0.737
	while eps < 0.8:
		print optimisation(clf,fvalide,rvalide,eps),eps
		eps += 0.01
	
	print plot_roc(clf)
