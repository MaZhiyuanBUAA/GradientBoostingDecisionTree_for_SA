# -*- coding: utf-8 -*-
"""
Created on Fri May 06 18:53:35 2016

@author: Richard
"""

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
		self.label_word.append(get_word(pyPath + '/dict/sorry_word.txt'))
		self.label_word.append(get_word(pyPath + '/dict/thank_word.txt'))
		self.label_word.append(get_word(pyPath + '/dict/wait_word.txt'))
		self.label_word.append(get_word(pyPath + '/dict/urge_word.txt'))
		self.label_word.append(get_word(pyPath + '/dict/dirty_word.txt'))
		self.label_word.append(get_word(pyPath + '/dict/dear_word.txt'))
		self.label_word.append(get_word(pyPath + '/dict/mode_word.txt'))
		self.label_word.append(get_word(pyPath + '/dict/turn_word.txt'))
		self.label_word.append(get_word(pyPath + '/dict/time_word.txt'))
		self.label_word.append(get_word(pyPath + '/dict/ask_word.txt'))
	def valuate(self,s):
		count = []
		for i in xrange(len(self.label_word)):
			count.append(0.0)
		for i in xrange(len(self.label_word)):
			for word in self.label_word[i]:
		    		count[i] += s.count(word)
		return count

#返回值为x列的字符串
	def find_word(self,s,num):
		s1=''
		try:
			s1 = s.decode('utf-8')
		except UnicodeDecodeError:
			print "unicode decode error"
		count = self.valuate(s1)
		x_line = ''
		for i in xrange(len(count)):
			if num == 0:
		    		f = 0.0
			else :
		    		f = count[i]/num
			x_line += str(f) + ' '
		return x_line


	def extractF5(self,srcFile):
		# get the dialog and judge it
		lines = srcFile.split('\n')
		dialog = ''
		visitor = ''
		agent = ''
		agent_num = 0
		visitor_num = 0
		count = 0
		f5=[]
		x = ''
		for line in lines:
			if not line and not line.strip():
				continue
			if line[0] == '#':
				count += 1
				if count == 1:
					continue
				x += self.find_word(visitor, 1)
				x += self.find_word(agent, 1)
				x += self.find_word(visitor, visitor_num)
				x += self.find_word(agent, agent_num)
				f5.append(x)
				x=''
				dialog = ''
				agent = ''
				visitor = ''
				visitor_num = 0
				agent_num = 0
			elif line.find('Visitor') > 0:
				dialog += line.split('|')[1].split(':')[1].replace('\n', ' ')
				visitor += line.split('|')[1].split(':')[1].replace('\n', ' ')
				visitor_num += 1
			elif line.find('Agent') > 0:
				dialog += line.split('|')[1].split(':')[1].replace('\n', ' ')
				agent += line.split('|')[1].split(':')[1].replace('\n', ' ')
				agent_num += 1 #写最后一句

		x += self.find_word(visitor, 1)
		x += self.find_word(agent, 1)
		x += self.find_word(visitor, visitor_num)
		x += self.find_word(agent, agent_num)
		f5.append(x)
		return f5

