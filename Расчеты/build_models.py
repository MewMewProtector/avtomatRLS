from pathlib import Path
from lxml import etree
from copy import deepcopy
import numpy as np
ROOT=Path(r'C:\Users\User\Documents\Индивидуальное задание')
WORK=ROOT/'Рабочие файлы'
OUT=WORK/'Схемы'
def enc(s):return "'" + str(s).replace("'","''").replace("\n","'#13#10'")+"'"
def un(s):return s.strip("'") if s else ''
def setval(e,tag,value):
 c=e.find(tag)
 if c is None:c=etree.SubElement(e,tag)
 c.text=enc(value)
 return c
def prop(o,group,name,typ,value):
 g=o.find(group)
 if g is None:g=etree.SubElement(o,group)
 d=next((d for d in g.findall('data') if un(d.findtext('name'))==name),None)
 if d is None:d=etree.SubElement(g,'data');setval(d,'name',name);setval(d,'type',typ);setval(d,'mode',2 if group=='visual_props' else 1)
 v=d.find('value')
 if v is None:v=etree.SubElement(d,'value')
 for c in list(v):v.remove(c)
 v.text=enc(value)
 t=d.find('textvalue')
 if t is not None:t.text=None
 return d
def blank(end,h):
 x=etree.parse(str(WORK/'Проверка/Шаблоны/demo.xprt'));pr=x.find('project');page=pr.find('page')
 for o in page.findall('object'):page.remove(o)
 for t in ['signal_list','connect_list','var_list','glprops_list']:
  e=page.find(t)
  if e is not None:page.remove(e)
 setval(page,'script','');setval(page,'x',500);setval(page,'y',300);setval(page,'width',1200);setval(page,'height',800);setval(page,'scalex',1);setval(page,'scaley',1);setval(page,'grid',0);setval(page,'calcany',1)
 for d in pr.findall('layers/layer/parameters/data'):
  n=un(d.findtext('name'))
  if n in {'endtime':end,'hmin':h,'hmax':h,'synstep':h,'intmet':'1','relerr':1e-8,'abserr':1e-10}: setval(d,'value',{'endtime':end,'hmin':h,'hmax':h,'synstep':h,'intmet':'1','relerr':1e-8,'abserr':1e-10}[n]);setval(d,'textvalue','')
 return x,page
def obj(page,name,cls,typ,x,y,w=120,h=60,label=''):
 defaults=etree.parse(str(WORK/'Проверка/defaults.xprt')).findall('project/page/object')
 o=deepcopy(next(d for d in defaults if un(d.findtext('class_name'))==cls));page.append(o);setval(o,'name',name);setval(o,'class_name',cls);setval(o,'obj_type',typ);prop(o,'visual_props','Name',4,name)
 pts=f'[({x} , {y}),({x+w/2} , {y}),({x} , {y-h/2}),({x} , {y+h/2+20})]'
 setval(o,'point_count',4);v=o.find('points');setval(v,'type',26);setval(v,'value',pts)
 for nm,tp,val in [('Points',26,pts),('LabelText',28,label),('Width',0,w),('Height',0,h),('ShowFrame',2,1),('Visible',2,1)]:
  prop(o,'visual_props',nm,tp,val)
 setval(o,'width',w);setval(o,'height',h)
 return o
def ports(o,spec):
 old=o.find('ports')
 if old is not None:o.remove(old)
 ps=etree.SubElement(o,'ports')
 w=float(un(o.findtext('width')));h=float(un(o.findtext('height')))
 import re
 cx,cy=map(float,re.findall(r'\(([^,]+) , ([^)]+)\)',o.findtext('points/value'))[0])
 for name,mode,side,xx,yy in spec:
  p=etree.SubElement(ps,'port')
  for k,v in [('name',name),('mode',mode),('side',side),('x',xx),('y',yy),('auto',1),('type',0),('x_glob',cx+xx*w),('y_glob',cy+yy*h)]:setval(p,k,v)
def portpos(o,k):
 p=o.findall('ports/port')[k];return(float(un(p.findtext('x_glob'))),float(un(p.findtext('y_glob'))))
def wire(page,a,pa,b,pb,via=[]):
 objs=page.findall('object');i=objs.index(a);j=objs.index(b);p1=portpos(a,pa);p2=portpos(b,pb)
 o=deepcopy(etree.parse(str(WORK/'Проверка/Шаблоны/demo.xprt')).findall('project/page/object')[3]);page.append(o);setval(o,'name','Wire'+str(len(objs)));prop(o,'visual_props','Name',4,'Wire'+str(len(objs)))
 for k,v in [('start_bl_index',i),('end_bl_index',j),('start_bl_name',un(a.findtext('name'))),('end_bl_name',un(b.findtext('name'))),('start_port_index',pa),('end_port_index',pb),('parent_wire_index',-1),('directed',1),('branched',0),('parentwirenode',-1)]:setval(o,k,v)
 pts=[p1]+via+[p2];v=o.find('base_points');setval(v,'type',26);ps='['+','.join(f'({x} , {y})' for x,y in pts)+']';setval(v,'value',ps);prop(o,'visual_props','Points',26,ps);setval(o.find('points'),'value',ps);setval(o,'point_count',len(pts))
 return o
def program(page,name,x,y,script,ins,outs,label):
 o=obj(page,name,'Язык программирования',109,x,y,180,max(64,24*max(len(ins),len(outs))),label)
 prop(o,'visual_props','Script',8,script)
 ss=[]
 for arr,mode,side,xx in [(ins,0,0,-.5),(outs,1,2,.5)]:
  for i,n in enumerate(arr):ss.append((n,mode,side,xx,(i-(len(arr)-1)/2)*24/float(un(o.findtext('height')))))
 ports(o,ss);return o
def graph(page,name,x,y,title,count=2):
 t=etree.parse(str(WORK/'Проверка/Шаблоны/xy_demo.xprt')).findall('project/page/object')[0];o=deepcopy(t);page.append(o)
 for tag,val in [('name',name),('width',80),('height',64)]:setval(o,tag,val)
 prop(o,'visual_props','Name',4,name);prop(o,'visual_props','LabelText',28,title)
 pts=f'[({x} , {y}),({x+40} , {y}),({x} , {y-32}),({x} , {y-57})]'
 prop(o,'visual_props','Points',26,pts);setval(o.find('points'),'value',pts);prop(o,'custom_props','count',1,count)
 ports(o,[('X',0,3,0,.5),('Y',0,0,-.5,0)] if count==1 else [('X',0,3,-.25,.5),('X1',0,3,.25,.5),('Y',0,0,-.5,-.25),('Y1',0,0,-.5,.25)])
 eng=o.find('enginedata');setval(eng,'name',title)
 for p in eng.findall('paramlist/param'):setval(p,'blockpath',name)
 plot=eng.find('plot');setval(plot,'title',title);setval(plot,'visible',0);setval(plot,'left',100);setval(plot,'top',100);setval(plot,'right',1100);setval(plot,'bottom',500)
 for font in plot.findall('.//value/height'):
  setval(font.getparent(),'height',17)
 setval(plot.find('titlefont/value'),'height',24)
 setval(plot.find('bottomaxis'),'title','Частота ω, рад/с');setval(plot.find('bottomaxis'),'log',1)
 setval(plot.find('bottomaxis'),'auto',0);setval(plot.find('bottomaxis'),'min',.001);setval(plot.find('bottomaxis'),'max',20000)
 if count==1:
  for series in plot.findall('series/series')[1:]:series.getparent().remove(series)
 setval(plot.find('leftaxis'),'title','Амплитуда L, дБ')
 for s,title in zip(plot.findall('series/series'),['точная ЛАЧХ','асимптотическая ЛАЧХ']):
  setval(s,'title',title);setval(s,'width',2);setval(s,'titlenotdefault',1)
 return o
def save(tree,file):tree.write(str(OUT/file),encoding='utf-8',xml_declaration=True)
N=1401
K=1.6*np.pi/.5
x,page=blank(.01,.001)
base='const n=1401;\noutput w[n], le[n], la[n];\ninitialization\n for (i=1,n) begin\n w[i]=10^(-3+7*(i-1)/(n-1));\n z=complex(0,w[i]);\n'
s0=base+'''
 v=5*(2*z+1)/(z*(2.5*z+1)*(z+1)*(.8*z+1)*(.5*z+1));
 le[i]=20*ln(abs(v))/ln(10);
 la[i]=20*ln(5/w[i])/ln(10)
 +20*max(0,ln(2*w[i])/ln(10))
 -20*max(0,ln(2.5*w[i])/ln(10))
 -20*max(0,ln(w[i])/ln(10))
 -20*max(0,ln(.8*w[i])/ln(10))
 -20*max(0,ln(.5*w[i])/ln(10));
 end;
end;
'''
sj=base+f'''
 v={K:.15g}/(z*(.05*z+1)*(.015*z+1)*(.001*z+1));
 le[i]=20*ln(abs(v))/ln(10);
 la[i]=20*ln({K:.15g}/w[i])/ln(10)
 -20*max(0,ln(.05*w[i])/ln(10))
 -20*max(0,ln(.015*w[i])/ln(10))
 -20*max(0,ln(.001*w[i])/ln(10));
 end;
end;
'''
sk='''const n=1401;
input e0[n],a0[n],ej[n],aj[n];
output w[n],le[n],la[n];
le=ej-e0; la=aj-a0;
for (i=1,n) w[i]=10^(-3+7*(i-1)/(n-1));
'''
a=program(page,'Исходная',200,100,s0,[],['w','le','la'],'Исходная система W0\nточная и асимптоты')
b=program(page,'Желаемая',200,300,sj,[],['w','le','la'],'Желаемая ломаная\nωс=10.053; ωb=20,66.667,1000')
c=program(page,'Разность',660,530,sk,['e0','a0','ej','aj'],['w','le','la'],'ЛАЧХ КУ = Lж − L0\nдва вида характеристик')
g0=graph(page,'ГрафикИсходной',940,100,'Исходная система')
gj=graph(page,'ГрафикЖелаемой',940,300,'Желаемая система')
gk=graph(page,'ГрафикКУ',940,530,'Корректирующее устройство')
for pr,gr,y in [(a,g0,100),(b,gj,300),(c,gk,530)]:
 wire(page,pr,len(pr.findall('ports/port'))-2,gr,2)
 wire(page,pr,len(pr.findall('ports/port'))-1,gr,3)
 for k,xx in [(0,920),(1,960)]:
  pp=portpos(pr,len(pr.findall('ports/port'))-3)
  wire(page,pr,len(pr.findall('ports/port'))-3,gr,k,[(pp[0]+40,pp[1]),(pp[0]+40,y+95),(xx,y+95)])
wire(page,a,1,c,0,[(390,100),(390,494)])
wire(page,a,2,c,1,[(420,124),(420,518)])
wire(page,b,1,c,2,[(450,300),(450,542)])
wire(page,b,2,c,3,[(480,324),(480,566)])
# Export actual SimInTech arrays after calculation
script='finalization\n'
for nm,gr in [('Исходная','ГрафикИсходной'),('Желаемая','ГрафикЖелаемой'),('Разность','ГрафикКУ')]:
 fn=str(WORK/'Расчёт'/(nm+'_SIT.csv')).replace('\\','/')
 script+=f'f=createfile("{fn}",-1);\nfor (i=1,1401) writeln(f,{nm}.w[i],";",{nm}.le[i],";",{nm}.la[i]);\nfreeobject(f);\n'
 script+=f'eid=getengineofblock({gr}); gid=getgraphicidbyengine(eid); savegraphicscreenshot(gid,2,"{(WORK/"Расчёт"/(gr+".png")).as_posix()}");\n'
script+='end;'
setval(page,'script',"finalization\n"+"\n".join('eid=getengineofblock('+nm+'); gid=getgraphicidbyengine(eid); redrawgraphic(gid); res=savegraphicscreenshot(gid,2,\"'+(WORK/'Проверка'/(nm+'.png')).as_posix()+'\");' for nm in ['ГрафикИсходной','ГрафикЖелаемой','ГрафикКУ'])+'\nend;');save(x,'01_ЛАЧХ.xprt')
# Initial prototype of real dynamic cascade
x,page=blank(8,.0001)
r=program(page,'Задание',40,100,'output r;\nr=step(1,0,1);',[],['r'],'Ступень r(t), t0=1 с')
s=obj(page,'Ошибка','Сравнивающее устройтсво',100,200,100,48,48,'e = r − y')
ports(s,[('out',1,2,.5,0),('+',0,0,-.5,-.25),('-',0,0,-.5,.25)])
# b and a in ascending powers, generic matrix type 17 is set through textvalue
def tf(name,xx,y,b,a,label):
 o=obj(page,name,'Передаточная функция общего вида',100,xx,y,100,60,label)
 for n,v in [('b',b),('a',a),('y0',[0])]:
  d=prop(o,'custom_props',n,17,'[['+','.join(f'{z:.15g}' for z in v)+']]')
  setval(d,'textvalue','[['+','.join(f'{z:.15g}' for z in v)+']]')
 ports(o,[('inport',0,0,-.5,0),('outport',1,2,.5,0)])
 return o
c1=tf('КУ1',360,100,[K/5,2.5*K/5],[1,2],'КУ1\nk=2.0106\nTz=2.5; Tp=2')
c2=tf('КУ2',520,100,[1,1],[1,.05],'КУ2\nTz=1; Tp=0.05')
c3=tf('КУ3',680,100,[1,.8],[1,.015],'КУ3\nTz=0.8; Tp=0.015')
c4=tf('КУ4',840,100,[1,.5],[1,.001],'КУ4\nTz=0.5; Tp=0.001')
w0=tf('Объект',1040,100,[5,10],[0,1,4.8,7.45,4.65,1],'Объект W0\nВариант 9')
wire(page,r,0,s,1,[(150,100),(150,88)])
chain=[s,c1,c2,c3,c4,w0]
for a,b in zip(chain[:-1],chain[1:]):wire(page,a,0 if a is s else 1,b,0)
wire(page,w0,1,s,2,[(1130,100),(1130,220),(150,220),(150,112)])
log=program(page,'ЗаписьВыхода',1260,340,'const n=1601;\ninput y;\noutput tt[n],yy[n];\ninitialization\n f=createfile("'+(WORK/'Проверка'/'dynamic_SIT.csv').as_posix()+'",-1);\nfor (i=1,n) begin tt[i]=(i-1)*0.005; yy[i]=0; end;\nend;\ni=round(time/0.005)+1;\nyy[i]=y;\nwriteln(f,time,";",y);\nfinalization\nfreeobject(f);\nend;', ['y'],['tt','yy'],'Выход y(t)\nзапись и история')
wire(page,w0,1,log,0,[(1160,100),(1160,340)])
g=graph(page,'ГрафикВыхода',1560,340,'Переходный процесс после коррекции',count=1)
setval(g.find('enginedata/plot/bottomaxis'),'log',0)
setval(g.find('enginedata/plot/bottomaxis'),'auto',1)
setval(g.find('enginedata/plot/bottomaxis'),'title','Время t, с')
setval(g.find('enginedata/plot/leftaxis'),'title','Выход y(t)')
for s in g.findall('enginedata/plot/series/series'):setval(s,'title','Выход y(t)')
wire(page,log,1,g,0,[(1390,328),(1390,420),(1560,420)])
wire(page,log,2,g,1)
setval(page,'width',1800)
setval(page,'script','finalization\neid=getengineofblock(ГрафикВыхода); gid=getgraphicidbyengine(eid); redrawgraphic(gid); res=savegraphicscreenshot(gid,2,"'+(WORK/'Проверка'/'native_step_chart.png').as_posix()+'");\nend;')
save(x,'02_Последовательное_КУ.xprt')
print('native projects written',K)
