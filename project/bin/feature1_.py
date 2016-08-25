# -*- coding: utf-8 -*-
"""
Created on Thu May 05 09:58:26 2016

@author: Richard
changed by: mazhiyuan
time:20160819 
"""

import jieba,time
import numpy as np

def get_word(file_name):
	s = []
	f = open(file_name)
	lines = f.readlines()
	for line in lines:
		line = line.strip()
		line = line.decode('utf-8')
		s.append(line)
	f.close()
	return s


class feature1(object):
	def __init__(self,pyPath):
	# get the word in different sensiment
		t0 = time.time()
		self.negetive_evaluate_custom = get_word(pyPath + "/project/dict/negetive_evaluate_custom.txt")
		self.negetive_evaluate = get_word(pyPath + "/project/dict/negetive_evaluate.txt")
		self.negetive_emotion = get_word(pyPath + "/project/dict/negetive_emotion.txt")
		self.positive_evaluate = get_word(pyPath + "/project/dict/positive_evaluate.txt")
		self.positive_emotion = get_word(pyPath + "/project/dict/positive_emotion.txt")
		self.over_word = get_word(pyPath + "/project/dict/over_word.txt")
		print 'load time:%f'%(time.time()-t0)
	def valuate(self,s):
		#t0 = time.time()
		word_list = jieba.cut(s, cut_all=True)
		count = np.zeros(5) 
		for word in word_list:
			word = word.strip()
			if not word:
				continue
			elif self.negetive_evaluate_custom.count(word) > 0 or self.negetive_evaluate.count(word) > 0:
				count[0] += 1
			elif self.negetive_emotion.count(word) > 0:
				count[1] += 1
			elif self.positive_evaluate.count(word) > 0:
				count[2] += 1
			elif self.positive_emotion.count(word) > 0:
				count[3] += 1
			elif self.over_word.count(word) > 0:
				count[4] += 1
		print count
		return count            
    
	# 返回值为x列的字符串
	def find_word(self, s, num):
		try:
			s1 = s.decode('utf-8')
		except UnicodeDecodeError:
			print "unicode decode error"
		#t0 = time.time()
		count = self.valuate(s1)/num
		#print 'valuate:%f'%(time.time()-t0)
		return count

	def extractF1(self, dialogs):
		#global pyPath
		#pyPath = path
		# get the dialog and judge it
		#dialogs = re.split(r'#[0-9]+')
		f1 = list()
		for dialog in dialogs:
			visitor = list()
			agent = list()
			visitor_num = 0
			num = 0
			for line in dialog:
				if line.find('Visitor') > -1:
					visitor.append(line)
					visitor_num += 1
					num += 1
				elif line.find('Agent') > -1:
					agent.append(line)
					num += 1
			visitor = ' '.join(visitor)
			agent = ' '.join(agent)
			x1,x2,x3,x4 = self.find_word(visitor, 1),self.find_word(agent, 1),self.find_word(visitor, visitor_num),self.find_word(visitor+agent, num)
			f1.append(np.hstack((x1,x2,x3,x4)))
		return f1
