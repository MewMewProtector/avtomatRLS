from lxml import etree
from pathlib import Path
R=Path(r'C:\Users\User\Documents\Индивидуальное задание')
for f in ['dynamic_demo.xprt','Проверка/defaults.xprt']:
 x=etree.parse(str(R/'Рабочие файлы'/f))
 for o in x.findall('project/page/object'):
  if o.findtext('class_name')=="'Временной график'":
   print(f,o.findtext('name'));print(etree.tostring(o,encoding='unicode')[:2500]);print('engine',etree.tostring(o.find('enginedata'),encoding='unicode')[:3500] if o.find('enginedata') is not None else None)
