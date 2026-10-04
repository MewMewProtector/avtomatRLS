from lxml import etree
from pathlib import Path
p=Path(r'C:\Users\User\Documents\Индивидуальное задание\Рабочие файлы')
x=etree.parse(str(p/'Проверка/dynamic_loaded.xprt'))
for o in x.findall('project/page/object'):
 if o.findtext('obj_type')!="'101'":
  print(o.findtext('name'),o.findtext('class_name'),o.findtext('extmodulname'))
  print([(d.findtext('name'),d.findtext('type'),d.findtext('value'),d.findtext('textvalue')) for d in o.findall('custom_props/data')])
