# -*- coding: utf-8 -*-

from pubdefines import CSERVER_PORT, MSGQUEUE_SEND, MSGQUEUE_RECV, DELAY_TIME, CallManagerFunc, C2S, S2S, SSERVER_PORT, SELF
from protocol import S2C_CONNECT

import twisted
import twisted.internet.protocol
import twisted.internet.reactor
import net.netpackage as netpackage
import timer
import mq
import net.link as link

#-------------客户端与服务器的连接实例---------------
class CServer(twisted.internet.protocol.Protocol):
	def connectionMade(self):
		oLink = CallManagerFunc("link", "AddLink", self, C2S)
		self.m_ID = oLink.m_ID
		print("客户端已连接%s"%self.m_ID)
		if not timer.GetTimer("SendMq_Handler"):
			timer.Call_out(DELAY_TIME, "SendMq_Handler", SendMq_Handler)

	def connectionLost(self, reason):
		print("客户端 %s 断开连接" % self.m_ID)
		CallManagerFunc("link", "DelLink", self.m_ID, C2S)
		oRecvMq = mq.GetMq(MSGQUEUE_RECV)
		if oRecvMq:
			oRecvMq.put((SELF, self.m_ID, "cdisconnect"))

	def dataReceived(self, data):
		oRecvMq = mq.GetMq(MSGQUEUE_RECV)
		if oRecvMq:
			if oRecvMq.full():
				print("数据在加载")
				return
			oRecvMq.put((C2S, self.m_ID, data))
			print("【C2S】收到客户端数据，并已加入消息队列")

class CBaseServerFactory(twisted.internet.protocol.Factory):
	protocol = CServer

#--------------服务器与服务器的连接实例---------------
class CSubServer(twisted.internet.protocol.Protocol):
	def connectionMade(self):
		oLink = CallManagerFunc("link", "AddLink", self, S2S)
		self.m_ID = oLink.m_ID
		print("其他服务器已连接%s"%self.m_ID)
		if not timer.GetTimer("SendMq_Handler"):
			timer.Call_out(DELAY_TIME, "SendMq_Handler", SendMq_Handler)

	def connectionLost(self, reason):
		print("客户端 %s 断开连接" % self.m_ID)
		CallManagerFunc("link", "DelLink", self.m_ID, S2S)
		oRecvMq = mq.GetMq(MSGQUEUE_RECV)
		if oRecvMq:
			oRecvMq.put((SELF, self.m_ID, "sdisconnect"))

	def dataReceived(self, data):
		oRecvMq = mq.GetMq(MSGQUEUE_RECV)
		if oRecvMq:
			if oRecvMq.full():
				print("数据在加载")
				return
			oRecvMq.put((S2S, self.m_ID, data))
			print("【C2S】收到客户端数据，并已加入消息队列")

class CSubBaseServerFactory(twisted.internet.protocol.Factory):
	protocol = CSubServer

def run(oSendMq, oRecvMq):
	link.Init()
	mq.SetMq(oSendMq, MSGQUEUE_SEND)
	mq.SetMq(oRecvMq, MSGQUEUE_RECV)
	twisted.internet.reactor.listenTCP(CSERVER_PORT, CBaseServerFactory())
	twisted.internet.reactor.listenTCP(SSERVER_PORT, CSubBaseServerFactory())
	print("服务端启动完毕，等待客户端连接")
	twisted.internet.reactor.run()

def SendMq_Handler():
	HANDLE_MAX = 100
	oMq = mq.GetMq(MSGQUEUE_SEND)
	if oMq.empty():
		timer.Call_out(DELAY_TIME, "SendMq_Handler", SendMq_Handler)
		return
	iHandled = 0
	while not oMq.empty() and iHandled <= HANDLE_MAX:
		iHandled += 1
		tData = oMq.get()
		iType, iLink, bData = tData
		print("消息队列数据准备发送至客户端 %s" % bData)
		oLink = CallManagerFunc("link", "GetLink", iLink, iType)
		oLink.m_Socket.transport.getHandle().sendall(bData)
	timer.Call_out(DELAY_TIME, "SendMq_Handler", SendMq_Handler)