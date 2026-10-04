from pathlib import Path
from lxml import etree
from zipfile import ZipFile
root=Path(r'C:\Users\User\Documents\Индивидуальное задание')
for p in root.glob('*.docx'):
 z=ZipFile(p); x=etree.fromstring(z.read('word/document.xml')); ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
 lines=[]
 for e in x.xpath('//w:body/*',namespaces=ns):
  t=''.join(e.xpath('.//w:t/text() | .//m:t/text()',namespaces=ns))
  if t: lines.append(t)
 (root/'Рабочие файлы'/(p.stem+'.txt')).write_text('\n'.join(lines),encoding='utf-8')
 print(p.name, len(lines), 'media',len([n for n in z.namelist() if n.startswith('word/media/')]))
