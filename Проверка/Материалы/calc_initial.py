import numpy as np
def metrics(k,ts):
 d=np.array([1.,0.]);
 for T in ts:d=np.polymul(d,[T,1])
 n=np.array([k]); q=np.polyadd(d,n); poles=np.roots(q); den=np.polymul(q,[1,0]); ps=np.roots(den); rs=[np.polyval(n,p)/np.polyval(np.polyder(den),p) for p in ps];t=np.arange(0,3,0.00005);y=sum(r*np.exp(p*t) for r,p in zip(rs,ps)).real
 w=np.logspace(-4,5,100001);h=np.polyval(n,1j*w)/np.polyval(d,1j*w);L=20*np.log10(abs(h));phase=np.unwrap(np.angle(h))*180/np.pi; wc=np.exp(np.interp(0,L[::-1],np.log(w)[::-1]));pm=np.interp(np.log(wc),np.log(w),phase)+180;wp=np.exp(np.interp(-180,phase[::-1],np.log(w)[::-1]));gm=-np.interp(np.log(wp),np.log(w),L)
 print(k,ts,'sigma',100*(y.max()-1),'tr',t[np.flatnonzero(abs(y-1)>0.05)[-1]+1],'PM',pm,'GM',gm,'wc',wc,'poles',poles)
for k in [1.6*np.pi/0.5,11]:
 for Ts in [[.05,.015,.001],[.05,.025,.001],[.04,.025,.001]]: metrics(k,Ts)
