from pathlib import Path
import json, hashlib

P = Path(__file__).resolve().parents[1]
ROOT = P.parent / "怀孕1-12周变化"
board_path = P / "storyboard/draft-v1.json"
board = json.loads(board_path.read_text())
source_numbers = [2, 2, 3, 10, 10, 2, 2, 3, 7, 7, 10, 1]
common = (
    "Edit the supplied warm hand-drawn portrait reference into one complete 9:16 starting frame. "
    "Preserve the same adult Chinese couple identity, clothing, gentle brown outlines, low-saturation cream palette, "
    "natural adult proportions and soft paper-like shading. Keep the room complete with furniture and props. "
    "No text, letters, numbers, watermark, logo, diagnosis, ultrasound result or speech bubble; all accurate text is added later. "
    "Keep the upper 18 percent calm for title and the bottom 20 percent calm for captions; no crucial face or prop at the right edge. "
    "Exactly one woman and one man, natural hands, no exaggerated pregnancy belly. Requested portrait canvas 1024x1792.\n\n"
)
for shot, ref in zip(board["shots"], source_numbers):
    shot["reference_source"] = f"怀孕1到12周（无文字版）参考图/landscape-scene-{ref:02d}.png"
    src = ROOT / shot["reference_source"]
    shot["reference_input_sha256"] = hashlib.sha256(src.read_bytes()).hexdigest()
    prompt = common + f"Scene brief: {shot['visual']}. Starting pose: {shot['action']}. Keep this as a quiet maternal information scene, not a medical advertisement."
    motion = (
        "Animate the same warm hand-drawn couple and room with one restrained action: "
        + shot["action"]
        + ". Stable faces, hair, clothing, hands and furniture; gentle light; very slow push or fixed camera; one continuous shot."
    )
    (P / "prompts/shots" / f"{shot['id']}-image-v1.txt").write_text(prompt + "\n")
    (P / "prompts/shots" / f"{shot['id']}-motion-v1.txt").write_text(motion + "\n")
    shot["reference_frame_status"] = "pending_generation"
    shot["prompt"] = f"prompts/shots/{shot['id']}-image-v1.txt"
    shot["motion_prompt"] = f"prompts/shots/{shot['id']}-motion-v1.txt"
board["reference_frame_status"] = "pending_generation"
board["identity_basis"] = "reuse approved previous episode warm couple language; direct scene edits from supplied reference images"
board_path.write_text(json.dumps(board, ensure_ascii=False, indent=2) + "\n")
print(f"prepared {len(board['shots'])} prompts")
