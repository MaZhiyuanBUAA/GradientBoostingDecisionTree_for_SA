# -*- coding: utf-8 -*-
"""
Created on Fri May 06 10:54:15 2016

@author: Richard
"""
import numpy as np

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
	x = np.zeros(10)
	visitor_num = 0.0
	agent_num = 0.0
	visitor_sentence = ''
	agent_sentence = ''
	visitor = []
	for sentence in dialog:
		if sentence.find("Visitor") >-1:
			visitor_num += 1
			temp = sentence.split('|')[1].split(':')[1]
			visitor_sentence += temp
			visitor.append(temp)
		if sentence.find("Agent") >-1:
			agent_num += 1
			agent_sentence += sentence.split('|')[1].split(':')[1]

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
	return x

class feature2(object):
	def extractF2(self,dialogs):
		f2 = list()
		for dialog in dialogs:
			f2.append(calculate_sentence(dialog))
		return f2

