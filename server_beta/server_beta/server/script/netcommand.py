# -*- coding: utf-8 -*-
from protocol import *
from pubdefines import C2S, S2S, CallManagerFunc, SERVER_NUM, SELF

import script.login.net as ln
import net.netpackage as np

RPC_PROTOCOL = [SS2S_RPCRESPONSE, SS2S_RPCCALL, SS2S_RESPONSEERR]

if "g_ServerNum2Link" not in globals():
	g_ServerNum2Link = {}

class CNetCommand:
	def __init__(self):
		self.m_Map = {
			C2S_CONNECT: ln.NetCommand,
		}

	def CallCommand(self, iHeader, oNetPackage, who=None):
		func = self.m_Map.get(iHeader, None)
		func(who, oNetPackage)

def NetCommand(tData):
	import rpc
	iType, iLink, bData = tData
	if iType == SELF:
		OnSelfMessage(iLink, bData)
		return
	oNetPackage = np.UnpackPrepare(bData)
	iHeader = np.UnpackI(oNetPackage)
	if iType == C2S:
		who = CallManagerFunc("user", "GetUser", iLink)
		if not who:
			who = CallManagerFunc("user", "AddUser", iLink)
		print("【服务端】接收头部数据 %s" % iHeader)
		CNetCommand().CallCommand(iHeader, oNetPackage, who)
	elif iType == S2S:
		if iHeader == SS2S_ESTABLISH:
			iServerNum = np.UnpackI(oNetPackage)
			print("服务器编号%s建立channel"%iServerNum)
			g_ServerNum2Link[iServerNum] = iLink
			oPack = np.PacketPrepare(SS2S_ESTABLISH_CONFIRM)
			np.PacketAddI(SERVER_NUM, oPack)
			np.S2SPacketSend(iLink, oPack)
			return
		elif iHeader in RPC_PROTOCOL:
			import rpc.myrpc as rpc
			bData = np.UnpackEnd(oNetPackage)
			rpc.Receive(iHeader, bData)

def OnSelfMessage(iLink, data):
	import rpc
	if data == "cdisconnect":
		who = CallManagerFunc("user", "GetUser", iLink)
		if who:
			who.Quit()
	elif data == "sdisconnect":
		rpc.RemoveRpcByLink(iLink)