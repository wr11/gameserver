# -*- coding: utf-8 -*-

from pubdefines import MSGQUEUE_SEND, MSGQUEUE_RECV

import multiprocessing

g_SendMessageQueue = None
g_RecvMessageQueue = None

def Init():
	global g_SendMessageQueue, g_RecvMessageQueue
	if not g_SendMessageQueue:
		g_SendMessageQueue = multiprocessing.Queue()
	if not g_RecvMessageQueue:
		g_RecvMessageQueue = multiprocessing.Queue()

def Put(data, iType):
	global g_SendMessageQueue, g_RecvMessageQueue
	if iType == MSGQUEUE_SEND:
		oQueue = g_SendMessageQueue
	elif iType == MSGQUEUE_RECV:
		oQueue = g_RecvMessageQueue
	if not oQueue:
		return
	if oQueue.full():
		print("网络延迟中，请稍后再试")
		return -1
	oQueue.put(data)
	return 1

def Get(iType):
	global g_SendMessageQueue, g_RecvMessageQueue
	if iType == MSGQUEUE_SEND:
		oQueue = g_SendMessageQueue
	elif iType == MSGQUEUE_RECV:
		oQueue = g_RecvMessageQueue
	if not oQueue:
		return
	if oQueue.empty():
		print("数据加载中，请稍后再试")
		return -1
	return oQueue.get()

def GetMq(iType):
	global g_SendMessageQueue, g_RecvMessageQueue
	if iType == MSGQUEUE_SEND:
		oQueue = g_SendMessageQueue
	elif iType == MSGQUEUE_RECV:
		oQueue = g_RecvMessageQueue
	return oQueue

def SetMq(oMq, iType):
	global g_SendMessageQueue, g_RecvMessageQueue
	if iType == MSGQUEUE_SEND:
		g_SendMessageQueue = oMq
	elif iType == MSGQUEUE_RECV:
		g_RecvMessageQueue = oMq