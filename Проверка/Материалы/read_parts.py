from lxml import etree,html
from pathlib import Path
p=Path(r'C:\Users\User\Documents\Индивидуальное задание\Рабочие файлы')
x=etree.parse(str(p/'demo.xprt'));o=x.findall('project/page/object')
for i in [0,1,3,4,12]:
 s=etree.tostring(o[i],encoding='unicode');(p/('obj'+str(i)+'.xml')).write_text(s,encoding='utf8')
print(etree.tostring(o[3],encoding='unicode')[-4500:])
