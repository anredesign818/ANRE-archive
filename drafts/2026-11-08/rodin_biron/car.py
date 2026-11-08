from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
W,H=1080,1350; FN='/home/claude/fonts/ANREUnderground.ttf'
def f(s): return ImageFont.truetype(FN,s)
def ct(d,txt,font,yy,fill,tr=0,x0=None,align='c'):
    w=sum(font.getlength(c) for c in txt)+tr*(len(txt)-1); x=(W-w)/2 if x0 is None else x0
    for c in txt: d.text((x,yy),c,font=font,fill=fill); x+=font.getlength(c)+tr
def wrap(txt,font,mw):
    out,cur=[],''
    for w_ in txt.split():
        c=(cur+' '+w_).strip()
        if font.getlength(c)<=mw or not cur: cur=c
        else: out.append(cur); cur=w_
    return out+[cur]
def base(p,fx=0.5,fy=0.5,grad=0.55,dark=0):
    im=ImageOps.exif_transpose(Image.open(p)).convert('RGB')
    s=max(W/im.width,H/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    l=int((im.width-W)*fx); t=int((im.height-H)*fy); im=im.crop((l,t,l+W,t+H))
    a=np.asarray(im).astype(float); y=np.linspace(0,1,H)[:,None,None]
    g=np.clip((y-0.72)/0.28,0,1)**1.3*grad+np.clip((0.10-y)/0.10,0,1)*0.35+dark
    return Image.fromarray((a*(1-np.clip(g,0,0.92))).astype('uint8'))
def top(d): ct(d,'ANRE  —  NOTES',f(24),46,(235,235,235),4)
def slide(n,p,line,out,fx=0.5,fy=0.5,sub=None):
    im=base(p,fx,fy); d=ImageDraw.Draw(im); top(d)
    ct(d,line,f(38),H-150,(248,248,248))
    if sub: ct(d,sub,f(22),H-100,(210,210,210),3)
    ct(d,f'{n} / 11',f(18),H-56,(190,190,190),4)
    im.save(out,quality=95,subsampling=0)
im=base('orig/002.jpg',0.55,0.5,grad=0.75); d=ImageDraw.Draw(im); top(d)
ct(d,'ОСОБНЯК  БИРОН',f(84),H-330,(250,250,250),8)
ct(d,'Дом, который стал музеем Родена',f(40),H-210,(240,240,240))
ct(d,'ПАРИЖ  —  77 RUE DE VARENNE',f(22),H-150,(205,205,205),5)
ct(d,'листайте',f(20),H-70,(180,180,180),4)
im.save('01.jpg',quality=95,subsampling=0)
S=[('orig/164.jpg','Особняк 1727–1732 годов','архитектор жан обер',0.5,0.5),
('orig/158.jpg','Лестница как скульптура',None,0.5,0.5),
('orig/079.jpg','Буазери и зеркала XVIII века',None,0.5,0.5),
('orig/045.jpg','Мрамор, который дышит',None,0.5,0.5),
('orig/141.jpg','«Собор», 1908',"две правые руки",0.5,0.4),
('orig/113.jpg','Свет из окна — лучший скульптор',None,0.5,0.5),
('orig/082.jpg','Рокайль под потолком',None,0.5,0.5),
('orig/167.jpg','«Три тени» в саду',None,0.45,0.5),
('orig/170.jpg','«Врата ада»',None,0.5,0.5)]
for i,(p,l,s,fx,fy) in enumerate(S): slide(i+2,p,l,f'{i+2:02d}.jpg',fx,fy,s)
im=base('orig/099.jpg',0.5,0.5,grad=0.2,dark=0.62); d=ImageDraw.Draw(im); top(d)
txt=["В 1908 году Роден снял здесь четыре комнаты под мастерские, а с 1911-го занимал весь особняк. Соседями по дому были Матисс, Кокто, Айседора Дункан.",
"Роден не покупал этот дом. Он подарил государству свои работы с условием, что здесь будет его музей. Музей открылся в 1919 году.",
"Дом, который стал продолжением своего хозяина.","А какой дом станет продолжением вас?"]
yy=300
for j,p in enumerate(txt):
    fs=f(42) if j<2 else f(48)
    for ln in wrap(p,fs,880): ct(d,ln,fs,yy,(245,245,245),0,100); yy+=58
    yy+=40
ct(d,'@ANRE_ARCHITECTS  —  ANREDESIGN.COM',f(20),H-70,(200,200,200),4)
im.save('11.jpg',quality=95,subsampling=0)
