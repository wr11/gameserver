# coding:utf-8

import time

#全局注释
#版本信息，客户端和服务端应保持一致
VERSION = 0.1

#连接类型
C2S = 1
S2S = 2
SELF = 3

#服务器地址
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

#消息队列类型
MSGQUEUE_SEND = 1
MSGQUEUE_RECV = 2
DELAY_TIME = 0.1

#全局函数
#全局对象管理
if "g_GloabalManagerDict" not in globals():
	g_GloabalManagerDict = {}
	g_GManagerLimit = {}

def SetGlobalManager(sFlag, oManager, bLimitReplace = True):
	global g_GloabalManagerDict
	global g_GManagerLimit

	oOld = g_GloabalManagerDict.get(sFlag, None)
	if oOld and g_GManagerLimit.get(sFlag, True):
		print("全局管理类 %s 被 %s 替换" % (oOld, oManager))

	g_GloabalManagerDict[sFlag] = oManager
	g_GManagerLimit[sFlag] = bLimitReplace
	if oOld and hasattr(oManager, "OnReplaced"):
		oManager.OnReplaced(oOld)

def DelGlobalManager(sFlag):
	global g_GloabalManagerDict
	global g_GManagerLimit

	if sFlag in g_GloabalManagerDict:
		del g_GloabalManagerDict[sFlag]
	if sFlag in g_GManagerLimit: 
		del g_GManagerLimit[sFlag]

def GetGlobalManager(sFlag):
	global g_GloabalManagerDict
	if sFlag in g_GManagerLimit:
		return g_GloabalManagerDict[sFlag]
	return None

def CallManagerFunc(sFlag, sFunc, *args, **kwargs):
	oManager = GetGlobalManager(sFlag)
	if not oManager:
		raise Exception("无此全局对象 %s" % sFlag)
	func = getattr(oManager, sFunc, None)
	if not func:
		raise Exception("全局对象 %s 中，找不到函数 %s" % (sFlag, sFunc))

	return func(*args, **kwargs)

def GetManagerFunc(sFlag, sFunc):
	oManager = GetGlobalManager(sFlag)
	if not oManager:
		print("无此全局对象 %s" % sFlag)
		return None
	func = getattr(oManager, sFunc, None)
	return func

#----------------time-----------------
Reference_Time = int(time.mktime((2006,10,2,0,0,0,0,0,0)))

def GetNowTime():
    return int(time.time())

def TimeStr(iTime = 0):
    if not iTime:
        iTime = GetNowTime()
    oTime = time.localtime(iTime)
    return time.strftime("%Y-%m-%d %H:%M:%S", oTime)

def GetTimeSec(setTime):
    return int(time.mktime(setTime))

def GetDayNo(iTime = 0):
    if not iTime:
        iTime = GetNowTime()
    iDayNo = (iTime - Reference_Time)/3600/24
    return int(iDayNo) + 1

def GetHourNo(iTime = 0):
    if not iTime:
        iTime = GetNowTime()
    iHourNo = (iTime - Reference_Time)/3600
    return int(iHourNo)

def GetMiniteNo(iTime = 0):
    if not iTime:
        iTime = GetNowTime()
    iMiniteNo = (iTime - Reference_Time)/60
    return int(iMiniteNo)

def GetWeekNo(iTime = 0):
    if not iTime:
        iTime = GetNowTime()
    iWeekNo = (iTime - Reference_Time)/3600/24/7
    return int(iWeekNo)+1

def GetMonthNo(iTime = 0):
    if not iTime:
        iTime = GetNowTime()
    setTime = time.localtime(iTime)
    return (setTime[0] - 2000) *100 + setTime[1]

def GetYearNo(iTime = 0):
    if not iTime:
        iTime = GetNowTime()
    setTime = time.localtime(iTime)
    return setTime[0]

def GetSecByMinNo(iNo):
    return iNo * 60 + Reference_Time

def GetSecByHourNo(iNo):
    return iNo * 3600 + Reference_Time

def GetSecByDayNo(iNo):
    return (iNo - 1) * 3600 * 24 + Reference_Time

def GetSecByWeekNo(iNo):
    return (iNo - 1) * 3600 * 24 * 7 + Reference_Time

def GetSecByMonthNo(iNo):
    return int(time.mktime((iNo/100 + 2000, iNo%100, 1, 0, 0, 0, 0, 0, 0)))

def GetSecByYearNo(iNo):
    return int(time.mktime((iNo, 1, 1, 0, 0, 0, 0, 0, 0)))

def GetDay0Sec(iNo):
    if not iNo:
        iNo = GetDayNo() - 1
    return Reference_Time + iNo * 3600 * 24

def GetDay5Sec(iNo):
    return GetDay0Sec(iNo) + 5*3600

def Get5DayNo(iTime):
    if not iTime:
        iTime = GetNowTime()
    return GetDayNo(iTime - 5*3600)