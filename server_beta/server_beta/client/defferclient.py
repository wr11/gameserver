# -*- coding: utf-8 -*-

from protocol import C2S_CONNECT
import twisted.internet.defer
import twisted.internet.protocol
import twisted.internet.reactor
import time
import clientnetpack
import clientlink
import timemanager
import mq

SERVER_HOST = "localhost"
SERVER_PORT = 8000

class DeferClient(twisted.internet.protocol.Protocol):
	def connectionMade(self):
		print("【客户端】服务器连接成功")
		oLink = clientlink.GetLink()
		oLink.SetSocket(self)
		#self.send()

	def dataReceived(self, data):
		content = data.decode("utf-8")
		twisted.internet.threads.deferToThread(self.handle_request, content).addCallback(self.handle_success)

	def handle_request(self, content):
		content = content.encode("utf-8")
		print("【客户端】对服务器端数据（%s）进行处理，此处会产生1-2,秒的延迟" % content)
		time.sleep(1)
		oNetPackage = clientnetpack.UnpackPrepare(content)
		iHeader = clientnetpack.UnpackI(oNetPackage)
		iSub = clientnetpack.UnpackS(oNetPackage)
		print(iHeader, iSub)
		return str((iHeader, iSub))

	def handle_success(self, data):
		print("【客户端】处理完成，进行参数接收 %s " % str(data))
		#self.send()

	def send(self):
		input_data = input()
		if input_data:
			oPack = clientnetpack.PacketPrepare(C2S_CONNECT)
			clientnetpack.PacketAddS(input_data, oPack)
			clientnetpack.PacketSend(oPack)
		else:
			self.transport.loseConnection()

class DefaultClientFactory(twisted.internet.protocol.ReconnectingClientFactory):
	protocol = DeferClient

def main(oMq):
	timemanager.Init()
	clientlink.Init()
	mq.SetMq(oMq)
	twisted.internet.reactor.connectTCP(SERVER_HOST, SERVER_PORT, DefaultClientFactory())
	twisted.internet.reactor.run()

'''if __name__ == "__main__":
	clientlink.Init()
	main()'''