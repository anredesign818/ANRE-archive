import sys; sys.path.insert(0,'/home/claude/n015')
from PIL import Image, ImageDraw, ImageFont, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES=True
import numpy as np, glob
W,H=1000,1500; FN='/home/claude/fonts/ANREUnderground.ttf'
def f(s): return ImageFont.truetype(FN,s)
K='/home/claude/kar/src/'
def k(n): return glob.glob(K+f'{n:02d}_*.jpg')[0]
def ct(d,txt,font,yy,fill,tr=0):
    w=sum(font.getlength(c) for c in txt)+tr*(len(txt)-1); x=(W-w)/2
    for c in txt: d.text((x,yy),c,font=font,fill=fill); x+=font.getlength(c)+tr
def pin(photo,line,out,top=0.5):
    im=Image.open(photo).convert('RGB'); s=max(W/im.width,H/im.height)
    im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    l=(im.width-W)//2; t=int((im.height-H)*top); im=im.crop((l,t,l+W,t+H))
    a=np.asarray(im).astype(float); y=np.linspace(0,1,H)[:,None,None]
    g=np.clip((y-0.78)/0.22,0,1)**1.2*0.7
    im=Image.fromarray((a*(1-g)).astype('uint8')); d=ImageDraw.Draw(im)
    ct(d,line,f(40),H-150,(248,248,248))
    ct(d,'ANRE  —  VITRUVIUS TODAY',f(20),H-86,(210,210,210),5)
    im.save(out,quality=93)
P=[(k(39),'Every ornament is a message',0.5),(k(28),'Living metal',0.5),(k(34),'Metal that remembers the sky',0.5),
   (k(23),'Light as a quiet presence',0.45),(k(5),'Love first, marketing later',0.5),(k(31),'Quiet prosperity',0.4)]
for i,(p,l,t) in enumerate(P): pin(p,l,f'pin{i+1}.jpg',t)
