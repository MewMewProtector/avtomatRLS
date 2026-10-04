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
pid=c.c_int64()
filename=str(Path(r'C:\Users\User\Documents\Индивидуальное задание\Рабочие файлы\Схемы\02_Последовательное_КУ.xprt'))
call('OpenProject',[filename,c.byref(pid)],[c.c_wchar_p,c.POINTER(c.c_int64)])
intmethod('CloseProject',pid.value)
call('OpenProject',[filename,c.byref(pid)],[c.c_wchar_p,c.POINTER(c.c_int64)])
call('WaitForAllLoading',[],[])
print('project',pid.value)

g=c.c_int64();call('CreateBlock',[pid.value,0,0,'Временной график',c.byref(g)],[c.c_int64,c.c_int,c.c_int64,c.c_wchar_p,c.POINTER(c.c_int64)])
rv=c.c_int64();call('SetGraphBlockProp',[g.value,'Name',"'StepOut'",c.byref(rv)],[c.c_int64,c.c_wchar_p,c.c_wchar_p,c.POINTER(c.c_int64)])
rv2=c.c_int();call('SetBlockPosition',[g.value,1180.0,400.0,80.0,60.0,0.0,c.byref(rv2)],[c.c_int64,c.c_double,c.c_double,c.c_double,c.c_double,c.c_double,c.POINTER(c.c_int)])
w0=c.c_int64();call('GetPageBlockId',[pid.value,6,c.byref(w0)],[c.c_int64,c.c_int,c.POINTER(c.c_int64)])
sp=c.c_int64();ep=c.c_int64();call('GetOutPort',[w0.value,0,c.byref(sp)],[c.c_int64,c.c_int,c.POINTER(c.c_int64)])
call('GetInPort',[g.value,0,c.byref(ep)],[c.c_int64,c.c_int,c.POINTER(c.c_int64)])
wire=c.c_int64();call('CreateWire',[pid.value,0,0,0,0,sp.value,ep.value,2,c.byref(wire)],[c.c_int64,c.c_int,c.c_int,c.c_int64,c.c_int,c.c_int64,c.c_int64,c.c_int,c.POINTER(c.c_int64)])
intmethod('BlockAfterEdit',g.value)
rv=c.c_int();call('SetPageScript',[pid.value,'finalization eid=getengineofblock(StepOut);gid=getgraphicidbyengine(eid);res=savegraphicscreenshot(gid,2,"C:/Users/User/Documents/Индивидуальное задание/Рабочие файлы/Проверка/fresh_graph.png");end;',1,c.byref(rv)],[c.c_int64,c.c_wchar_p,c.c_int,c.POINTER(c.c_int)])

nb=c.c_int();call('GetPageObjectCount',[pid.value,c.byref(nb)],[c.c_int64,c.POINTER(c.c_int)]);print('objects',nb.value)
for index in range(nb.value):
 b=c.c_int64();call('GetPageBlockId',[pid.value,index,c.byref(b)],[c.c_int64,c.c_int,c.POINTER(c.c_int64)]);intmethod('BlockAfterEdit',b.value)
call('SetProjectRealTimeDelay',[pid.value,0,1.0],[c.c_int64,c.c_int,c.c_double])
intmethod('ProjectStart',pid.value)
class Desc(c.Structure):_fields_=[('dataid',c.c_int64),('type',c.c_int)]
for name in ['project_error_flag','prjinited','time']:
 d=Desc();call('FindProjectData',[name,pid.value,0,c.byref(d)],[c.c_wchar_p,c.c_int64,c.c_int,c.POINTER(Desc)]);v=c.c_double();call('ReadAsFloat',[d,c.byref(v)],[Desc,c.POINTER(c.c_double)]);print(name,d.dataid,d.type,v.value)
t=c.c_double();call('GetProjectTime',[pid.value,c.byref(t)],[c.c_int64,c.POINTER(c.c_double)]);print('time',t.value)

import time as tm
for k in range(10):
 call("ProcessAllMessages",[],[]);tm.sleep(.1)
intmethod('ProjectStep',pid.value)
intmethod('ProjectRun',pid.value)
r=c.c_int64();call("RunTo",[pid.value,8.0,c.byref(r)],[c.c_int64,c.c_double,c.POINTER(c.c_int64)]);print("run result",r.value)
for k in range(20):call("ProcessAllMessages",[],[]);tm.sleep(.1)
call("GetProjectTime",[pid.value,c.byref(t)],[c.c_int64,c.POINTER(c.c_double)]);print("final time",t.value)
intmethod("ProjectStop",pid.value)

call('SaveProjectXML',[pid.value,r'C:\Users\User\Documents\Индивидуальное задание\Рабочие файлы\Проверка\dynamic_loaded.xprt'],[c.c_int64,c.c_wchar_p])


class Variant(c.Structure):
 _fields_=[('vt',c.c_uint16),('r1',c.c_uint16),('r2',c.c_uint16),('r3',c.c_uint16),('data',c.c_uint64),('extra',c.c_uint64)]
for name in ['Объект.y','Задание.r']:
 d=Desc();call('FindProjectData',[name,pid.value,0,c.byref(d)],[c.c_wchar_p,c.c_int64,c.c_int,c.POINTER(Desc)])
 v=Variant();call('ReadAsString',[c.byref(d),c.byref(v)],[c.POINTER(Desc),c.POINTER(Variant)])
 print(name,d.dataid,d.type,v.vt)
 if v.vt==8 and v.data:Path(filename).with_name(name+'.txt').write_text(c.wstring_at(v.data),encoding='utf8')
call('CloseProject',[pid.value],[c.c_int64]);call('SetShutdownOnLastRelease',[1],[c.c_int]);c.WINFUNCTYPE(c.c_ulong,c.c_void_p)(c.cast(p,c.POINTER(c.POINTER(c.c_void_p)))[0][2])(p)
