# -*- coding: utf-8 -*-
"""
Created on Fri May 06 20:57:36 2016

@author: Richard
"""
import re
import numpy as np

def get_word(file_name):
	s = []
	f = open(file_name)
	lines = f.readlines()   
	for line in lines:
	#         line = line.decode("utf-8")
		line = line.strip()
		s.append(line)
	f.close()
	return s

class feature6(object):
	def __init__(self,path):
		#self.pyPath = path
		self.solve_word = get_word(path + "/project/dict/solve_word.txt")  
		self.cannot_word = get_word(path + "/project/dict/cannot_word.txt")
		self.can_word = get_word(path + "/project/dict/can_word.txt")
	#用户重复句子数
	def get_x0(self,visitor):
		return 1.*(len(visitor)-len(list(set(visitor))))
	#差评批评
	def get_x1(self,visitor):
		count = 0
		for i in visitor:
			if i.count('好评') > 0 and i.count('不') > 0:
				count += 1
			if i.count('差评') > 0 and i.count('不') <= 0:
				count += 1
			if i.count('投诉') > 0 and i.count('不') <= 0:
				count += 1
			if i.count('满意') > 0 and i.count('不') > 0:
				count += 1
		return float(count)
	#好评表扬
	def get_x2(self,visitor):
		count = 0
		for i in visitor:
			if i.count('好评') > 0 and i.count('不') <= 0:
				count += 1
			if i.count('差评') > 0 and i.count('不') > 0:
				count += 1
			if i.count('满意') > 0 and i.count('不') <= 0:
				count += 1
			if i.count('投诉') > 0 and i.count('不') > 0:
				count += 1    
		return float(count)
	#问题未解决
	def get_x3(self,agent):
		count = 0
		for i in self.solve_word:
			for j in self.cannot_word:
				for k in agent:
					if k.count(i) > 0 and k.count(j) >0:
						count += 1
		return float(count)
	#问题解决
	def get_x4(self,agent):
		count = 0
		for i in self.solve_word:
			for j in self.cannot_word:
				for c in self.can_word:
					for k in agent:
						if k.count(i) > 0 and k.count(j) <= 0 and k.count(c)>0:
							count += 1    
		return float(count)

	def get_x(self,visitor,agent):
		#visitor<list>:用户语句
		#agent<list>:客服语句
		x = np.zeros(10)
		x[0] = self.get_x0(visitor)
		x[1] = self.get_x1(visitor)
		x[2] = self.get_x2(visitor)
		x[3] = self.get_x3(agent)
		x[4] = self.get_x4(agent)
		x[5] = x[0]/len(visitor)
		x[6] = x[1]/len(visitor)
		x[7] = x[2]/len(visitor)
		x[8] = x[3]/len(visitor)    
		x[9] = x[4]/len(visitor)  
		return x

	def extractF6(self, dialogs):
		f6 = list()
		for dialog in dialogs:
			visitor = list()
			agent = list()
			for line in dialog:
				if line.find('Visitor') > -1:
					visitor.append(line)
				if line.find('Agent') > -1:
					agent.append(line)
			s = self.get_x(visitor, agent)
			f6.append(s)
		#print f6
		return f6

