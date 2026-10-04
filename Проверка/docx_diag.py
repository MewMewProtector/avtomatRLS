from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
R=Path(r'C:\Users\User\Documents\Индивидуальное задание')
d=Document(R/'Отчёты/РПЗ_Последовательная_коррекция.docx')
for n in ['Normal','Heading 1','Heading 2','TOC 1','TOC 2']:
 print(n,d.styles[n]._element.xml)
o=d.element.findall('.//'+qn('m:oMath'))[0];print('equation',o.xml[:2000])
print('oMathPara',len(d.element.findall('.//'+qn('m:oMathPara'))))
