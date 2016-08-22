#coding:utf-8


import redis
from predict import predict
path = '/home/easemob/work2/models_test/gbdt'
prediction = predict(path,'localhost',6379)
prediction.predict('x_test','y_test','#136-3','#136-3')
