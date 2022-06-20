class CDefaultList(list):
    
    def __init__(self, default=None, num=0):
        super(CDefaultList, self).__init__()
        self.m_Default = default
        if num:
            self.__setitem__(num, self.GetDefault(num, default))
            
    def __setitem__(self, s, o):
        iCur = self.__len__()
        if iCur == 0:
            self.append(self.GetDefault(iCur, o))
            iCur += 1
        if s > iCur - 1:
            for i in range(iCur, s+1):
                self.append(self.GetDefault(i, o))
        super(CDefaultList, self).__setitem__(s, o)
            
    def GetDefault(self, s, o):
        if callable(self.m_Default):
            return self.m_Default(s, o)
        return self.m_Default
'''   
a=CDefaultList(dict(), 10)
print(a)

b=CDefaultList([])
b[10]=12
print(b)
'''


class CRangeDict(dict):
    def __setitem__(self, tRange, v):
        iMin, iMax = tRange[0], tRange[1]
        for i in range(iMax - iMin + 1):
            i = i + iMin
            super(CRangeDict, self).__setitem__(i, v)
'''
b=CRangeDict()
b[10,20] = 45
print(b)
'''