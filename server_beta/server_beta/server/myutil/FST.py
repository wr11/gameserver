# coding=utf-8

from collections import defaultdict
import random

KEY = 1000000

DATA = [[13140,130,90]]*KEY + [[13141,120,80]]*KEY + [[13142,110,70]]*KEY + [[13143,100,60]]*KEY + [[13144,90,50]]*KEY\
    + [[13145,80,40]]*KEY + [[13146,70,30]]*KEY + [[13147,60,130]]*KEY + [[13148,130,120]]*KEY + [[13149,120,110]]*KEY + [[13150,100,70]]*KEY

ID = 0

class CGoods:
    m_Price = 0
    m_ServerGrade = 0
    m_PlayerGrade = 0
    m_Weight = 0
    m_Storage = defaultdict(int)
    
    def __init__(self, sid, iServerGrade, iPlayerGrade):
        global ID
        ID += 1
        self.m_SID = sid
        self.m_ServerGrade = iServerGrade
        self.m_PlayerGrade = iPlayerGrade
        self.m_ID = ID

    def __repr__(self):
        return "<%s %s %s %s>"%(self.m_ID, self.m_SID, self.m_ServerGrade, self.m_PlayerGrade)

def GenerateListGoods():
    lstGoods = []
    for i in DATA:
        iServerGrade = i[1]
        iPlayerGrade = i[2]
        sid = i[0]
        lstGoods.append(CGoods(sid,iServerGrade,iPlayerGrade))
    return lstGoods

def GenerateFSTGoods(oFST):
    for i in DATA:
        iServerGrade = i[1]
        iPlayerGrade = i[2]
        sid = i[0]
        oGoods = CGoods(sid,iServerGrade,iPlayerGrade)
        oFST.InputState([sid, iServerGrade, iPlayerGrade, oGoods])
    return oFST

'''o=CGoods(100,130,110,50,10001)
print(o.m_Storage)'''

class CStateNode:
    def __init__(self):
        self.m_State = "init"
        self.m_Type = 0
        self.m_NodeMap = {}
        self.m_Data = []

    def __repr__(self):
        return "<tyoe:%s nodemap:%s data:%s>"%(self.m_Type, self.m_NodeMap, self.m_Data)
        
    def SetRoot(self):
        self.m_Type = 1
        
    def SetEnd(self):
        self.m_Type = 2

    def SetState(self, iState):
        self.m_State = iState

    def IsEnd(self):
        return self.m_Type == 2

class CFST:
    def __init__(self, iStateNum):
        self.m_InitNode = None
        self.m_CurNode = None
        self.m_AllState = iStateNum
        self.m_CurState = 1
        self.m_Res = []
        self._InitNode()

    def __repr__(self):
        return "<%s %s %s>"%(self.m_CurNode, self.m_CurState, self.m_Res)
        
    def _InitNode(self):
        oNode = CStateNode()
        oNode.SetRoot()
        self.m_CurNode = oNode
        self.m_InitNode = oNode

    def Reset(self):
        self.m_CurNode = self.m_InitNode
        self.m_CurState = 1
        
    def InputState(self, lstInfo):
        for info in lstInfo:
            self._BuidFloor(info)
        self.Reset()

    def _BuidFloor(self, info):
        if self.m_CurNode.IsEnd():
            self.m_CurNode.m_Data.append(info)
            return
        if info not in self.m_CurNode.m_NodeMap:
            oState = CStateNode()
            oState.SetState(self.m_CurState)
            self.m_CurNode.m_NodeMap[info] = oState
        oState = self.m_CurNode.m_NodeMap[info]
        if self.m_CurState == self.m_AllState:
            oState.SetEnd()
        self.m_CurState += 1
        self.m_CurNode = oState

    def Find(self, lstInfo):
        self.m_Res = []
        for info in lstInfo:
            if not self._FindFloor(info, lstInfo):
                self.Reset()
                return []
        self.Reset()
        return self.m_Res

    def _FindFloor(self, info, lstInfo):
        if info not in self.m_CurNode.m_NodeMap:
            return 0
        self.m_CurNode = self.m_CurNode.m_NodeMap[info]
        self.m_CurState += 1
        if self.m_CurNode.IsEnd():
            self.m_Res = self.m_CurNode.m_Data
            return 1
        if self.m_CurState > len(lstInfo):
            print(self.m_CurNode.m_NodeMap)
            for _, oState in self.m_CurNode.m_NodeMap.items():
                self.SetEndData(oState)
        return 1

    def SetEndData(self, oState):
        if oState.IsEnd():
            self.m_Res += oState.m_Data
            return
        for _, oState1 in oState.m_NodeMap:
            self.SetEndData()

def LstFind(lst):
    r = []
    for o in lst:
        if o.m_SID == 13148 and o.m_ServerGrade == 130 and o.m_PlayerGrade == 120:
            r.append(o)
    return r

if __name__ == "__main__":
    '''oFST = CFST(3)
    oFST.InputState([10,20,30,"whw"])
    oFST.Find([10,20,])
    print(oFST.m_Res)'''
    import time
    print("FST------------------------")
    time0 = time.time()
    oFST = CFST(3)
    GenerateFSTGoods(oFST)
    time1 = time.time()
    oFST.Find([13148,130,120])
    time2 = time.time()
    #print(oFST.m_Res)
    print("structtime: ", time1-time0)
    print("resulttime: ", time2-time1)
    print("FST------------------------")

    print("LST------------------------")
    time5 = time.time()
    lst = GenerateListGoods()
    time3 = time.time()
    r=LstFind(lst)
    time4 = time.time()
    print("LST------------------------")
    #print(r)
    print("structtime: ", time3-time5)
    print("resulttime: ", time4-time3)
    print("LST------------------------")

    print(len(oFST.m_Res),len(r))
