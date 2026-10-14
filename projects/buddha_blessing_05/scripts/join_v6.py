"""Join independently generated, inspected short clips on220, without retiming."""
import argparse,hashlib,json,subprocess,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--a',type=Path,required=True);p.add_argument('--b',type=Path,required=True);args=p.parse_args()
E=Path(__file__).resolve().parents[1];job=E/'runs'/('joined-v6-'+time.strftime('%Y%m%d-%H%M%S'));job.mkdir()
clips=[args.a.resolve(),args.b.resolve()]
for c in clips: assert c.is_file()
(job/'concat.txt').write_text(''.join("file '"+str(c)+"'\n" for c in clips))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(job/'concat.txt'),'-an','-frames:v','447','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',str(job/'clip.mp4')],check=True)
(job/'lineage.json').write_text(json.dumps(dict(method='two independently generated226-frame clips; hard cut at9.4167s between same-reference anchors; retain first447/452 frames, no loop, freeze, speed or frame interpolation',sources=[dict(path=str(c),sha256=hashlib.sha256(c.read_bytes()).hexdigest()) for c in clips],output_sha256=hashlib.sha256((job/'clip.mp4').read_bytes()).hexdigest()),indent=2))
subprocess.run(['ffmpeg','-y','-v','error','-ss','8.9','-i',str(job/'clip.mp4'),'-t','1.1','-vf','fps=10,scale=216:384,tile=6x2','-frames:v','1',str(job/'seam.jpg')],check=True)
print(job,flush=True)
