import random
import time

if "g_LastTimeStamp" not in globals():
    g_LastTimeStamp = 0
    
def TransUUID2String(iUUID):
    lstText = []
    for i in range(10):
        lstText.append(chr((iUUID >> (8 * i)) & 0xff))
    sUUID = "".join(lstText)
    return sUUID

def SUUID(iServerNum):
    global g_LastTimeStamp
    nanoseconds = time.time() * 1e9
    timestamp = int(nanoseconds / 100) + 0x01b21dd213814000
    if timestamp <= g_LastTimeStamp:
        timestamp = g_LastTimeStamp + 1
    g_LastTimeStamp = timestamp
    return TransUUID2String(timestamp << 20 | iServerNum << 6 | random.randint(0, 1 << 6))

def GetServerByUUID(sUUID):
    iUUID = 0
    for i in range(3):
        iUUID |= (ord(sUUID[i]) << (8 * i))
    iUUID = iUUID >> 6
    iServerNo = iUUID & 0x3fff
    return 4070000 + iServerNo

def Test():
    sUUID = SUUID(4070103)
    print(sUUID)
    iServerNo = GetServerByUUID(sUUID)
    print(iServerNo)
    
if __name__ == "__main__":
    Test()