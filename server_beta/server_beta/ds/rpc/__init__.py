# -*- coding: utf-8 -*-
import sys
sys.path.append("rpc")

import rpc.myrpc as myrpc

RemoteCallFunc = myrpc.RemoteCallFunc
Receive = myrpc.Receive
RemoveRpcByLink = myrpc.RemoveRpcByLink
RpcFunctor = myrpc.RpcFunctor
RpcOnlyCBFunctor = myrpc.RpcOnlyCBFunctor