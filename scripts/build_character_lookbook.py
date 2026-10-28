"""Read-only lookbook; source images remain in episode directories."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
groups={'在天上选妈妈_参考复刻':'选妈妈 · 卡通母婴','孕期少说这十句话':'生活剧场 · 夫妻人物','怀孕1-12周变化':'孕周变化 · 妈妈','pregnancy_nausea_presenter_03':'孕吐 · 女性讲解员','early_pregnancy_signs_storybook_02':'早孕 · 奶油绘本','early_pregnancy_signs_01':'早孕 · 暖色手绘','wound_healing_cells_08':'伤口愈合 · 拟人细胞','fever_thermostat_09':'发烧 · 拟人角色'}
old=R/'review/character-lookbook-v1.json'
known={x['path']:x['id'] for x in json.loads(old.read_text())['items']} if old.exists() else {}
next_id=max([int(v[1:]) for v in known.values()]+[0])+1
items=[]
for ep,label in groups.items():
 base=R/'projects'/ep
 for folder in [base/'references/character',base/'references/characters',base/'h3_v2/references/character']:
  if not folder.exists():continue
  for p in sorted(folder.iterdir()):
   if p.suffix.lower() not in {'.png','.jpg','.webp'}:continue
   status='历史候选 · 确认记录未核对';evidence=None
   if ep=='在天上选妈妈_参考复刻' and p.stem in {'character-master-v3','character-sheet-v3'}:status='用户已确认 · 妈妈v3';evidence=f'projects/{ep}/review/character-approval-v3.json'
   if ep=='pregnancy_nausea_presenter_03' and p.stem=='candidate-A-v2-younger':status='用户已确认 · 女性v2';evidence=f'projects/{ep}/review/character-approval-v2.json'
   if ep=='孕期少说这十句话' and p.stem=='history-couple-prenatal-v2':status='用户指定沿用 · 历史夫妻';evidence='本线程用户指定沿用产检等视频的男女人物母版'
   rel=str(p.relative_to(R))
   if rel not in known:
    known[rel]=f'C{next_id:03}';next_id+=1
   items.append(dict(id=known[rel],episode=ep,group=label,category='科普角色' if ep in {'wound_healing_cells_08','fever_thermostat_09'} else '母婴',name=p.stem,role='设计页' if any(s in p.stem for s in ['sheet','design']) else ('宝宝造型' if 'baby' in p.stem else '母版 / 候选'),status=status,evidence=evidence,path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
manifest={'version':1,'scope':'本地已发现的角色文件；不是全历史完整性声明。图片留原项目。','items':items}
(R/'review/character-lookbook-v1.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
template=(R/'scripts/character-lookbook-template.html').read_text()
(R/'review/character-lookbook-v1.html').write_text(template.replace('__DATA__',json.dumps(items,ensure_ascii=False).replace('<','\\u003c')))
print(f'{len(items)} images / {len(set(i["episode"] for i in items))} projects')
