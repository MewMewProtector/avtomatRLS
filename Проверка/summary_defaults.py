from lxml import etree
x=etree.parse(r'C:\Users\User\Documents\Индивидуальное задание\Рабочие файлы\Проверка\defaults.xprt')
for o in x.findall('project/page/object'):
 print(o.findtext('class_name'),o.findtext('calctemplate'))
 print([(d.findtext('name'),d.findtext('type'),d.findtext('value')) for d in o.findall('custom_props/data')][:8])
