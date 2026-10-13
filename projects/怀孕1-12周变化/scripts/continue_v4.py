import os,time,subprocess
from pathlib import Path
R=Path('/home/ly/shortvideo');P=R/'projects/怀孕1-12周变化'
# Respect the existing shared factory job; wait for the whole admitted batch.
while Path('/proc/2733776').exists():
 print('WAITING_FOR_SHARED_GPU_BATCH',flush=True);time.sleep(30)
for cmd in [ ['uv','run','python',str(P/'scripts/produce_audio_v4.py')],['uv','run','--with','faster-whisper','python',str(P/'scripts/align_v4.py')],['uv','run','--with','numpy','python',str(P/'scripts/revise_v4.py')]]:
 env=os.environ.copy();env['UV_DEFAULT_INDEX']='https://mirrors.aliyun.com/pypi/simple';subprocess.run(cmd,cwd=R,env=env,check=True)
