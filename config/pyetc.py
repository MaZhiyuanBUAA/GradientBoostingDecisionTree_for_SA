#coding:utf-8
#pyetc.py
#Python 格式的配置文件支持库
#
import sys,os.path
Module = type(sys)
modules = {}

#导入任意符合Python语法的文件

def load(fullpath,env={},module=Module):
	try:
		code = open(fullpath).read()
	except IOError:
		raise ImportError,'No module named %s'%fullpath
	filename = os.path.basename(fullpath)
	
	try:
		return modules[filename]
	except KeyError:
		pass
	m = module(filename)
	m.__module_class_ = module
	m.__file__ = fullpath
	m.__dict__.update(env)
	exec compile(code,filename,'exec') in m.__dict__
	modules[filename] = m
	return m

#移出已经导入的模块

def unload(m):
	filename = os.path.basename(m.__file__)
	del modules[filename]
	return None
#重新导入模块

def reload(m):
	fullpath = m.__file__
	try:
		code = open(fullpath).read()
	except IOError:
		raise ImportError,'No module named %s'%fullpath
	env = m.__dict__
	module_class = m.__module_class__
	filename = os.path.basename(fullpath)
	m = module_class(filename)
	m.__file__ = fullpath
	m.__dict__.update(env)
	m.__module_class__ = module_class
	exec compile(code,filename,'exec') in m.__dict__
	modules[filename] = m
	return m

