"""Caption-only revision: restore large blessing captions and add a sacred top title."""
import argparse, json, shutil
from pathlib import Path

p = argparse.ArgumentParser(); p.add_argument('--source', type=Path, required=True); p.add_argument('--job', type=Path, required=True); a = p.parse_args()
source = a.source.resolve(); job = a.job.resolve(); job.mkdir(parents=True, exist_ok=False)
for name in ['alignment.json', 'captions.srt', 'music-source.json', 'tts-manifest.json', 'voice-reference.json', 'revision.json', 'narration.wav', 'mix.wav']:
    shutil.copy2(source / name, job / name)
shutil.copytree(source / 'audio', job / 'audio')
alignment = json.loads((source / 'alignment.json').read_text())
def ass_time(seconds):
    cs = round(seconds * 100); return f'{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}'
header = '''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Blessing,Noto Sans CJK SC,192,&H00FFFFFF,&H00FFFFFF,&H00111111,&H00000000,-1,-1,0,0,100,100,2,0,1,14,1,2,70,70,326,1
Style: BlessingTop,Noto Serif CJK SC,64,&H0089D8F6,&H0089D8F6,&H00143B5A,&H00000000,-1,0,0,0,100,100,4,0,1,4,2,8,70,70,150,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 1,0:00:00.00,0:00:14.37,BlessingTop,,0,0,0,,{\\fad(550,550)\\blur0.6}心诚即灵，为您祈福
'''
lines = []
for cue in alignment['cues']:
    color = r'{\c&H008FA3FF&}' if cue['text'] in ('一顺百顺', '阖家幸福', '平安顺遂') else ''
    lines.append(f"Dialogue: 0,{ass_time(cue['start'])},{ass_time(cue['end'])},Blessing,,0,0,0,,{color}{cue['text']}")
(job / 'captions.ass').write_text(header + '\n'.join(lines) + '\n')
(job / 'revision.json').write_text(json.dumps({'revision': 9, 'source_audio_run': str(source), 'audio_reused': True, 'caption_font_size': 192, 'third_sentence_color': '#FF8FA3', 'top_title': '心诚即灵，为您祈福', 'top_title_font': 'Noto Serif CJK SC', 'top_title_color': '#F6D889'}, ensure_ascii=False, indent=2))
print('CAPTIONS_READY', job)
