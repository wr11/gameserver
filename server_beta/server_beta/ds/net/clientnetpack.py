# -*- coding: utf-8 -*-
from pubdefines import MSGQUEUE_SEND, C2S, S2S

import struct
import net.clientlink as clientlink
import mq

def NetPackagePrepare(byteContent = b""):
	return CNetPackage(byteContent)

class CNetPackage:
	def __init__(self, byteContent):
		self.m_BytesBuffer = byteContent
		self.m_Offset = 0

	def PackInto(self, byteContent):
		self.m_BytesBuffer += byteContent

	def Unpack(self, sType):
		iAddOffset = struct.calcsize(sType)
		byteContent = self.m_BytesBuffer[self.m_Offset:self.m_Offset+iAddOffset]
		self.m_Offset += iAddOffset
		return struct.unpack(sType, byteContent)[0]

	def UnpackEnd(self):
		return self.m_BytesBuffer[self.m_Offset:]

def PacketPrepare(header):
	oNetPack = NetPackagePrepare()
	byteHeader = struct.pack("i", header)
	oNetPack.PackInto(byteHeader)
	return oNetPack

def PacketAddI(iVal, oNetPack):
	if not isinstance(iVal, int):
		iVal = int(iVal)
	byteData = struct.pack("i", iVal)
	if byteData:
		oNetPack.PackInto(byteData)

def PacketAddB(bytes, oNetPack):
	oNetPack.PackInto(bytes)

def PacketAddC(char, oNetPack):
	byteData = struct.pack('c', bytes(char.encode("utf-8")))
	if byteData:
		oNetPack.PackInto(byteData)

def PacketAddS(sVal, oNetPack):
	iLen = len(sVal)
	PacketAddI(iLen, oNetPack)
	if iLen == 1:
		PacketAddC(sVal, oNetPack)
	else:
		byteData = struct.pack('%ss' % len(sVal), sVal.encode("utf-8"))
		if byteData:
			oNetPack.PackInto(byteData)

def PacketSend(iLink, oNetPack):
	oMq = mq.GetMq(MSGQUEUE_SEND)
	bData = oNetPack.m_BytesBuffer
	if oMq:
		if oMq.full():
			print("网络延迟中")
			return
		oMq.put((C2S, iLink,bData))
		print("数据 %s 已加入消息队列" % (bData))
	del oNetPack
 
def S2SPacketSend(iLink, oNetPack):
	oMq = mq.GetMq(MSGQUEUE_SEND)
	bData = oNetPack.m_BytesBuffer
	if oMq:
		if oMq.full():
			print("网络延迟中")
			return
		oMq.put((S2S, iLink,bData))
		print("数据 %s 已加入消息队列" % (bData))
	del oNetPack

'''def PacketSend(oNetPack):
	oLink = clientlink.GetLink()
	if oLink and oLink.m_Socket:
		print("数据 %s 打包完毕，发送至服务端" % (oNetPack.m_BytesBuffer))
		oLink.m_Socket.transport.write(oNetPack.m_BytesBuffer)
	del oNetPack'''

def UnpackPrepare(byteData):
	oNetPackage = NetPackagePrepare(byteData)
	return oNetPackage

def UnpackI(oNetPackage):
	return int(oNetPackage.Unpack("i"))

def UnpackC(oNetPackage):
	return oNetPackage.Unpack("c").decode("utf-8")

def UnpackEnd(oNetPackage):
	return oNetPackage.UnpackEnd()

def UnpackS(oNetPackage):
	iLen = UnpackI(oNetPackage)
	if iLen == 1:
		return UnpackC(oNetPackage)
	else:
		return oNetPackage.Unpack("%ss" % iLen).decode("utf-8")