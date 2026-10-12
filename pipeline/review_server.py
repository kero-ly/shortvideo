from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from pathlib import Path
class H(SimpleHTTPRequestHandler):
 def send_head(self):
  self.bound=None
  path=Path(self.translate_path(self.path))
  if path.is_file() and 'Range' in self.headers:
   n=path.stat().st_size
   r=self.headers['Range'].removeprefix('bytes=').split(',')[0].split('-');start=int(r[0] or 0);end=min(int(r[1]) if r[1] else n-1,n-1)
   self.send_response(206);self.send_header('Content-Type',self.guess_type(str(path)));self.send_header('Accept-Ranges','bytes');self.send_header('Content-Range',f'bytes {start}-{end}/{n}');self.send_header('Content-Length',str(end-start+1));self.end_headers();f=path.open('rb');f.seek(start);self.bound=end-start+1;return f
  return super().send_head()
 def copyfile(self,s,o):
  if self.bound is None:return super().copyfile(s,o)
  left=self.bound
  while left:
   b=s.read(min(65536,left))
   if not b:break
   o.write(b);left-=len(b)
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--port',type=int,default=8770);a.add_argument('--directory',default=str(Path(__file__).resolve().parents[1]));args=a.parse_args()
 ThreadingHTTPServer(('127.0.0.1',args.port),partial(H,directory=args.directory)).serve_forever()
