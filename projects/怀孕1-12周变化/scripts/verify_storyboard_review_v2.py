from pathlib import Path
from urllib.parse import unquote,urlsplit
from html.parser import HTMLParser
import json,hashlib,subprocess
import jsonschema
from PIL import Image
P=Path(__file__).resolve().parents[1];root=P.parents[1]
s=json.loads((P/'storyboard/draft-v2.json').read_text());p=json.loads((P/'production-plan.json').read_text())
jsonschema.validate(p,json.loads((root/'schemas/production-plan.schema.json').read_text()))
assert len(s['shots'])==16
for x in s['shots']:
 f=P/x['reference_frame'];im=Image.open(f);im.verify()
 assert hashlib.sha256(f.read_bytes()).hexdigest()==x['reference_frame_sha256']
 assert subprocess.run(['git','check-ignore','-q',str(f)],cwd=root).returncode==0
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,t,a):
  for k,v in a:
   if k in ('src','href'):self.links.append(v)
v=Links();v.feed((P/'review/storyboard-v2.html').read_text());checked=0
for u in v.links:
 parsed=urlsplit(u)
 if parsed.scheme or not parsed.path:continue
 f=(P/'review'/unquote(parsed.path)).resolve();assert f.exists(),str(f);checked+=1
result={'schema':'passed','image_count':16,'sha256_checks':'passed','media_ignored':'passed','local_link_count':checked,'broken_links':0,'scope':'static storyboard package verification; no video generated'}
(P/'review/package-verification-v2.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result))
