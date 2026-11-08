import json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageOps
d=json.load(open('/home/claude/fuji/list.json'))
seen=set(); jobs=[]
for x in d:
    if not x['path'].upper().endswith('.JPG'): continue
    fid=x['url'].split('id=')[1]
    if fid in seen: continue
    seen.add(fid); jobs.append((fid,x['path']))
meta={}
def one(j):
    fid,name=j
    out=f'/home/claude/fuji/img/{name[:-4]}_{fid[:6]}.jpg'
    if os.path.exists(out): return
    tmp=f'/home/claude/fuji/tmp/{fid}.jpg'
    for a in range(4):
        r=subprocess.run(['gdown','-q',f'https://drive.google.com/uc?id={fid}','-O',tmp],capture_output=True,text=True)
        if os.path.exists(tmp) and os.path.getsize(tmp)>50000: break
        time.sleep(10*(a+1))
    else:
        print('FAIL',name,r.stderr[-200:],flush=True); return
    try:
        im=Image.open(tmp); ex=im.getexif(); dt=ex.get(306) or ''
        try: dt=im._getexif().get(36867,dt)
        except Exception: pass
        im=ImageOps.exif_transpose(im).convert('RGB'); im.thumbnail((2048,2048)); im.save(out,quality=88)
        meta[os.path.basename(out)]={'id':fid,'name':name,'date':str(dt)}
    except Exception as e: print('ERR',name,e,flush=True)
    os.remove(tmp)
with ThreadPoolExecutor(4) as ex:
    for i,_ in enumerate(ex.map(one,jobs)):
        if i%50==0:
            print('done',i,len(jobs),flush=True); json.dump(meta,open('/home/claude/fuji/meta_part.json','w'))
json.dump(meta,open('/home/claude/fuji/meta.json','w')); print('ALLDONE',flush=True)
