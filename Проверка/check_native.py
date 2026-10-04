from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parents[1]/'Расчёт/packages'))
import numpy as np
from scipy.integrate import quad
R=Path(r'C:\Users\User\Documents\Индивидуальное задание')
a=np.loadtxt(R/'Рабочие файлы/Проверка/dynamic_SIT.csv',delimiter=';')
ix=np.r_[np.where(np.diff(a[:,0])!=0)[0],len(a)-1]
a=a[ix];t=a[:,0]-1;y=a[:,1];s=t>=0;t=t[s];y=y[s]
o=np.flatnonzero(np.abs(y-1)>.05)
print('native',len(t),'peak',y.max(),'time',t[y.argmax()],'sigma',100*(y.max()-1),'tp',t[o[-1]+1])
K=1.6*np.pi/.5
f=lambda w:abs(K/(K+1j*w+.066*(1j*w)**2+.000815*(1j*w)**3+7.5e-7*(1j*w)**4))**2
print('Beq',quad(f,0,np.inf,epsabs=1e-10)[0]/(2*np.pi))
np.savetxt(R/'Рабочие файлы/Расчёт/native_step.csv',a,delimiter=';',header='time;y',comments='')
