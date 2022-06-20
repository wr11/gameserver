# -*- coding: utf-8 -*-

import mysql.mysqlbase
import pubdefines
import time

def Init():
	oLinkManager = CUserManager()
	if not pubdefines.GetGlobalManager("user"):
		pubdefines.SetGlobalManager("user", oLinkManager)

class CUser:
	def __init__(self, iLink):
		self.m_ID = 0
		self.m_Login = 0
		self.m_Link = iLink

	def Load(self):
		print("加载用户数据。。。。")
		time.sleep(3)
  
	def Quit(self):
		print("准备下线")

class CUserManager:
	def __init__(self):
		#可以利用玩家ID通过哈希做一些分层
		self.m_Users = {}

	def AddUser(self, iLink):
		oUser = CUser(iLink)
		self.m_Users[iLink] = oUser
		return oUser

	def GetUser(self, iLink):
		return self.m_Users.get(iLink, None)