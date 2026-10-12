# Factory operating rules
Use 220 as primary host and /home/ly/shortvideo as the project root.
Local authoring root is /Users/ly/Desktop/project/shortvideo with the same Git layout. Original upstream repository is preserved at /Users/ly/Desktop/project/shortvideo-reference-original; treat it as a reference, never the production root. Put episode work in projects/<episode-id> and document selective reuse in library/ATTRIBUTIONS.md. Track source, prompts, manifests and QA summaries in Git; transfer media separately and record SHA256. Read docs/workspace-layout.md for sync rules.
Never store passwords/API keys in tracked files. Do not modify shared /home/video runtimes.
Read configs/resources.json and docs/workflow.md before production. Explicit user tool choices override defaults.
Do not claim capability is ready based solely on a path or HTTP response: distinguish configured, reachable, smoke-tested and production-approved.
All jobs write unique runs/<job-id>/ directories. Check GPU availability before model work. Never kill shared jobs.
A smoke test is not a validated style. Final content production requires script/storyboard, audio timing, preview review, render, QA and delivery manifest.

Python uses uv: orchestration via uv sync / uv run; TTS environment via uv venv. TTS borrows explicitly configured external dependency directories read-only. configs/tts-observed-packages.json is an observed snapshot, NOT a portable lockfile. A separate fully isolated TTS lock remains future work.
