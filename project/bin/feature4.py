# -*- coding: utf-8 -*-
"""
Created on Fri May 06 16:22:34 2016

@author: Richard
"""
import numpy as np

def find_sign(dialog):
	x = np.zeros(5)
	for sentence in dialog:
		if not sentence.strip():
			continue
		x[0] += sentence.count('！')
		if sentence.split('|')[1].split(':')[1].strip() == '？':
			x[1] += 1
		x[3] += sentence.count('？')
		if sentence.find('/') >= 0 or sentence.find('[') >= 0:
			x[4] += 1
	x[3] = x[3]/len(dialog)
	x[2] = x[0]/len(dialog)
	return x

class feature4(object):
	def extractF4(self, dialogs):
		f4 = list()
		for dialog in dialogs:
			visitor = list()
			for line in dialog:
				if line.find('Visitor') > -1:
					visitor.append(line)
			s1,s2= find_sign(dialog),find_sign(visitor)
			f4.append(np.hstack((s1,s2)))
		#print f4
		return f4

