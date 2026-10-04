from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(r'C:\Users\User\Documents\Индивидуальное задание')
Q=R/'Рабочие файлы/Проверка'
files=[max(Q.glob(n+'*.png'),key=lambda p:p.stat().st_mtime) for n in ['ГрафикИсходной','ГрафикЖелаемой','ГрафикКУ']]
imgs=[Image.open(p).convert('RGB') for p in files]
im=Image.new('RGB',(max(z.width for z in imgs),sum(z.height for z in imgs)+24),'white')
yy=0
font=ImageFont.truetype(r'C:\Windows\Fonts\times.ttf',25)
for z,letter in zip(imgs,'абв'):
 im.paste(z,(0,yy))
 ImageDraw.Draw(im).text((10,yy+7),letter,font=font,fill='black')
 yy+=z.height+8
im.save(R/'Отчёты/Иллюстрации/10_ЛАЧХ_SimInTech.png')
print([str(p.name) for p in files],im.size)
