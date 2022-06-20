'''import struct
res=struct.pack("i", 1)
res2=struct.pack("4s", b"good")
u = struct.unpack("i", res2)
print(res2, type(res2))
print(u, type(u))'''

'''import msgpack
msg = msgpack.pack({1:2,"name":"arr"})
msg2=msgpack.unpack(msg)
print(msg)
print(msg2)'''

import  struct
import binascii
import ctypes
import msgpack

msg = msgpack.packb({1:2,"name":"arr"})
print(msg)
 
'''values = (1, b'good' , 1.22) #查看格式化字符串可知，字符串必须为字节流类型。
s =  struct .Struct( 'I4sf' )
buff = ctypes.create_string_buffer(s.size)
packed_data = s.pack_into(buff,0,*values)
unpacked_data = s.unpack_from(buff,0)
  
print( 'Original values:' , values)
print( 'Format string :' , s.format)
print( 'buff :' , buff)
print( 'Packed Value :' , binascii.hexlify(buff))
print( 'Unpacked Type :' , type(unpacked_data),  ' Value:' , unpacked_data)'''