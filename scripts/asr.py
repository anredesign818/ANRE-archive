import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True).stdout
    return np.frombuffer(raw,np.int16).astype(np.float32)/32768
m=WhisperModel('/home/claude/whisper-small',device='cpu',compute_type='int8')
for p in sys.argv[1:]:
    segs,_=m.transcribe(load(p),language='ru',vad_filter=True,beam_size=5)
    print('##',p)
    for s in segs: print(f'{s.start:6.1f}-{s.end:6.1f} {s.text.strip()}')
