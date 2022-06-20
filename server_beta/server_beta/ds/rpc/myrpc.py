# -*- coding: utf-8 -*-
from io import BytesIO
from script.netcommand import g_ServerNum2Link
from protocol import *
from pubtool import CTimeOutManager
from timer import *

import mq
import pubdefines
import struct
import random
import msgpack
import traceback
import importlib
import net.clientnetpack as np

if "_g_FuncCache" not in globals():
	_g_FuncCache = {}
 
if "g_RPCManager" not in globals():
	g_RPCManager = {}
 
MAX_TIME_OUT = 3600

def GetGlobalFuncByName(sFunc):
	global _g_FuncCache
	func = _g_FuncCache.get(sFunc, None)
	if not func:
		lstPath = sFunc.split(".")
		if len(lstPath) < 2:
			func = None
		else:
			sMod = ".".join(lstPath[:-1])
			sName = lstPath[-1]
			obj = importlib.import_module(sMod)
			func = getattr(obj, sName)
		if not func:
			raise Exception("Erro Global Func Name %s"%sFunc)
		else:
			_g_FuncCache[sFunc] = func
	return func

class CCallBackFunctor:
	def __init__(self, oCBFunc, oTimeoutFunc, args, kwargs):
		self.m_Timeout = 3600
		self.m_TimeoutFunc = oTimeoutFunc
		self.m_CBFunc = oCBFunc
		self.m_args = args
		self.m_kwargs = kwargs
		self.m_Called = 0
  
	def __repr__(self):
		return "<rpc callback %s>"%self.m_CBFunc

	def SetTimeout(self, iTime):
		if iTime > MAX_TIME_OUT or iTime < 1:
			iTime = min(max(1, iTime), MAX_TIME_OUT)
		self.m_Timeout = iTime
  
	def ExecCallBack(self, args, kwargs):
		if not self.m_CBFunc:
			return
		if self.m_Called:
			return
		self.m_Called = 1
		callkwargs = self.m_kwargs.copy()
		callkwargs.update(kwargs)
		callargs = list(self.m_args) + args
		try:
			self.m_CBFunc(*callargs, **callkwargs)
		except:
			raise Exception("rpc回调函数执行错误%s"%(self.m_CBFunc))

	def ExecTimeout(self):
		if not self.m_TimeoutFunc:
			return
		if self.m_Called:
			return
		self.m_Called = 1
		try:
			self.m_TimeoutFunc(self.m_args, self.m_kwargs)
		except:
			raise Exception("rpc超时回调函数执行错误%s"%(self.m_TimeoutFunc))

	def ExecErr(self):
		print("rpc远程端报错%s"%(self.m_CBFunc))

class CRPC:
	def __init__(self):
		self.m_Packet = None
		self.m_CallBackBuff = CTimeOutManager()
		self.m_CBIdx = -1
		self._CheckTimeOut()

	def _CheckTimeOut(self):
		Call_out(5, "_CheckTimeOut", self._CheckTimeOut)
		lst = self.m_CallBackBuff.PopTimeOut()
		if lst:
			for oTask in lst:
				oTask.ExecTimeout()

	def InitCall(self, oCallBack, oPacket, sFunc, *args, **kwargs):
		self.m_Packet = oPacket
		idx = 0
		if oCallBack:
			idx = self._GetCallBackIdx()
			self._AddCallBack(idx, oCallBack)
		self.m_Packet._PushCallPacket((pubdefines.SERVER_NUM, sFunc, idx, args, kwargs))
		return idx

	def CallFunc(self, iLink):
		oPack = np.PacketPrepare(SS2S_RPCCALL)
		np.PacketAddB(self.m_Packet.m_Data, oPack)
		np.S2SPacketSend(iLink, oPack)

	def _GetCallBackIdx(self):
		if self.m_CBIdx == -1:
			self.m_CBIdx = random.randint(0,0xfffffff)
		self.m_CBIdx += 1
		if self.m_CBIdx >= 0x7fffffff:
			self.m_CBIdx = 1
		return self.m_CBIdx

	def _AddCallBack(self, idx, oCallBack):
		self.m_CallBackBuff.Push(idx, self.m_TimeOut, oCallBack)

class CRPCPacket:
	def __init__(self):
		self.m_Data = None

	def _PushCallPacket(self, lstInfo):
		"""
		lstInfo 格式：
		iServerNum: 源服务器编号
		sFunc：远程调用函数名
		CBIdx：回调函数编号
		args：列表参数
		kwargs：字典参数
		"""
		global CMD_CALL
		oBuffer = BytesIO()
		for oParam in lstInfo:
			oBuffer.write(msgpack.packb(oParam, use_bin_type=True))
		self.m_Data = oBuffer.getvalue()

class CRPCResponse:
	def __init__(self, lstInfo):
		self.m_Called = 0
		self.m_SourceServer = lstInfo[0]
		self.m_CallFunc = lstInfo[1]
		self.m_CBIdx = lstInfo[2]
		self.m_Args = lstInfo[3]
		self.m_Kwargs = lstInfo[4]

	def __repr__(self) -> str:
		return "< CRPCResponse ss:%s func:%s CB:%s args:%s kwargs%s>"% \
				(self.m_SourceServer, self.m_CallFunc, self.m_CBIdx, self.m_Args, self.m_Kwargs)

	def __call__(self, *args, **kwargs):
		if not self.m_CBIdx:		#不需要回调
			print("不需要回调")
			return
		if self.m_Called:		#不可重复回调
			return
		self.m_Called = 1
		oPacket = CRPCPacket()
		oPacket._PushCallPacket((pubdefines.SERVER_NUM, self.m_CBIdx, args, kwargs))
		oPack = np.PacketPrepare(SS2S_RPCRESPONSE)
		np.PacketAddB(oPacket.m_Data, oPack)
		iLink = g_ServerNum2Link.get(self.m_SourceServer, 0)
		np.S2SPacketSend(iLink, oPack)

	def RemoteExcute(self):
		func = GetGlobalFuncByName(self.m_CallFunc)
		try:
			func(self, *self.m_Args, **self.m_Kwargs)
		except:
			oPacket = CRPCPacket()
			oPacket._PushCallPacket((pubdefines.SERVER_NUM, self.m_CBIdx))
			oPack = np.PacketPrepare(SS2S_RESPONSEERR)
			np.PacketAddB(oPacket.m_Data, oPack)
			iLink = g_ServerNum2Link.get(self.m_SourceServer, 0)
			np.S2SPacketSend(iLink, oPack)
			raise Exception("远程调用函数执行错误")

def RemoteCallFunc(iServerNum, oCallBack, sFunc, *args, **kwargs):
	print("【server】开始远程调用")
	iLink = g_ServerNum2Link.get(iServerNum, 0)
	if not iLink:
		raise Exception("服务器%s未建立连接" % iServerNum)
	if iServerNum not in g_RPCManager:
		g_RPCManager[iServerNum] = CRPC()
	oRpc = g_RPCManager[iServerNum]
	oPacket = CRPCPacket()
	oRpc.InitCall(oCallBack, oPacket, sFunc, *args, **kwargs)
	oRpc.CallFunc(iLink)

def Receive(iHeader, data):
	oBuffer = BytesIO(data)
	unpacker = msgpack.Unpacker(oBuffer, raw=False)
	lstInfo = [unpacked for unpacked in unpacker]
	print(lstInfo)
	if iHeader == SS2S_RPCCALL:
		oResponse = CRPCResponse(lstInfo)
		oResponse.RemoteExcute()
	elif iHeader == SS2S_RPCRESPONSE:
		_OnResponse(lstInfo)
	elif iHeader == SS2S_RESPONSEERR:
		_OnResponseErr(lstInfo)
  
def _OnResponseErr(lstInfo):
	oRpc = g_RPCManager.get(lstInfo[0], 0)
	if not oRpc:
		print("rpc对象已移除%s"%lstInfo[0])
		return
	oCallBack = oRpc.m_CallBackBuff.Get(lstInfo[1])
	if not oCallBack:
		print("rpc回调对象已移除%s"%lstInfo[1])
		return
	oCallBack.ExecErr()

def _OnResponse(lstInfo):
	oRpc = g_RPCManager.get(lstInfo[0], 0)
	if not oRpc:
		print("rpc对象已移除%s"%lstInfo[0])
		return
	oCallBack = oRpc.m_CallBackBuff.Get(lstInfo[1])
	if not oCallBack:
		print("rpc回调对象已移除%s"%lstInfo[1])
		return
	oCallBack.ExecCallBack(lstInfo[2], lstInfo[3])
	oRpc.m_CallBackBuff.Pop(lstInfo[1])
	if oRpc.m_CallBackBuff.IsEmpty():
		del oRpc
		del g_RPCManager[lstInfo[0]]
  
def RemoveRpcByLink(iLink):
	iNum = 0
	for k,v in g_ServerNum2Link.items():
		if iLink == v:
			iNum = k
			break
	if not iNum:
		return
	del g_ServerNum2Link[iNum]
	if iNum in g_RPCManager:
		del g_RPCManager[iNum]
 
def RpcFunctor(oCBFunc, oTimeoutFunc, *args, **kwargs):
	return CCallBackFunctor(oCBFunc, oTimeoutFunc, args, kwargs)

def RpcOnlyCBFunctor(oCBFunc, *args, **kwargs):
	return CCallBackFunctor(oCBFunc, None, args, kwargs)