#!/usr/bin/env python3
"""Read-only core tool/resource discovery; does not claim inference readiness."""
import json, os, subprocess, urllib.request
from pathlib import Path
root=Path(__file__).resolve().parents[1]
c=json.loads((root/'configs/resources.json').read_text())
checks={}
for name in ['python','node','ffmpeg','ffprobe']:
    path=c['tools'][name]
    checks[name]={'path':path,'executable':os.access(path,os.X_OK)}
for name in ['python','runtime','models','reference','external_site_packages']:
    path=c['narration'][name]
    checks['tts_'+name]={'path':path,'readable':os.access(path,os.R_OK)}
checks['remotion']={'installed':(root/'renderers/remotion/node_modules/.bin/remotion').exists()}
try:
    d=json.load(urllib.request.urlopen(c['optional_services']['h3_220']['url']+'/system_stats',timeout=3))
    checks['h3_220']={'reachable':True,'version':d.get('system',{}).get('comfyui_version'),'inference_tested':False}
except Exception as e: checks['h3_220']={'reachable':False,'error':str(e),'inference_tested':False}
print(json.dumps(checks,indent=2,ensure_ascii=False))
core_ok=all(next((v[k] for k in ['executable','readable','installed'] if k in v),True) for v in checks.values())
raise SystemExit(0 if core_ok else 1)
