# -*- coding: utf-8 -*-

import net.clientnetpack as np

def NetCommand(oNetPackage):
	iSub = np.UnpackS(oNetPackage)
	print("【客户端】数据接收完毕 %s" % iSub)