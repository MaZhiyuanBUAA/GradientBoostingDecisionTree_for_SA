# -*- coding: utf-8 -*-
"""
Created on Fri May 06 18:53:35 2016

@author: Richard
"""
import numpy as np

def get_word(file_name):
	s = []
	f = open(file_name)
	lines = f.readlines()   
	for line in lines:
		line = line.decode("utf-8")
		line = line.strip()
		s.append(line)
	f.close()
	return s

class feature5(object):
	def __init__(self,pyPath):
		#self.path = path
		self.label_word = []
		self.label_word.append(get_word(pyPath + '/project/dict/sorry_word.txt'))
		self.label_word.append(get_word(pyPath + '/project/dict/thank_word.txt'))
		self.label_word.append(get_word(pyPath + '/project/dict/wait_word.txt'))
		self.label_word.append(get_word(pyPath + '/project/dict/urge_word.txt'))
		self.label_word.append(get_word(pyPath + '/project/dict/dirty_word.txt'))
		self.label_word.append(get_word(pyPath + '/project/dict/dear_word.txt'))
		self.label_word.append(get_word(pyPath + '/project/dict/mode_word.txt'))
		self.label_word.append(get_word(pyPath + '/project/dict/turn_word.txt'))
		self.label_word.append(get_word(pyPath + '/project/dict/time_word.txt'))
		self.label_word.append(get_word(pyPath + '/project/dict/ask_word.txt'))
		self.length_lw = len(self.label_word)
	def valuate(self,s):
		count = np.zeros(self.length_lw)
		for i in range(self.length_lw):
			for word in self.label_word[i]:
		    		count[i] += s.count(word)
		return count

#返回值为x列的字符串
	def find_word(self,s,num):
		try:
			s1 = s.decode('utf-8')
		except UnicodeDecodeError:
			print "unicode decode error"
		count = self.valuate(s1)
		if num == 0:
			return 0*count
		else:
			return count/num


	def extractF5(self,dialogs):
		# get the dialog and judge it
		f5 = list()
		for dialog in dialogs:
			visitor = list()
			agent = list()
			visitor_num = 0
			agent_num = 0
			for line in dialog:
				if line.find('Visitor') > -1:
					visitor.append(line)
					visitor_num += 1
				elif line.find('Agent') > -1:
					agent.append(line)
					agent_num += 1 #写最后一句
			visitor = ' '.join(visitor)
			agent = ' '.join(agent)

			x1,x2,x3,x4 = self.find_word(visitor, 1),self.find_word(agent, 1),self.find_word(visitor, visitor_num),self.find_word(agent, agent_num)
			f5.append(np.hstack((x1,x2,x3,x4)))
		#print f5
		return f5

