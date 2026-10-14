"""Generate bounded direct-reference edits for the prenatal-checkup storyboard."""
from pathlib import Path
import argparse, datetime, hashlib, json, subprocess, sys
import struct

P = Path(__file__).resolve().parents[1]
ROOT = P.parent / "怀孕1-12周变化"
parser = argparse.ArgumentParser()
parser.add_argument("--shots", nargs="+", required=True)
parser.add_argument("--workers", type=int, default=1)
args = parser.parse_args()
assert 1 <= args.workers <= 2
board = json.loads((P / "storyboard/draft-v1.json").read_text())
shots = [item for item in board["shots"] if item["id"] in args.shots]
assert len(shots) == len(args.shots)
job = "reference-v1-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
run = P / "runs" / job
run.mkdir(parents=True, exist_ok=False)
out_dir = P / "references" / "shots" / "v1"
out_dir.mkdir(parents=True, exist_ok=True)

def generate(shot):
    sid = shot["id"]
    src = ROOT / shot["reference_source"]
    prompt_path = P / "prompts" / "shots" / f"{sid}-image-v1.txt"
    raw = run / f"{sid}-raw.png"
    target = out_dir / f"{sid}.png"
    result = subprocess.run([
        sys.executable,
        "/Users/ly/.codex/skills/openlux-gpt-image/scripts/openlux_image.py",
        "--mode", "edit", "--image", str(src), "--prompt", prompt_path.read_text(),
        "--size", "1024x1792", "--quality", "high", "--output", str(raw), "--timeout", "240",
    ], capture_output=True, text=True)
    (run / f"{sid}-result.log").write_text(result.stdout + "\n" + result.stderr)
    rec = {
        "shot": sid, "job": job, "input": str(src.relative_to(P.parent)),
        "input_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
        "prompt": str(prompt_path.relative_to(P)),
        "status": "failed", "exit_code": result.returncode,
        "automatic_retry": False,
    }
    if result.returncode == 0:
        response = json.loads(result.stdout)
        data = raw.read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError("provider output is not a PNG")
        width, height = struct.unpack(">II", data[16:24])
        target.write_bytes(raw.read_bytes())
        size = [width, height]
        rec.update(status="generated_pending_visual_review", output=str(target.relative_to(P)),
                   sha256=hashlib.sha256(target.read_bytes()).hexdigest(), actual_size=size,
                   response=response)
    else:
        rec["error"] = result.stderr.strip()[-2000:]
    (run / f"{sid}-manifest.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n")
    return rec

records = [generate(shot) for shot in shots]
(run / "batch-manifest.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"job": job, "records": records}, ensure_ascii=False))
