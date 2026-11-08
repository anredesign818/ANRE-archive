import subprocess, numpy as np
from PIL import Image, ImageFile, ImageFilter
ImageFile.LOAD_TRUNCATED_IMAGES=True
S=1.12; CARD=3.6; FPS=30; W,H=1080,1920
M='/home/claude/vitr/vo_e.m4a'
B='/tmp/claude-0/-home-claude/5d96c106-ca2c-514a-bc88-391c7399f298/scratchpad/artifact-files/01fcdebb-e6f2-40e4-9ef2-e66c6f6228dc/'
K='/home/claude/kar/src/'
import glob
def k(n): return glob.glob(K+f'{n:02d}_*.jpg')[0]
clips=[(3.0,38.95),(39.4,42.4),(42.85,58.15),(59.15,145.0),(158.7,176.5)]
offs=[];t=0
for a,b in clips: offs.append(t); t+=(b-a)/S
END=t
def mp(x):
    for (a,b),o in zip(clips,offs):
        if a-0.3<=x<=b+0.3: return o+(min(max(x,a),b)-a)/S
    raise SystemExit(f'bad {x}')
# shots: (raw_start, image, mode) mode: 'pan' horizontal pan for landscape, 'in' zoom in, 'out' zoom out, 'up' pan up
shots=[(3.0,k(40),'up'),(9.0,k(39),'in'),(12.7,k(42),'in'),(18.0,k(37),'up'),(26.5,k(38),'out'),
 (31.3,B+'59df7206bf89d0649460eaf12555adc8.jpg','panL'),(34.0,k(41),'in'),
 (39.4,k(1),'in'),(45.9,k(33),'in'),(51.5,k(2),'out'),
 (59.15,k(36),'in'),(64.3,k(23),'in'),(70.0,k(28),'out'),(76.0,k(31),'up'),(82.0,k(24),'in'),(85.3,k(34),'out'),(88.0,k(8),'in'),
 (91.2,k(5),'in'),(96.5,k(7),'out'),(100.6,k(32),'up'),(107.5,k(14),'in'),(114.2,k(12),'out'),(121.0,k(25),'in'),(127.4,k(27),'out'),
 (132.2,k(30),'in'),(140.0,k(3),'up'),(158.7,k(26),'in'),(165.5,B+'305cf8038bffcc2088b82a8e28355613.jpg','in'),(171.3,k(35),'in')]
starts=[mp(s) for s,_,_ in shots]+[END]
grad=np.zeros((H,W,1),np.float32)
for y in range(H):
    g=max(0,(y-H*0.55)/(H*0.45)); g2=max(0,(H*0.12-y)/(H*0.12))
    grad[y]=min(1,g**1.4*0.85+g2*0.45)
def prep(p):
    im=Image.open(p).convert('RGB'); 
    sc=max(W*1.18/im.width, H*1.18/im.height)
    return im.resize((int(im.width*sc),int(im.height*sc)),Image.LANCZOS)
ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
  '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','/home/claude/kar/build/vid.mp4'],stdin=subprocess.PIPE)
N=int(round(END*FPS)); si=-1; XF=0.5
cache={}
def frame(i,t):
    s0,s1=starts[i],starts[i+1]; _,p,mode=shots[i]
    if p not in cache: cache.clear(); cache[p]=prep(p)
    im=cache[p]; u=min(1,max(0,(t-s0)/(s1-s0)))
    u=u*u*(3-2*u)*0.6+u*0.4
    iw,ih=im.size
    if mode in('panL','panR'):
        z=1.0; cw,ch=W/ (iw/ (iw)) ,0
        ch=ih; cw=ih*W/H
        x0=(iw-cw)*(0.15+0.7*(u if mode=='panR' else 1-u)); y0=0
    else:
        z={'in':1.0+0.12*u,'out':1.12-0.12*u,'up':1.06}[mode]
        ch=ih/1.0/ (1.18*z) *1.0; cw=ch*W/H
        if cw>iw: cw=iw; ch=cw*H/W
        x0=(iw-cw)/2; y0=(ih-ch)/2
        if mode=='up': y0=(ih-ch)*(0.75-0.5*u)
    return im.transform((W,H),Image.EXTENT,(x0,y0,x0+cw,y0+ch),Image.BILINEAR)
for f in range(N):
    t=f/FPS
    i=max(j for j in range(len(shots)) if starts[j]<=t+1e-6)
    a=np.asarray(frame(i,t),np.float32)
    # crossfade 0.5s into next shot
    if i+1<len(shots) and starts[i+1]-t<XF:
        w=1-(starts[i+1]-t)/XF; b=np.asarray(frame(i+1,starts[i+1]),np.float32); a=a*(1-w)+b*w
    a=a*(1-grad)
    if t<0.6: a*=t/0.6
    if END-t<0.8: a*=(END-t)/0.8
    ff.stdin.write(a.clip(0,255).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()
print('END',END)
open('/home/claude/kar/build/end.txt','w').write(str(END))
