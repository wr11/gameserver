# -*- coding: utf-8 -*-

from pubdefines import MSGQUEUE_SEND, MSGQUEUE_RECV, DELAY_TIME
import twisted.internet.defer
import twisted.internet.protocol
import twisted.internet.reactor
import net.clientlink as clientlink
import timer
import mq

SERVER_HOST = "localhost"
SERVER_PORT = 8000

class DeferClient(twisted.internet.protocol.Protocol):
	def connectionMade(self):
		print("【客户端】服务器连接成功")
		oLink = clientlink.GetLink()
		oLink.SetSocket(self)
		timer.Call_out(DELAY_TIME, "SendMq_Handler", SendMq_Handler)

	def dataReceived(self, data):
		oRecvMq = mq.GetMq(MSGQUEUE_RECV)
		if oRecvMq:
			if oRecvMq.full():
				print("数据在加载")
				return
			oRecvMq.put(data)
			print("【客户端】收到服务端数据，并已加入消息队列")

	def connectionLost(self, reason):
		print("与服务器断开连接")
		oRecvMq = mq.GetMq(MSGQUEUE_RECV)
		if oRecvMq:
			oRecvMq.put("disconnect")

def SendMq_Handler():
	HANDLE_MAX = 100
	oMq = mq.GetMq(MSGQUEUE_SEND)
	if oMq.empty():
		timer.Call_out(DELAY_TIME, "SendMq_Handler", SendMq_Handler)
		return
	iHandled = 0
	while not oMq.empty()  and iHandled <= HANDLE_MAX:
		bData = oMq.get()
		print("消息队列数据准备发送至服务端 %s" % bData)
		clientlink.GetLink().m_Socket.transport.getHandle().sendall(bData)
	timer.Call_out(DELAY_TIME, "SendMq_Handler", SendMq_Handler)

class DefaultClientFactory(twisted.internet.protocol.ReconnectingClientFactory):
	protocol = DeferClient

def main(oSendMq, oRecvMq):
	clientlink.Init()
	mq.SetMq(oSendMq, MSGQUEUE_SEND)
	mq.SetMq(oRecvMq, MSGQUEUE_RECV)
	twisted.internet.reactor.connectTCP(SERVER_HOST, SERVER_PORT, DefaultClientFactory())
	twisted.internet.reactor.run()

'''if __name__ == "__main__":
	clientlink.Init()
	main()'''