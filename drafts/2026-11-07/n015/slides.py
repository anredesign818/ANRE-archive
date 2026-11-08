from PIL import Image, ImageDraw, ImageFont, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
import numpy as np, glob
W,H=1080,1350; FN='/home/claude/fonts/ANREUnderground.ttf'
def f(s): return ImageFont.truetype(FN,s)
K='/home/claude/kar/src/'; B='/tmp/claude-0/-home-claude/5d96c106-ca2c-514a-bc88-391c7399f298/scratchpad/artifact-files/01fcdebb-e6f2-40e4-9ef2-e66c6f6228dc/'
def k(n): return glob.glob(K+f'{n:02d}_*.jpg')[0]
def base(photo,dark=0.0,top=0.5):
    im=Image.open(photo).convert('RGB')
    s=max(W/im.width,H/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    l=(im.width-W)//2; t=int((im.height-H)*top); im=im.crop((l,t,l+W,t+H))
    a=np.asarray(im).astype(float); y=np.linspace(0,1,H)[:,None,None]
    g=np.clip((y-0.38)/0.42,0,1)**1.1*0.88+np.clip((0.14-y)/0.14,0,1)**0.8*0.55+dark
    return Image.fromarray((a*(1-np.clip(g,0,0.95))).astype('uint8'))
def ct(d,txt,font,yy,fill,tr=0,x0=None):
    w=sum(font.getlength(c) for c in txt)+tr*(len(txt)-1); x=(W-w)/2 if x0 is None else x0
    for c in txt: d.text((x,yy),c,font=font,fill=fill); x+=font.getlength(c)+tr
def wrap(txt,font,mw):
    out,cur=[],''
    for w in txt.split():
        c=(cur+' '+w).strip()
        if font.getlength(c)<=mw or not cur: cur=c
        else: out.append(cur); cur=w
    return out+[cur]
def header(d):
    ct(d,'ANRE  —  NOTES  —  N°015',f(28),56,(240,240,240),4)
    ct(d,'ВИТРУВИЙ СЕГОДНЯ  —  I',f(22),100,(215,215,215),4)
def slide(n,photo,head,body,cap,out,top=0.5,last=False):
    im=base(photo,top=top); d=ImageDraw.Draw(im); header(d)
    bf=f(40); lines=wrap(body,bf,900); lh=54
    yy=H-150-len(lines)*lh
    ct(d,head,f(30),yy-74,(230,230,230),5,90)
    for ln in lines: ct(d,ln,bf,yy,(250,250,250),0,90); yy+=lh
    ct(d,cap,f(18),H-92,(175,175,175),2,90)
    ct(d,'ANREDESIGN.COM' if last else f'{n} / 10',f(20),H-56,(205,205,205),5)
    im.save(out,quality=93)
def cover(photo,out):
    im=base(photo,dark=0.12); d=ImageDraw.Draw(im); header(d)
    ct(d,'CARYATIDS',f(112),H-470,(250,250,250),10)
    ct(d,'Какую историю рассказывают детали',f(44),H-320,(240,240,240))
    ct(d,'Эссе Анастасии Резниковой  —  листайте',f(24),H-250,(200,200,200),3)
    ct(d,'Референсы из открытых источников · права принадлежат авторам'.replace('·','—'),f(16),H-60,(160,160,160),2)
    im.save(out,quality=93)
REF='Референс из открытых источников — права у авторов'; OWN='Фрагмент проекта ANRE'
cover(k(39),'01.jpg')
S=[(k(40),'ORNAMENT IS A MESSAGE','Витрувий писал: архитектор должен знать историю, чтобы объяснять смысл украшений. И его главный пример — кариатиды.',REF,0.5),
 (k(37),'FROZEN PUNISHMENT','Город Карии встал на сторону персов. После победы греки увели его женщин в плен, а архитекторы закрепили это в камне: женщины навечно держат архитрав головой.',REF,0.3),
 (k(38),'THE VOICE OF POWER','Так государство разговаривало с людьми через архитектуру. Она была не только формой — это была застывшая политическая пропаганда. Хоть и очень красивая.',REF,0.5),
 (k(36),'WHAT DO MY DETAILS SAY?','Я за созидание, а не за наказание. Мир форм и пропорции предметов говорят с нами на всех уровнях. Поэтому я выбираю, кто сделал вещь и что за ней стоит.',OWN,0.5),
 (k(28),'LIVING METAL','Atelier 001 — крошечная мастерская светильников в Лондоне. Я была у них в Ноттинг-Хилле. Мастера превращают работу с металлом в алхимию и понимают мой тонкий язык: что такое живой металл.',OWN+' — Atelier 001',0.5),
 (k(5),'SEALED WITH WAX','Apparatus, De Castelli — тоже кастомные мастерские, не для огромных объёмов. Каждый ящик запечатан, на пломбах восковая печать, как раньше на письмах.',OWN,0.5),
 (k(31),'LOVE FIRST','За каждым настоящим брендом стоит заряд любви — как поток, как канал. И только потом он разливается в маркетинг, отделы продаж и премиальные салоны.',OWN,0.4),
 (k(34),'NO SHADOW OF SORROW','Я не собираю вещи, сделанные без радости. Предметы в доме должны рождать радость и достоинство в собственных глазах. Ни одна вещь не должна напоминать, что кому-то от неё было плохо.',OWN+' — De Castelli',0.5),
 (B+'305cf8038bffcc2088b82a8e28355613.jpg','QUIET PROSPERITY','Мои проекты — о победе и красоте. О спокойном процветании, которое не нужно доказывать. Какую историю рассказывают вещи в вашем доме? Строите виллу, дом или пентхаус — напишите мне в Direct.','@anre_architects',0.25)]
for i,(p,h,b,c,t) in enumerate(S):
    slide(i+2,p,h,b,c,f'{i+2:02d}.jpg',top=t,last=(i==8))
