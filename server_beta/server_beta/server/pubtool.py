# -*- coding: utf-8 -*-

import collections
import pubdefines

class CTimeOutManager:
	def __init__(self):
		self.m_PreTime = pubdefines.GetNowTime()
		self.m_TimeSlot = collections.defaultdict(dict)
		self.m_Flag2TS = {}

	def Push(self, flag, iTime, oTask):		#需要保证flag唯一，否则会有覆盖危险
		if iTime <= 1:
			iTime = 1
		iDDL = pubdefines.GetNowTime() + iTime
		dSlot = self.m_TimeSlot[iDDL]
		dSlot[flag] = oTask
		self.m_Flag2TS[flag] = iDDL
  
	def Pop(self, flag):
		if flag not in self.m_Flag2TS:
			return
		iDDL = self.m_Flag2TS[flag]
		dSlot = self.m_TimeSlot[iDDL]
		oTask = dSlot.pop(flag)
		del self.m_Flag2TS[flag]
		return oTask

	def Get(self, flag):
		if flag not in self.m_Flag2TS:
			return None
		iDDL = self.m_Flag2TS[flag]
		dSlot = self.m_TimeSlot[iDDL]
		return dSlot[flag]

	def PopTimeOut(self):
		iNowTime = pubdefines.GetNowTime()
		lst = []
		for iTime in range(self.m_PreTime, iNowTime+1):
			if iTime not in self.m_TimeSlot:
				continue
			dSlot = self.m_TimeSlot.pop(iTime)
			for flag in dSlot.keys():
				del self.m_Flag2TS[flag]
			lst.extend(dSlot.values())
		self.m_PreTime = iNowTime
		return lst

	def IsEmpty(self):
		return 1 if not len(self.m_Flag2TS) else 0

#单例模式
class Singleton:
	hasinstance=False
	orig_instance=None
	def __new__(cls):
		if cls.hasinstance==False:
			cls.hasinstance=True
			cls.orig_instance=super().__new__(cls)
			return cls.orig_instance
		else:
			return cls.orig_instance

#管理类基类
class BaseManager(Singleton):
	pass

'''
三种Functor:
Functor: 正常的打包函数类
LiteFuctor：轻量级打包函数类
MyFuncotor：增加了错误的输出栈信息，更容易定位错误的位置
'''

import inspect

class Functor:
	def __init__(self, fn, *args, **kwargs):
		self._fn = fn
		self._args = args
		self._kwargs = kwargs
		self.m_Type = ""

	def __call__(self, *args, **kwargs):
		dKwargs = {}
		dKwargs.update(self._kwargs)
		dKwargs.update(kwargs)
		return self._fn(*(self._args + args), **dKwargs)

class LiteFuctor:
	def __init__(self, fn, *args):
		self._fn = fn
		self._args = args

	def __call__(self, *args):
		return self._fn(*(self._args + args))

class MyFuncotor(Functor):
	def __init__(self, fn, *args, **kwargs):
		Functor.__init__(self, fn, *args, **kwargs)
		self.__m_traceinfo = []
		for _, filename, line, fromcode, _, _ in inspect.stack()[1:]:
			self.__m_traceinfo.append((filename, line, fromcode))

	def __call__(self, *args, **kwargs):
		try:
			return super().__call__(*args, **kwargs)
		except Exception as e:
			print('trace' + '-' * 40)
			for filename, line, formcode in self.__m_traceinfo[::-1]:
				print(filename, 'line%s'%line, 'in %s '%formcode)
			print
			raise e