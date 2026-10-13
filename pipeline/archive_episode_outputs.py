"""One-time idempotent archive of known episode outputs; old paths stay symlinks."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parents[1];records=[]
for kind in ('runs','deliveries'):
 for src in sorted((root/kind).iterdir()):
  if src.is_symlink() or not src.is_dir():continue
  n=src.name
  episode=('early_pregnancy_signs_storybook_02' if n.startswith(('storybook-','h3-storybook-')) else 'early_pregnancy_signs_01' if n.startswith(('early-pregnancy-','h3-pregnancy-','h3-compose-')) else None)
  if not episode:continue
  dst=root/'projects'/episode/kind/n
  if dst.exists():raise RuntimeError(f'Destination exists: {dst}')
  records.append({'old':str(src.relative_to(root)),'new':str(dst.relative_to(root))})
  if a.apply:
   dst.parent.mkdir(parents=True,exist_ok=True);src.rename(dst);src.symlink_to(Path('..')/dst.relative_to(root),target_is_directory=True)
print(json.dumps(records,ensure_ascii=False,indent=2))
