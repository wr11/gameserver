# -*- coding: utf-8 -*-

from protocol import *

import script.clientlogin.net as cn
import net.clientnetpack as clientnetpack

class CNetCommand:
	def __init__(self):
		self.m_Map = {
			S2C_CONNECT: cn.NetCommand,
		}

	def CallCommand(self, iHeader, oNetPackage):
		func = self.m_Map.get(iHeader)
		func(oNetPackage)

def NetCommand(bData):
	if bData == "disconnect":
		print("服务器断开连接")
		return
	else:
		oNetPackage = clientnetpack.UnpackPrepare(bData)
		iHeader = clientnetpack.UnpackI(oNetPackage)
		#iSub = clientnetpack.UnpackS(oNetPackage)
		print("【客户端】接收头部数据 %s" % iHeader)
		CNetCommand().CallCommand(iHeader, oNetPackage)