# -*- coding: utf-8 -*-

import pubtool

class CClientLink(pubtool.Singleton):
	def __init__(self):
		self.m_Socket = None

	def SetSocket(self, oSocket):
		self.m_Socket = oSocket

g_Link = None

def Init():
	global g_Link
	g_Link = CClientLink()

def GetLink():
	global g_Link
	return g_Link