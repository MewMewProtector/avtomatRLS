from pathlib import Path
import sys,re,json
R=Path(r'C:\Users\User\Documents\Индивидуальное задание')
sys.path.insert(0,str(R/'Рабочие файлы/Расчёт/packages'))
from lxml import etree
from PIL import Image,ImageDraw,ImageFont
OUT=R/'Отчёты/Иллюстрации'
def val(s):
 if not s:return ''
 return s.strip("'").replace("'#13#10'","\n").replace("''","'")
def point(s):return [tuple(map(float,m)) for m in re.findall(r'\(([^,]+) , ([^)]+)\)',val(s))]
def draw(f,png):
 x=etree.parse(str(R/'Рабочие файлы/Схемы'/f));objs=x.findall('project/page/object')
 blocks=[o for o in objs if val(o.findtext('class_name'))!='Математическая связь']
 boxes={}
 for o in blocks:
  cx,cy=point(o.findtext('points/value'))[0];w=float(val(o.findtext('width')));h=float(val(o.findtext('height')))
  boxes[val(o.findtext('name'))]=(cx-w/2,cy-h/2,cx+w/2,cy+h/2)
 pts=[p for o in objs if val(o.findtext('class_name'))=='Математическая связь' for p in point(o.findtext('base_points/value'))]
 xs=[v for b in boxes.values() for v in (b[0],b[2])]+[p[0] for p in pts]
 ys=[v for b in boxes.values() for v in (b[1],b[3]+75)]+[p[1] for p in pts]
 xmin=min(xs)-25;xmax=max(xs)+200;ymin=min(ys)-25;ymax=max(ys)+25
 scale=2;im=Image.new('RGB',(int((xmax-xmin)*scale),int((ymax-ymin)*scale)),'white');d=ImageDraw.Draw(im)
 conv=lambda p:((p[0]-xmin)*scale,(p[1]-ymin)*scale)
 font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',26)
 small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',21)
 bad=[]
 # detect line entering any unrelated block; ignore wires crossing other wires
 for o in objs:
  if val(o.findtext('class_name'))!='Математическая связь':continue
  pp=point(o.findtext('base_points/value'))
  start=val(o.findtext('start_bl_name'));end=val(o.findtext('end_bl_name'))
  for a,b in zip(pp[:-1],pp[1:]):
   for name,rect in boxes.items():
    if name in (start,end):continue
    # open rectangle intersection, sampled conservatively
    for k in range(1001):
     t=k/1000;q=(a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1]))
     if rect[0]+.01<q[0]<rect[2]-.01 and rect[1]+.01<q[1]<rect[3]-.01:
      bad.append((val(o.findtext('name')),name));break
  xy=[conv(p) for p in pp];d.line(xy,fill='black',width=3)
  if len(xy)>1:
   a,b=xy[-2:];import math
   dx=b[0]-a[0];dy=b[1]-a[1];l=math.hypot(dx,dy)
   if l:
    ux,uy=dx/l,dy/l;d.polygon([b,(b[0]-12*ux+5*uy,b[1]-12*uy-5*ux),(b[0]-12*ux-5*uy,b[1]-12*uy+5*ux)],fill='black')
 for o in blocks:
  name=val(o.findtext('name'));b=boxes[name];bb=[*conv(b[:2]),*conv(b[2:])]
  d.rectangle(bb,fill='white',outline='black',width=3)
  cx=(bb[0]+bb[2])/2;cy=(bb[1]+bb[3])/2
  internal={'Исходная':'W0(jω)','Желаемая':'Wж(jω)','Разность':'Lж − L0','Задание':'r(t)','Ошибка':'r − y','Объект':'W0(s)','ЗаписьВыхода':'t; y(t)'}.get(name,'График' if 'График' in name else name)
  d.text((cx,cy),internal,font=font,fill='black',anchor='mm')
  lab=next((val(z.findtext('value')) for z in o.findall('visual_props/data') if val(z.findtext('name'))=='LabelText'),'')
  for i,line in enumerate(lab.splitlines()):d.text((cx,bb[3]+6+25*i),line,font=small,fill='black',anchor='mt')
 im.save(OUT/png)
 return sorted(set(bad))
audit={}
audit['frequency']=draw('01_ЛАЧХ.xprt','08_частотная_схема.png')
audit['dynamic']=draw('02_Последовательное_КУ.xprt','09_динамическая_схема.png')
(R/'Рабочие файлы/Проверка/geometry_check.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
print(audit)
