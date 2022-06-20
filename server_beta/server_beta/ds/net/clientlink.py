# -*- coding: utf-8 -*-

import pubdefines

if "g_ClientNum" not in globals():
	g_ClientNum = 0

def Init():
	oLinkManager = CLinkManager()
	if not pubdefines.GetGlobalManager("link"):
		pubdefines.SetGlobalManager("link", oLinkManager)

class CLinkObject:
	def __init__(self, oServerProtocol, iType):
		self.m_ID = 0
		self.m_Socket = oServerProtocol
		self.m_Type = iType

class CLinkManager:
	def __init__(self):
		self.m_CLinkList = {}
		self.m_SLinkList = {}

	def _GetListName(self, iType):
		if iType == pubdefines.C2S:
			return "m_CLinkList"
		elif iType == pubdefines.S2S:
			return "m_SLinkList"
		else:
			return ""

	def AddLink(self, oServerProtocol, iType):
		global g_ClientNum
		oLink = CLinkObject(oServerProtocol, iType)
		sListName = self._GetListName(iType)
		if not sListName:
			return None
		dLink = getattr(self, sListName)
		if g_ClientNum not in dLink:
			dLink[g_ClientNum] = oLink
			oLink.m_ID = g_ClientNum
			g_ClientNum += 1
		return oLink

	def DelLink(self, iLink, iType):
		sListName = self._GetListName(iType)
		if not sListName:
			return
		dLink = getattr(self, sListName)
		if iLink not in dLink:
			return
		del dLink[iLink]
		setattr(self, sListName, dLink)

	def GetLink(self, iLink, iType):
		sListName = self._GetListName(iType)
		if not sListName:
			return None
		return getattr(self, sListName).get(iLink, None)