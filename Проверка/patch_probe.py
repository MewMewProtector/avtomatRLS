from pathlib import Path
from lxml import etree
root=Path(r'C:\Users\User\Documents\Индивидуальное задание')
p=root/'Рабочие файлы/Схемы/01_ЛАЧХ.xprt'
x=etree.parse(str(p))
x.find('project/page/script').text="'finalization'#13#10'eid=getengineofblock(ГрафикИсходной); gid=getgraphicidbyengine(eid); res=savegraphicscreenshot(gid,2,\""+(root/'Рабочие файлы/Проверка/L0_SIT.png').as_posix()+"\");'#13#10'end;'"
x.write(str(p),encoding='utf8',xml_declaration=True)
p=root/'Рабочие файлы/Схемы/02_Последовательное_КУ.xprt';x=etree.parse(str(p))
o=x.find('project/page/object');d=next(d for d in o.findall('visual_props/data') if d.findtext('name')=="'Script'");d.find('value').text="'output r;'#13#10'r=1;'"
x.write(str(p),encoding='utf8',xml_declaration=True)
