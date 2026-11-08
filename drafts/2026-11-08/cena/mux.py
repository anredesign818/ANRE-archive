import subprocess
S=1.12; CARD=3.6
clips=[(1.5,122.2)]
offs=[];t=0
for a_,b_ in clips: offs.append(t); t+=(b_-a_)/S
END=t
def mp(x):
    for (a_,b_),o in zip(clips,offs):
        if a_-0.3<=x<=b_+0.3: return o+(min(max(x,a_),b_)-a_)/S
    raise SystemExit(f'bad {x}')
subs=[(1.6,3.7,"Цена — это мировоззрение."),
(4.6,8.1,"Когда вы приходите в премиальный салон и покупаете вещь,"),
(8.7,13.4,"вам не делают раскладку: сколько стоит доставка, аренда, зарплаты, налоги."),
(13.6,15.1,"У вас просто есть цена."),
(15.5,19.2,"Я — бренд. И клиент приходит ко мне как к бренду."),
(19.9,24.2,"Моя задача не взять больше, а уравновесить все процессы."),
(24.5,29.3,"Я выбираю тишину, покой и людей, которые любят своё дело."),
(29.9,34.5,"Я сама спокойно переплачиваю 10–15%, куда бы я ни посмотрела,"),
(34.8,37.9,"за спокойную красивую жизнь среди счастливых людей."),
(38.5,41.9,"Лампу можно купить за 3000 рублей на маркетплейсе,"),
(42.2,46.5,"а можно в Atelier 001 за 20 тысяч евро. Размер одинаковый."),
(47.0,55.0,"Разница в цене — это разница во взгляде на жизнь, в философии и ценностях тех, кто создаёт, и тех, кто выбирает."),
(55.4,59.8,"А что такое ценности? Это решения, которые мы принимаем на этапе сметы."),
(60.1,66.4,"Можно сэкономить: товар поедет в полусвободном контейнере, и мы получим его через полгода."),
(67.0,68.2,"А может быть, через полтора."),
(69.2,74.7,"А можно, чтобы всё пришло ровно через четыре месяца и хранилось в отдельном помещении,"),
(74.7,77.8,"где каждая коробочка подписана и отдельный человек отвечает за порядок."),
(77.9,81.1,"Вы готовы за это заплатить ещё 15%? Я — да."),
(81.9,87.1,"Когда мировоззрение не совпадает, рождается хаос. Я выбираю порядок."),
(87.3,92.3,"Там, где порядок, там деньги, уважение к материи, к идее, к причине."),
(93.3,98.2,"Это как картина за миллион долларов: никто не объясняет, сколько стоили краски."),
(98.8,105.5,"Есть ценность искусства и времени. Есть ценность моего личного времени и присутствия — времени моей жизни."),
(106.0,107.9,"Есть то, что я люблю создавать:"),
(108.3,112.3,"бутик-отель на обрыве скалы, семейное шато, вилла, пентхаус."),
(112.9,115.5,"Каждый выбирает себе креатора по взглядам."),
(116.1,122.1,"А я стремлюсь не просто зарабатывать, а видеть философию и чудо в том, что я создаю."),
]
def ts(t): return f"0:{int(t//60):02d}:{t%60:05.2f}"
ass=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,ANRE Underground,54,&H00F2F2F2,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,0,0,1,0,2,2,100,100,330,1
Style: Brand,ANRE Underground,32,&H00D8D8D8,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,5,0,1,0,1,8,60,60,130,1
Style: Title,ANRE Underground,88,&H00F2F2F2,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,2,5,80,80,0,1
Style: Kick,ANRE Underground,36,&H00E0E0E0,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,5,0,1,0,1,5,80,80,0,1
Style: Q,ANRE Underground,62,&H00F2F2F2,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,110,110,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ass+=f"Dialogue: 0,{ts(0)},{ts(END)},Brand,,0,0,0,,ANRE  —  NOTES\n"
ass+=f"Dialogue: 0,{ts(0.3)},{ts(3.6)},Kick,,0,0,0,,{{\\fad(500,500)\\pos(540,820)}}ANRE NOTES\n"
ass+=f"Dialogue: 0,{ts(0.3)},{ts(3.6)},Title,,0,0,0,,{{\\fad(500,500)\\pos(540,940)}}Цена —\\Nэто мировоззрение\n"
for a,b,tx in subs:
    A=mp(a); 
    if A<3.6: A=max(A,3.6) if a>3.2 else A
    ass+=f"Dialogue: 0,{ts(max(mp(a),3.7) if mp(a)<3.7 else mp(a))},{ts(mp(b))},Sub,,0,0,0,,{{\\fad(150,150)}}{tx}\n"
ass+=f"Dialogue: 0,{ts(END)},{ts(END+CARD)},Q,,0,0,0,,{{\\fad(400,0)}}За что вы\\Nготовы платить\\Nбольше?\n"
open('/home/claude/cena/build/subs.ass','w').write(ass)
fc=''
for i,(a,b) in enumerate(clips):
    d=b-a; fc+=f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={d-0.06:.3f}:d=0.06[a{i}];"
fc+=''.join(f'[a{i}]' for i in range(len(clips)))+f"concat=n={len(clips)}:v=0:a=1,atempo={S},loudnorm=I=-15:TP=-1.5,apad=pad_dur={CARD+0.5}[au];"
fc+=f"[1:v]tpad=stop_mode=add:stop_duration={CARD}:color=black,drawbox=enable='lt(t,3.9)':x=0:y=0:w=iw:h=ih:color=black@0.45:t=fill,ass=/home/claude/cena/build/subs.ass[v]"
subprocess.run(['ffmpeg','-y','-v','error','-i','/home/claude/vitr/vo_g.m4a','-i','/home/claude/cena/build/vid.mp4','-filter_complex',fc,'-map','[v]','-map','[au]',
 '-t',f'{END+CARD:.2f}','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart','/home/claude/cena/build/reel.mp4'],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i','/home/claude/cena/build/reel.mp4','-vf','scale=720:-2','-c:v','libx264','-preset','veryfast','-crf','24','-c:a','copy','/home/claude/cena/build/tg.mp4'],check=True)
print('END',END+CARD)
