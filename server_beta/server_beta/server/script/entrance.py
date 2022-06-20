# -*- coding: utf-8 -*-
from pubdefines import MSGQUEUE_SEND, MSGQUEUE_RECV, DELAY_TIME
from timer import Call_out

import mq
import script.netcommand as netcommand
import script.user as user

def RecvMq_Handler():
	HANDLE_MAX = 100
	oRecvMq = mq.GetMq(MSGQUEUE_RECV)
	if oRecvMq.empty():
		Call_out(DELAY_TIME, "RecvMq_Handler", RecvMq_Handler)
		return
	iHandled = 0
	while not oRecvMq.empty() and iHandled <= HANDLE_MAX:
		tData = oRecvMq.get()
		iType, iLink, bData = tData
		print("从消息队列中接收到数据 %s %s %s" % (iType, iLink, bData))
		netcommand.NetCommand(tData)
	Call_out(DELAY_TIME, "RecvMq_Handler", RecvMq_Handler)

def run(oSendMq, oRecvMq):
	user.Init()
	mq.SetMq(oSendMq, MSGQUEUE_SEND)
	mq.SetMq(oRecvMq, MSGQUEUE_RECV)
	Call_out(DELAY_TIME, "RecvMq_Handler", RecvMq_Handler)