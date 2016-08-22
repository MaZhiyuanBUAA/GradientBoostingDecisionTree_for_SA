#coding:utf-8

import os
from flask import Flask,url_for
from predict import predict
app = Flask(__name__)
@app.route('/')
def hello():
	return 'Hello!'

@app.route('/prediction/input/<input>')
def pred(input):
	scredisId,spredisId,featureId,dataId = input.split('|')
	#return str(s)
	return prediction.predict(scredisId,spredisId,featureId,dataId)

if __name__ == '__main__':
	path = '/home/easemob/work2/models_test/gbdt'
	global prediction
	prediction = predict(path,'localhost',6379)
	#prediction.predict('x_test','y_test','#136-3','#136-3')
	app.run()















