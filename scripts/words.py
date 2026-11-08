import sys
sys.path.insert(0,'/home/claude/asr')
import subprocess, numpy as np
from faster_whisper import WhisperModel
p=sys.argv[1]
raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True).stdout
a=np.frombuffer(raw,np.int16).astype(np.float32)/32768
m=WhisperModel('/home/claude/whisper-small',device='cpu',compute_type='int8')
segs,_=m.transcribe(a,language='ru',vad_filter=True,beam_size=5,word_timestamps=True)
for s in segs:
    print(' '.join(f'{w.word.strip()}[{w.start:.2f}-{w.end:.2f}]' for w in s.words))
