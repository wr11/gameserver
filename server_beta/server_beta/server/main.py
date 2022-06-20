# -*- coding: utf-8 -*-

from pubdefines import MSGQUEUE_SEND, MSGQUEUE_RECV

import multiprocessing
import script
import net
import mq

if __name__ == "__main__":
	mq.Init()

	oSendMq = mq.GetMq(MSGQUEUE_SEND)
	oRecvMq = mq.GetMq(MSGQUEUE_RECV)
	oProcessScript = multiprocessing.Process(target = script.main, args=(oSendMq, oRecvMq, ))
	oProcessNet = multiprocessing.Process(target = net.main, args=(oSendMq, oRecvMq, ))

	oProcessScript.start()
	oProcessNet.start()