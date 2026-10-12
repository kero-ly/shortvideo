#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export UV_CACHE_DIR="$PWD/.cache/uv"
uv sync --python /usr/bin/python3
if [[ ! -x .runtime/tts/bin/python ]]; then
  uv venv --python /usr/bin/python3 .runtime/tts
fi
# Borrow the known existing inference dependencies without modifying them.
# This external dependency is intentionally recorded, not claimed to be uv-locked.
uv run --no-sync python - <<'PYTHON'
import json, pathlib, subprocess
root=pathlib.Path.cwd()
c=json.loads((root/'configs/resources.json').read_text())
external=pathlib.Path(c['narration']['external_site_packages'])
if not external.is_dir(): raise SystemExit('Missing shared TTS dependencies: '+str(external))
python=c['narration']['python']
purelib=subprocess.check_output([python,'-c','import sysconfig; print(sysconfig.get_paths()["purelib"])'],text=True).strip()
paths=[str(external),*c['narration'].get('additional_site_packages',[])]
for path in paths:
    if not pathlib.Path(path).is_dir(): raise SystemExit('Missing external dependency: '+path)
pathlib.Path(purelib,'shared-indextts2.pth').write_text('\n'.join(paths)+'\n')
PYTHON
.runtime/tts/bin/python - <<'PYTHON'
import importlib.metadata, json
from pathlib import Path
items=sorted([{'name':d.metadata['Name'],'version':d.version} for d in importlib.metadata.distributions()],key=lambda x:x['name'].lower())
Path('configs/tts-observed-packages.json').write_text(json.dumps(items,indent=2))
PYTHON
