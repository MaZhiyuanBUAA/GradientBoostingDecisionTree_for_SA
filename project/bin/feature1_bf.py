# -*- coding: utf-8 -*-
"""
Created on Thu May 05 09:58:26 2016

@author: Richard
changed by: mazhiyuan
time:20160819 
"""

import jieba,time
import numpy as np


import pybloomfilter as pbf

class feature1(object):
	def __init__(self,pyPath):
	# get the word in different sensiment
		t0 = time.time()
		self.negetive_evaluate_custom = pbf.BloomFilter.open(pyPath + "/project/dict/negetive_evaluate_custom.bloom")
		self.negetive_evaluate = pbf.BloomFilter.open(pyPath + "/project/dict/negetive_evaluate.bloom")
		self.negetive_emotion = pbf.BloomFilter.open(pyPath + "/project/dict/negetive_emotion.bloom")
		self.positive_evaluate = pbf.BloomFilter.open(pyPath + "/project/dict/positive_evaluate.bloom")
		self.positive_emotion = pbf.BloomFilter.open(pyPath + "/project/dict/positive_emotion.bloom")
		self.over_word = pbf.BloomFilter.open(pyPath + "/project/dict/over_word.bloom")
		print 'load time:%f'%(time.time()-t0)
	def valuate(self,s):
		#t0 = time.time()
		word_list = jieba.cut(s, cut_all=True)
		#word_list = [word.encode('utf-8') for word in word_list]
		#print word_list
		#print 'cut:%f'%(time.time()-t0)
		count = np.zeros(5) 
		#n = 0
		for word in word_list:
			word = word.strip()
			if not word:
				continue
			try:
				word = word.encode('utf-8')
				#count[self.dic[word]] += 1
			except:
				continue
			if word in self.negetive_evaluate_custom or word in self.negetive_evaluate:
				count[0] += 1
			elif word in self.negetive_emotion:
				count[1] += 1
			elif word in self.positive_evaluate:
				count[2] += 1
			elif word in self.positive_emotion:
				count[3] += 1
			elif word in self.over_word:
				count[4] += 1
		#print count
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
