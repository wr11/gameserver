# -*- coding: utf-8 -*-

from time import sleep
import twisted
import twisted.internet.protocol
import twisted.internet.reactor
import struct
import rpc

SERVER_HOST = "localhost"
SERVER_PORT = 8001

RECEIVE_NUM = 0

def Test(oResPonse, *args, **kwargs):
	print("【client】romtecallfunc：Test",oResPonse, args, kwargs)
	#sleep(20)
	oResPonse(3, {"444":555})

class CClient(twisted.internet.protocol.Protocol):
	def connectionMade(self):
		print("【client】服务器连接成功")

	def send(self):
		pass

	def dataReceived(self, data):
		print("dataReceived", data)
		global RECEIVE_NUM
		RECEIVE_NUM += 1
		if RECEIVE_NUM == 1:
			print("【client】连接序号 %s" % struct.unpack("i",data))
		else:
			print("【client】接收到服务端远程调用请求 %s" % data)
			rpc.Receive(self, data)

class DefaultClientFactory(twisted.internet.protocol.ReconnectingClientFactory):
	protocol = CClient

def main():
	twisted.internet.reactor.connectTCP(SERVER_HOST, SERVER_PORT, DefaultClientFactory())
	twisted.internet.reactor.run()

if __name__ == "__main__":
	main()