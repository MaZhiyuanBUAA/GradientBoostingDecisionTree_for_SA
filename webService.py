#coding:utf-8

import os
from flask import Flask,url_for
from project.predict import predict
from config import pyetc
app = Flask(__name__)
@app.route('/')
def hello():
	return 'Hello!'

@app.route('/prediction/input/<input>')
def pred(input):
	scredisId,spredisId,featureId,dataId = input.split('|')
	#return str(s)
	try:
		result = prediction.predict(scredisId,spredisId,featureId,dataId)
	except IOError:
		return IOError,'Please confirm your input ...'
	return result

if __name__ == '__main__':
	PATH = os.getcwd()
	config = pyetc.load(PATH+os.path.sep+'config/demo.conf')
	path,host,port = config.path,config.host,config.port
	print path,host,port
	global prediction
	prediction = predict(path,host,port)
	#prediction.predict('x_test','y_test','#136-3','#136-3')
	app.run()















