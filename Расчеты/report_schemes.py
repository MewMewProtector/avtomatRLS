from pathlib import Path
import sys
R=Path(r'C:\Users\User\Documents\Индивидуальное задание');sys.path.insert(0,str(R/'Рабочие файлы/Расчёт/packages'))
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
O=R/'Отчёты/Иллюстрации'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
def base(height):
 f,a=plt.subplots(figsize=(7,height));a.set_xlim(0,100);a.set_ylim(100,0);a.axis('off');return f,a
def box(a,x,y,w,h,t,fs=10):
 a.add_patch(Rectangle((x-w/2,y-h/2),w,h,facecolor='white',edgecolor='black',lw=1));a.text(x,y,t,ha='center',va='center',fontsize=fs)
def line(a,pts):
 xx,yy=zip(*pts);a.plot(xx,yy,color='black',lw=1);p,q=pts[-2:];a.annotate('',xy=q,xytext=p,arrowprops={'arrowstyle':'-|>','lw':1,'color':'black'})
f,a=base(4.2)
box(a,18,15,28,20,'Исходная система\nW₀(jω)\nточная / асимптоты')
box(a,18,50,28,20,'Желаемая система\nWж(jω)\nточная / асимптоты')
box(a,56,83,28,20,'Разность Lж − L₀\nточная / асимптоты')
box(a,85,15,24,18,'График L₀')
box(a,85,50,24,18,'График Lж')
box(a,85,83,24,18,'График LКУ')
line(a,[(32,15),(73,15)]);line(a,[(32,50),(73,50)]);line(a,[(70,83),(73,83)])
line(a,[(32,20),(36,20),(36,78),(42,78)])
line(a,[(32,25),(39,25),(39,81),(42,81)])
line(a,[(32,55),(34,55),(34,85),(42,85)])
line(a,[(32,59),(32,89),(42,89)])
a.text(51,9,'ω, Lточн, Lас',ha='center',fontsize=9)
a.text(51,44,'ω, Lточн, Lас',ha='center',fontsize=9)
a.text(86,98,'X — ω, рад/с; Y — L, дБ',ha='center',fontsize=9)
f.tight_layout();f.savefig(O/'08_частотная_схема.png',dpi=240,bbox_inches='tight');plt.close(f)
f,a=base(3.9)
# Folded direct channel, connected around the perimeter.
box(a,9,20,16,16,'r(t)\nступень')
box(a,30,20,16,16,'Σ\nr − y')
box(a,53,20,20,16,'КУ1\nk = 2,0106')
box(a,78,20,20,16,'КУ2')
line(a,[(17,20),(20,20),(20,17),(22,17)])
line(a,[(38,20),(43,20)]);line(a,[(63,20),(68,20)])
box(a,9,57,16,16,'КУ3')
box(a,33,57,20,16,'КУ4')
box(a,61,57,24,16,'Полный W₀\nвариант 9')
line(a,[(88,20),(96,20),(96,40),(1,40),(1,57)])
line(a,[(17,57),(23,57)]);line(a,[(43,57),(49,57)])
line(a,[(73,57),(93,57)]);a.text(91,52,'y(t)',ha='center')
line(a,[(77,57),(77,84),(20,84),(20,23),(22,23)])
a.text(53,33,'Tz = 2,5 с; Tp = 2 с',ha='center',fontsize=9)
a.text(78,33,'Tz = 1 с; Tp = 0,05 с',ha='center',fontsize=9)
a.text(10,75,'Tz = 0,8 с\nTp = 0,015 с',ha='center',fontsize=9)
a.text(34,75,'Tz = 0,5 с\nTp = 0,001 с',ha='center',fontsize=9)
a.text(59,93,'Единичная отрицательная обратная связь',ha='center',fontsize=10)
f.tight_layout();f.savefig(O/'09_динамическая_схема.png',dpi=240,bbox_inches='tight');plt.close(f)
