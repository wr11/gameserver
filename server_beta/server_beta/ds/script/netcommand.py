# -*- coding: utf-8 -*-

from protocol import *
from pubdefines import S2S, SELF, CallManagerFunc

import script.clientlogin.net as cn
import net.clientnetpack as clientnetpack

RPC_PROTOCOL = [SS2S_RPCRESPONSE, SS2S_RPCCALL]

if "g_ServerNum2Link" not in globals():
	g_ServerNum2Link = {}

class CNetCommand:
	def __init__(self):
		self.m_Map = {
			S2C_CONNECT: cn.NetCommand,
		}

	def CallCommand(self, iHeader, oNetPackage):
		func = self.m_Map.get(iHeader)
		func(oNetPackage)

def NetCommand(tData):
	import rpc
	iType, iLink, bData = tData
	if iType == SELF:
		OnSelfMessage(iLink, bData)
		return
	oNetPackage = clientnetpack.UnpackPrepare(bData)
	iHeader = clientnetpack.UnpackI(oNetPackage)
	if iType == S2S:
		if iHeader in RPC_PROTOCOL:
			bData = clientnetpack.UnpackEnd(oNetPackage)
			rpc.Receive(iHeader, bData)
		elif iHeader == SS2S_ESTABLISH_CONFIRM:
			iServerNum = clientnetpack.UnpackI(oNetPackage)
			print("服务器编号%s建立channel"%iServerNum)
			g_ServerNum2Link[iServerNum] = iLink
		else:
			#iSub = clientnetpack.UnpackS(oNetPackage)
			print("【客户端】接收头部数据 %s" % iHeader)
			CNetCommand().CallCommand(iHeader, oNetPackage)
   
def OnSelfMessage(iLink, data):
	import rpc
	if data == "disconnect":
		rpc.RemoveRpcByLink(iLink)