import ctypes as c
from ctypes import wintypes as w
from pathlib import Path
import re
class GUID(c.Structure):
 _fields_=[('a',c.c_uint32),('b',c.c_uint16),('c',c.c_uint16),('d',c.c_ubyte*8)]
 def __init__(self,s):
  import uuid
  super().__init__();c.memmove(c.byref(self),uuid.UUID(s).bytes_le,16)
ole=c.OleDLL('ole32');ole.CoInitialize(None);p=c.c_void_p()
hr=ole.CoCreateInstance(c.byref(GUID('ACE730D7-1712-4C70-87C8-7E4C55622E91')),None,4,c.byref(GUID('145848B3-2BE8-4497-9A6B-8A42DA658844')),c.byref(p))
print('create',hex(hr&0xffffffff),p.value)
src=Path('C:/SimInTech64/source/exe/mmain_TLB.pas').read_text()
part=src[src.index('IMVTU_Server = interface(IDispatch)'):src.index('IMVTU_ServerDisp = dispinterface',src.index('IMVTU_Server = interface(IDispatch)'))]
names=re.findall(r'procedure\s+(\w+)',part)
def call(name,args,types):
 idx=7+names.index(name);vt=c.cast(p,c.POINTER(c.POINTER(c.c_void_p)))[0];f=c.WINFUNCTYPE(c.c_int32,c.c_void_p,*types)(vt[idx]);hr=f(p,*args)
 if hr:print(name,hex(hr&0xffffffff))
 return hr
def intmethod(name,v):return call(name,[v],[c.c_int64])
call('SetMainFormVisible',[0],[c.c_int])
pid=c.c_int64();call('NewProject',[c.byref(pid)],[c.POINTER(c.c_int64)])
for name in ['Передаточная функция общего вида','Язык программирования','Сравнивающее устройтсво','График Y от X','Константа','Временной график','Построение частотных характеристик']:
 b=c.c_int64();call('CreateBlock',[pid.value,0,0,name,c.byref(b)],[c.c_int64,c.c_int,c.c_int64,c.c_wchar_p,c.POINTER(c.c_int64)]);print(name,b.value)
call('SaveProjectXML',[pid.value,r'C:\Users\User\Documents\Индивидуальное задание\Рабочие файлы\Проверка\defaults.xprt'],[c.c_int64,c.c_wchar_p])
