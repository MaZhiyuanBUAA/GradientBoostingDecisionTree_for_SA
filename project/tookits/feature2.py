# -*- coding: utf-8 -*-
"""
Created on Fri May 06 10:54:15 2016

@author: Richard
"""

def get_x7(dialog):
	num = 0.0
	flag = False
	for sentence in dialog:
		if sentence.find('Visitor') > 0 and flag == False:
			num += 1
		elif sentence.find('Agent') > 0:
			break
	return num

def get_x8(dialog):
	num = 0.0
	for sentence in dialog:
		if sentence.find('Visitor') > 0:
			num = 0.0
		elif sentence.find('Agent') > 0:
			num += 1
	return num

def get_x9(dialog,visitor_num):
	num = 0.0
	for sentence in dialog:
		if len(sentence)<10:
			num += 1
	return num/visitor_num

def calculate_sentence(dialog):
	x = []
	for k in xrange(10):
		x.append(0.0)
	visitor_num = 0.0
	agent_num = 0.0
	visitor_sentence = ''
	agent_sentence = ''
	visitor = []
	for sentence in dialog:
		if sentence.find("Visitor") >= 0:
			visitor_num += 1
			visitor_sentence += sentence.split(':')[1]
			visitor.append(sentence.split(':')[1])
		if sentence.find("Agent") >= 0:
			agent_num += 1
			agent_sentence += sentence.split(':')[1]

	x[0] = visitor_num
	x[1] = agent_num
	x[2] = visitor_num - agent_num
	x[3] = float(len(visitor_sentence))
	x[4] = float(len(agent_sentence))
	if visitor_num != 0 :
		x[5] = float(len(visitor_sentence))/visitor_num
	if agent_num !=0 :
		x[6] = float(len(agent_sentence))/agent_num  
	x[7] = get_x7(dialog)
	x[8] = get_x8(dialog)
	x[9] = get_x9(visitor,visitor_num)
	r = ''    
	for i in x:
		r = r + str(i) + ' '
	return r

class feature2(object):
	def extractF2(self,srcSessions):
		lines = srcSessions.split('\r\n')
		f2=[]
		x = ''
		f2_dialog = []
		dialog_num = 0
		for line in lines:   	
			if  not line or not line.strip():
				continue
			if line[0] == '#':
				dialog_num += 1
				if dialog_num > 1:
					x += calculate_sentence(f2_dialog)
					f2.append(x)
					x = ''
				f2_dialog = []
			else:
				f2_dialog.append(line.split('|')[1].replace('\n', ''))

		x += calculate_sentence(f2_dialog)
		f2.append(x)
		return f2

