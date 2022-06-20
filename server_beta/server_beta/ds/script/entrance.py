from pubdefines import MSGQUEUE_SEND, MSGQUEUE_RECV, DELAY_TIME

import mq
import timer
import script.netcommand as netcommand
import script.clientui as clientui

def RecvMq_Handler():
	HANDLE_MAX = 100
	oRecvMq = mq.GetMq(MSGQUEUE_RECV)
	if oRecvMq.empty():
		timer.Call_out(DELAY_TIME, "RecvMq_Handler", RecvMq_Handler)
		return
	iHandled = 0
	while not oRecvMq.empty() and iHandled <= HANDLE_MAX:
		iHandled += 1
		tData = oRecvMq.get()
		iType, iLink, bData = tData
		print("从消息队列中接收到数据 %s %s %s" % (iType, iLink, bData))
		netcommand.NetCommand(tData)
	timer.Call_out(DELAY_TIME, "RecvMq_Handler", RecvMq_Handler)

def main(oSendMq, oRecvMq):
	mq.SetMq(oSendMq, MSGQUEUE_SEND)
	mq.SetMq(oRecvMq, MSGQUEUE_RECV)
	timer.Call_out(DELAY_TIME, "RecvMq_Handler", RecvMq_Handler)
	#clientui.main()