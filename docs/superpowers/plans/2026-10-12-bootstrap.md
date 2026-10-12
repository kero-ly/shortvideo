# Shortvideo factory bootstrap plan

Goal: initialize an isolated factory in /home/ly/shortvideo and prove one real narrated video end-to-end.
Authorization: user approved directory/resource initialization and end-to-end verification on 220.
Architecture: user-owned source, dependencies, caches and outputs; read-only reuse of shared models.
Stack: Python orchestration, pinned Remotion/React, FFmpeg, existing IndexTTS2.
Scope: baseline tooling and smoke production; style skills await user reference material.
Tasks:
- [x] Create documented directory layout and explicit resource configuration.
- [x] Install isolated Remotion dependencies/browser; inspect existing voice runtime.
- [x] Generate new Chinese narration on one currently available GPU without altering shared services.
- [x] Render a short animated portrait test, mux voice, decode and verify streams/audio/frames.
- [x] Save report, reusable commands and local review artifact; record optional capabilities honestly.
Checks: missing tools/models must fail explicitly; no shared writes; no embedded credentials; output paths contained in factory; no silent fake speech fallback.

User requested uv; borrowed TTS dependencies explicitly documented; GPU lock regression passed.
