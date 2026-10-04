from lxml import etree
from pathlib import Path
p=Path(r'C:\Users\User\Documents\Индивидуальное задание\Рабочие файлы')
for f in ['xy_demo.xprt','tf_demo.xprt','dynamic_demo.xprt']:
 print('FILE',f);x=etree.parse(str(p/f))
 for i,o in enumerate(x.findall('project/page/object')):
  print(i,o.findtext('name'),o.findtext('class_name'),o.findtext('obj_type'))
  if o.findtext('class_name') in ["'Язык программирования'","'График Y от X'","'Передаточная функция общего вида'","'Сумматор'"]:
   print([(d.findtext('name'),d.findtext('value'),d.findtext('textvalue')) for d in o.findall('custom_props/data')]); (p/(f[:-5]+'_'+str(i)+'.xml')).write_bytes(etree.tostring(o))
