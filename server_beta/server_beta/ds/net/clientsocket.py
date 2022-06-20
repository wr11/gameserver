# -*- coding: utf-8 -*-
from protocol import SS2S_ESTABLISH
from pubdefines import CallManagerFunc, MSGQUEUE_SEND, MSGQUEUE_RECV, DELAY_TIME, SERVER_NUM,S2S, SELF
import twisted.internet.defer
import twisted.internet.protocol
import twisted.internet.reactor
import net.clientlink as clientlink
import timer
import mq
import net.clientnetpack as cp

SERVER_HOST = "localhost"
SERVER_PORT = 8001

class DeferClient(twisted.internet.protocol.Protocol):
	def connectionMade(self):
		oLink = CallManagerFunc("link", "AddLink", self, S2S)
		self.m_ID = oLink.m_ID
		print("【客户端】服务器连接成功")
		oPack = cp.PacketPrepare(SS2S_ESTABLISH)
		cp.PacketAddI(SERVER_NUM, oPack)
		cp.S2SPacketSend(oLink.m_ID, oPack)
		if not timer.GetTimer("SendMq_Handler"):
			timer.Call_out(DELAY_TIME, "SendMq_Handler", SendMq_Handler)
   
	def connectionLost(self, reason):
		print("与服务器断开连接")
		CallManagerFunc("link", "DelLink", self.m_ID, S2S)
		oRecvMq = mq.GetMq(MSGQUEUE_RECV)
		if oRecvMq:
			oRecvMq.put((SELF, self.m_ID, "disconnect"))

	def dataReceived(self, data):
		oRecvMq = mq.GetMq(MSGQUEUE_RECV)
		if oRecvMq:
			if oRecvMq.full():
				print("数据在加载")
				return
			oRecvMq.put((S2S, self.m_ID, data))
			print("【客户端】收到服务端数据，并已加入消息队列")

	def connectionLost(self, reason):
		print("与服务器断开连接")

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
		print("消息队列数据准备发送至服务端 %s" % bData)
		oLink = CallManagerFunc("link", "GetLink", iLink, iType)
		oLink.m_Socket.transport.getHandle().sendall(bData)
	timer.Call_out(DELAY_TIME, "SendMq_Handler", SendMq_Handler)

class DefaultClientFactory(twisted.internet.protocol.ReconnectingClientFactory):
	protocol = DeferClient

def main(oSendMq, oRecvMq):
	clientlink.Init()
	mq.SetMq(oSendMq, MSGQUEUE_SEND)
	mq.SetMq(oRecvMq, MSGQUEUE_RECV)
	twisted.internet.reactor.connectTCP(SERVER_HOST, SERVER_PORT, DefaultClientFactory())
	twisted.internet.reactor.run()