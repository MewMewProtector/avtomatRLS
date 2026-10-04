from pathlib import Path
import sys,json
BASE=Path(__file__).parent
sys.path.insert(0,str(BASE/'packages'))
import numpy as np
from scipy import signal,integrate,optimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.labelsize':13,'legend.fontsize':11,'lines.linewidth':1.7})
ROOT=BASE.parent.parent;FIG=ROOT/'Отчёты'/'Иллюстрации';FIG.mkdir(exist_ok=True)
K=1.6*np.pi/.5
n0=np.array([10.,5.]);d0=np.array([1.,4.65,7.45,4.8,1.,0.])
dj=np.polymul(np.polymul([.05,1],[.015,1]),[.001,1]);dj=np.polymul(dj,[1,0])
nj=np.array([K]);qj=np.polyadd(dj,nj);q0=np.polyadd(d0,n0)
nk=(K/5)*np.polymul(np.polymul([2.5,1],[1,1]),np.polymul([.8,1],[.5,1]))
dk=np.polymul([2,1],dj[:-1])
def resp(n,d,t):
 r,p,k=signal.residue(n,np.polymul(d,[1,0]))
 return sum(ri*np.exp(pi*t) for ri,pi in zip(r,p)).real
def margins(n,d):
 def L(w):return 20*np.log10(abs(np.polyval(n,1j*w)/np.polyval(d,1j*w)))
 w=np.logspace(-4,5,50000);ph=np.unwrap(np.angle(np.polyval(n,1j*w)/np.polyval(d,1j*w)))*180/np.pi
 wc=optimize.brentq(L,.0001,1e5);pm=180+np.interp(np.log(wc),np.log(w),ph)
 wp=np.exp(np.interp(-180,ph[::-1],np.log(w)[::-1]));gm=-L(wp)
 return {'wc':wc,'PM':pm,'GM':gm,'wp':wp}
t=np.arange(0,8.00001,.00005);yj=resp(nj,qj,t);y0=resp(n0,q0,t)
sig=100*(yj.max()-1);tr=t[np.flatnonzero(abs(yj-1)>.05)[-1]+1]
e=1-yj;J=integrate.trapezoid(e**2,t);rms=np.sqrt(integrate.cumulative_trapezoid(e**2,t,initial=0)/np.maximum(t,1e-30));rms[0]=abs(e[0])
w=np.unique(np.r_[np.logspace(-3,4,2801),[.4,.5,1,1.25,2,20,40,1/.015,1000]])
s=1j*w
W0=np.polyval(n0,s)/np.polyval(d0,s);Wj=np.polyval(nj,s)/np.polyval(dj,s)
Le0=20*np.log10(abs(W0));Lej=20*np.log10(abs(Wj));Lek=Lej-Le0
def A(T):return 20*np.maximum(0,np.log10(T*w))
La0=20*np.log10(5/w)+A(2)-A(2.5)-A(1)-A(.8)-A(.5)
Laj=20*np.log10(K/w)-A(.05)-A(.015)-A(.001);Lak=Laj-La0
np.savetxt(BASE/'reference_frequency.csv',np.c_[w,Le0,La0,Lej,Laj,Lek,Lak],delimiter=';',header='omega;L0exact;L0asym;Ljexact;Ljasym;Lkexact;Lkasym',comments='')
np.savetxt(BASE/'reference_step.csv',np.c_[t,y0,yj,e],delimiter=';',header='tau;y0;yj;e',comments='')
metrics={'K':K,'sigma':sig,'tr':tr,'tpeak':t[yj.argmax()],'J8':J,'rms8':float(rms[-1]),'original':margins(n0,d0),'corrected':margins(nj,dj),'pol_original':[[p.real,p.imag] for p in np.roots(q0)],'pol_corrected':[[p.real,p.imag] for p in np.roots(qj)],'gain_inf':float(nk[0]/dk[0]),'N0_asc':n0[::-1].tolist(),'D0_asc':d0[::-1].tolist(),'Nk_asc':nk[::-1].tolist(),'Dk_asc':dk[::-1].tolist(),'Nj_asc':nj[::-1].tolist(),'Dj_asc':dj[::-1].tolist()}
phi=Wj/(1+Wj);M=abs(phi).max();metrics['M']=float(M)
# one-sided equivalent bandwidth of unity DC reference/noise channel, in Hz
B=integrate.quad(lambda om: abs(np.polyval(nj,1j*om)/np.polyval(qj,1j*om))**2,0,np.inf,epsabs=1e-10)[0]/(2*np.pi);metrics['B_eq_Hz']=float(B)
print(json.dumps(metrics,ensure_ascii=False,indent=2));(BASE/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf8')
def save(name):
 axes=plt.gcf().axes
 if len(axes)>1:
  for ax,letter in zip(axes,'абвг'):ax.set_title(letter,loc='left',fontsize=14,pad=8)
 plt.tight_layout();plt.savefig(FIG/name,dpi=220,bbox_inches='tight');plt.close()
fig,axs=plt.subplots(3,1,figsize=(9,10),sharex=True)
for ax,le,la,name in zip(axs,[Le0,Lej,Lek],[La0,Laj,Lak],['Исходная система','Желаемая система','Корректирующее устройство']):
 ax.semilogx(w,le,color='black',label='точная');ax.semilogx(w,la,'--',color='#1971a6',label='асимптотическая');ax.axhline(0,color='gray',lw=.8);ax.grid(True,which='both',alpha=.25);ax.set_ylabel('L, дБ');ax.set_title(name);ax.legend(loc='lower left')
axs[-1].set_xlabel('Частота ω, рад/с');save('01_три_ЛАЧХ.png')
fig,ax=plt.subplots(figsize=(9,5))
for a,n,c in [(La0,'исходная L0','black'),(Laj,'желаемая Lж','#1971a6'),(Lak,'разность LКУ','#c05c21')]:ax.semilogx(w,a,label=n,color=c)
ax.axvline(K,color='gray',ls=':');ax.axhline(0,color='gray',lw=.8);ax.set_ylim(-120,140);ax.set_xlim(.1,2000);ax.set_xlabel('Частота ω, рад/с');ax.set_ylabel('Асимптотическая амплитуда L, дБ');ax.legend();ax.grid(True,which='both',alpha=.3);save('02_синтез_ломаных.png')
fig,axs=plt.subplots(2,1,figsize=(9,7),sharex=True)
for a,lab,color in [(W0,'исходный контур','black'),(Wj,'скорректированный контур','#1971a6')]:
 axs[0].semilogx(w,20*np.log10(abs(a)),label=lab,color=color)
 axs[1].semilogx(w,np.unwrap(np.angle(a))*180/np.pi,label=lab,color=color)
axs[0].axhline(0,color='gray',ls=':');axs[1].axhline(-180,color='gray',ls=':');axs[0].set_ylabel('L, дБ');axs[1].set_ylabel('Фаза φ, град');axs[1].set_xlabel('Частота ω, рад/с')
for ax in axs:ax.grid(True,which='both',alpha=.3);ax.legend()
save('03_запасы.png')
fig,axs=plt.subplots(2,1,figsize=(9,7))
axs[0].plot(t,y0,color='black',label='исходная система');axs[0].plot(t,yj,color='#1971a6',label='с КУ');axs[0].set_xlim(0,8);axs[0].set_ylabel('Выход y');axs[0].legend();axs[0].grid(alpha=.3)
axs[1].plot(t,yj,color='#1971a6');axs[1].axhspan(.95,1.05,color='#999999',alpha=.2);axs[1].axhline(1,color='black',ls=':');axs[1].axvline(tr,color='black',ls='--',label=f'tр = {tr:.4f} с');axs[1].set_xlim(0,1.2);axs[1].set_ylabel('Выход y');axs[1].set_xlabel('Время после ступени τ, с');axs[1].legend();axs[1].grid(alpha=.3);save('04_переходные.png')
fig,axs=plt.subplots(2,2,figsize=(9,6))
for ax,val,label in zip(axs.ravel(),[e,e**2,integrate.cumulative_trapezoid(e**2,t,initial=0),rms],['Ошибка e','Квадрат ошибки e²','ИКО J','СКЗ ошибки']):
 ax.plot(t,val,color='#1971a6');ax.set_xlim(0,2);ax.set_xlabel('τ, с');ax.set_ylabel(label);ax.grid(alpha=.3)
save('05_ошибки_ступени.png')
tt=np.arange(0,8.0001,.0005)
fig,axs=plt.subplots(2,1,figsize=(9,6))
for ax,r,lab in [(axs[0],tt,'Линейное задание r = τ'),(axs[1],tt**2/2,'Квадратичное задание r = τ²/2')]:
 _,y,_=signal.lsim((nj,qj),r,tt);ax.plot(tt,r-y,label='расчётная ошибка');ax.set_title(lab);ax.set_ylabel('e');ax.set_xlabel('τ, с');ax.grid(alpha=.3);ax.legend()
axs[0].axhline(1/K,color='black',ls=':');axs[1].plot(tt,tt/K+(.066-1/K)/K,'--',color='black',label='низкочастотная оценка');save('06_ошибки_слежения.png')
fig,axs=plt.subplots(2,1,figsize=(9,6))
for factor in [.8,1,1.2]:
 y=resp(nj*factor,np.polyadd(dj,nj*factor),tt)
 axs[0].plot(tt,y,label=f'усиление объекта ×{factor:g}')
 axs[1].semilogx(w,20*np.log10(abs(Wj*factor)),label=f'×{factor:g}')
axs[0].set_xlim(0,1.2);axs[0].set_xlabel('τ, с');axs[0].set_ylabel('y');axs[1].set_xlim(.1,1000);axs[1].set_xlabel('ω, рад/с');axs[1].set_ylabel('L, дБ')
for ax in axs:ax.grid(alpha=.3);ax.legend()
save('07_чувствительность.png')
