#coding:utf-8

import pybloomfilter

def creatBf(filename):
	f = file(filename)
	data = f.readlines()
	f.close()
	l = len(data)
	dic = pybloomfilter.BloomFilter(l,0.0001,filename.replace('.txt','.bloom'))
	data = [ele.strip() for ele in data]
	dic.update(data)
	return dic

if __name__ == '__main__':
	filename = 'negetive_evaluate_custom.txt'
	NE = creatBf(filename)
	print NE.capacity
	print NE.error_rate
	print NE.hash_seeds
	print NE.name
	print NE.num_bits
	print NE.num_hashes
