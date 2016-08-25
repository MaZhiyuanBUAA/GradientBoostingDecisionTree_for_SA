# -*- coding: utf-8 -*-
"""
Created on Thu May 05 09:58:26 2016

@author: Richard
changed by: mazhiyuan
time:20160819 
"""

import jieba,time
import numpy as np

def get_word(file_name,n):
	#s = []
	f = open(file_name)
	lines = f.readlines()
	f.close()
	dic = dict()
	'''
	lines = lines.decode('utf-8')
	f.close()
	'''
	for line in lines:
		line = line.strip()
		dic[line] = n
		#s.append(line)
	return dic


class feature1(object):
	def __init__(self,pyPath):
	# get the word in different sensiment
		t0 = time.time()
		self.negetive_evaluate_custom = get_word(pyPath + "/project/dict/negetive_evaluate_custom.txt",0)
		self.negetive_evaluate = get_word(pyPath + "/project/dict/negetive_evaluate.txt",0)
		self.negetive_emotion = get_word(pyPath + "/project/dict/negetive_emotion.txt",1)
		self.positive_evaluate = get_word(pyPath + "/project/dict/positive_evaluate.txt",2)
		self.positive_emotion = get_word(pyPath + "/project/dict/positive_emotion.txt",3)
		self.over_word = get_word(pyPath + "/project/dict/over_word.txt",4)
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
			try:
				count[self.negetive_evaluate_custom[word]] += 1
				continue
			except:
				pass
			try:
				count[self.negetive_evaluate[word]] += 1
				continue
			except:
				pass
			try:
				count[self.negetive_emotion[word]] += 1
				continue
			except:
				pass
			try:
				count[self.positive_evaluate[word]] += 1
				continue
			except:
				pass
			try:
				count[self.positive_emotion[word]] += 1
				continue
			except:
				pass
			try:
				count[self.over_word[word]] += 1
				continue
			except:
				pass
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
