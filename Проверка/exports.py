import struct
from pathlib import Path
def exports(file):
 d=Path(file).read_bytes();pe=struct.unpack_from('<I',d,60)[0];ns=struct.unpack_from('<H',d,pe+6)[0];opts=struct.unpack_from('<H',d,pe+20)[0];opt=pe+24;magic=struct.unpack_from('<H',d,opt)[0];dd=opt+(112 if magic==523 else 96);er,sz=struct.unpack_from('<II',d,dd);sec=opt+opts
 sections=[struct.unpack_from('<IIII',d,sec+40*i+8) for i in range(ns)]
 def addr(r):
  for vs,va,rs,raw in sections:
   if va<=r<va+max(vs,rs):return r-va+raw
  return r
 e=addr(er);nn,na=struct.unpack_from('<II',d,e+24)[0],struct.unpack_from('<I',d,e+32)[0]
 names=[]
 for i in range(nn):
  r=struct.unpack_from('<I',d,addr(na)+4*i)[0];s=addr(r);names.append(d[s:d.find(b'\0',s)].decode())
 print(file);print('\n'.join(names))
for f in ['mbtylib.dll','Common.dll','mbty_std.dll']:
 exports('C:/SimInTech64/bin/'+f)
