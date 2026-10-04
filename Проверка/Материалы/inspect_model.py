from pathlib import Path
from lxml import etree,html
p=Path(r'C:\Users\User\Documents\Индивидуальное задание\Рабочие файлы')
x=etree.parse(str(p/'demo.xprt')); page=x.find('project/page')
for i,o in enumerate(page.findall('object')):
 print(i,o.findtext('name'),o.findtext('class_name'),o.findtext('obj_type'))
 if o.find('custom_props') is not None:
  print([(d.findtext('name'),d.findtext('value'),d.findtext('textvalue')) for d in o.find('custom_props').findall('data')])
 if o.find('ports') is not None: print(etree.tostring(o.find('ports'),encoding='unicode')[:3000])
for f in ['savescreenshot','zoomrect']:
 h=html.parse('C:/SimInTech64/webhelp/11_yazyk_programmirovaniya/6_funkcii/3_graficheskie_i_sistemnye/graficheskie/'+f+'.html'); print(h.find('.//body').text_content()[:6000])
