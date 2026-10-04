from lxml import etree
p=r'C:\Users\User\Documents\Индивидуальное задание\Рабочие файлы\Проверка\frequency_loaded.xprt'
x=etree.parse(p)
print('page script',x.findtext('project/page/script')[:700])
print([(d.findtext('name'),d.findtext('value'),d.findtext('textvalue')) for d in x.findall('project/layers/layer/parameters/data')][:10])
for o in x.findall('project/page/object')[:3]:
 print(o.findtext('name'),o.findtext('calctemplate'))
 print([(d.findtext('name'),d.findtext('value')[:150] if d.findtext('value') else '') for d in o.findall('visual_props/data') if d.findtext('name')=="'Script'"])
print([(o.findtext('name'),len(o.findall('ports/port'))) for o in x.findall('project/page/object')[:6]])
