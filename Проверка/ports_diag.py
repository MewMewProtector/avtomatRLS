from lxml import etree
from pathlib import Path
R=Path(r'C:\Users\User\Documents\Индивидуальное задание')
for f in ['dynamic_demo.xprt','Проверка/defaults.xprt','Схемы/02_Последовательное_КУ.xprt']:
 x=etree.parse(str(R/'Рабочие файлы'/f));print(f)
 for o in x.findall('project/page/object'):
  print(o.findtext('name'),o.findtext('class_name'),o.findtext('obj_type'),[(p.findtext('name'),p.findtext('mode')) for p in o.findall('ports/port')])
