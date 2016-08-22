# -*- coding: utf-8 -*-
"""
Created on Thu May 05 09:58:26 2016

@author: Richard
changed by: mazhiyuan
time:20160819 
"""

import jieba

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
		self.negetive_evaluate_custom = get_word(pyPath + "/dict/negetive_evaluate_custom.txt")
		self.negetive_evaluate = get_word(pyPath + "/dict/negetive_evaluate.txt")
		self.negetive_emotion = get_word(pyPath + "/dict/negetive_emotion.txt")
		self.positive_evaluate = get_word(pyPath + "/dict/positive_evaluate.txt")
		self.positive_emotion = get_word(pyPath + "/dict/positive_emotion.txt")
		self.over_word = get_word(pyPath + "/dict/over_word.txt")
	def valuate(self,s):
		word_list = jieba.cut(s, cut_all=True)
		count = [0.0, 0.0, 0.0, 0.0, 0.0] 
		for word in word_list:
			if self.negetive_evaluate_custom.count(word) > 0 or self.negetive_evaluate.count(word) > 0:
				count[0] += 1
			elif self.negetive_emotion.count(word) > 0:
				count[1] += 1
			elif self.positive_evaluate.count(word) > 0:
				count[2] += 1
			elif self.positive_emotion.count(word) > 0:
				count[3] += 1
			elif self.over_word.count(word) > 0:
				count[4] += 1
		return count        
    
	# 返回值为x列的字符串
	def find_word(self, s, num):
		s1 = ''
		try:
			s1 = s.decode('utf-8')
		except UnicodeDecodeError:
			print "unicode decode error"
		count = self.valuate(s1)
		x_line = ''
		for i in xrange(5):
			f = count[i] / num
			x_line += str(f) + ' '
		return x_line

	def extractF1(self, srcSessions):
		#global pyPath
		#pyPath = path
		# get the dialog and judge it
		lines = srcSessions.split('\n')
		dialog = ''
		visitor = ''
		agent = ''
		num = 0
		visitor_num = 0
		count = 0
		f1 = []
		x = ''
		for line in lines:
			if not line or not line.strip():
				continue
        
			if line[0] == '#':
				count += 1 
				if count == 1:
					continue
				x += self.find_word(visitor, 1)
				x += self.find_word(agent, 1)
				x += self.find_word(visitor, visitor_num)
				x += self.find_word(dialog, num)
				f1.append(x)
				x = ''
				dialog = ''
				agent = ''
				visitor = ''
				visitor_num = 0
				num = 0
			elif line.find('Visitor') > 0:
				dialog += line.split('|')[1].split(':')[1].strip()
				visitor += line.split('|')[1].split(':')[1].strip()
				visitor_num += 1
				num += 1
			elif line.find('Agent') > 0:
				dialog += line.split('|')[1].split(':')[1].strip()
				agent += line.split('|')[1].split(':')[1].strip()
				num += 1 

		# 写最后一句
		x += self.find_word(visitor, 1)
		x += self.find_word(agent, 1)
		x += self.find_word(visitor, visitor_num)
		x += self.find_word(dialog, num)
		f1.append(x)
		return f1
