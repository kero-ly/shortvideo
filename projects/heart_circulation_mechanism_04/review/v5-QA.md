# v5 layout review

User authorized removing the orange frame, full-screen animation, repositioning subtitles and a large upper title. This is an episode-only change.

- Rendered on 220: 1080×1920, 30 fps, 682 frames, 22.733 seconds.
- Inspected all five representative stills and the 15-frame contact sheet. No orange outer card; upper title and bottom outlined captions are readable. Close-ups intentionally crop peripheral anatomy; the body-circulation shot crops lungs below the title. Bottom gradient de-emphasizes peripheral labels behind captions.
- All frames decode; no black segments >= 0.15 s. Integrated loudness -16.89 LUFS, true peak -4.46 dBTP; narration tail 0.919 s.
- v4/v5 AAC packet SHA256 is identical: 1de16a6bb1b0cef66586904b16fd84fb453e4ade78ba37127febad0240471c27. No TTS changes.
- Browser playback observed running from 0.19 s through ended=true at 22.733333 s, no media error. Five review images loaded.
- Local delivery: all 18 manifest entries verified against SHA256 after transfer. Media generated and packaged on 220.
- Packaging assertion typo yuv520p corrected to yuv420p before successful QA; no media regeneration required.
- Supplementary playback evidence is v5-playback-check.json; the immutable delivery qa.json records the earlier pending playback stage. Actual listening remains pending. Internal preview, not publication approval.
