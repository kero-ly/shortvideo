# v6 audio and delivery review

User requested a livelier science-explainer narration and background music. v6 preserves the five checked statements and v5 full-screen visual layout, replaces the narration, adds original procedural music, and re-times the animation to the new voice clips.

- 220 render: 1080×1920, 30 fps, 842 frames, 28.0667 seconds. Complete decode passed; no black segment >= 0.15 seconds. Integrated loudness -16.22 LUFS, true peak -7.60 dBTP; voice tail 0.906 seconds.
- Narration: IndexTTS2 generated five clips with per-shot happy/surprised/calm emotion guidance, without tempo compression. Faster-whisper word alignment and normalized transcription match the locked script in all five shots. ASR does not establish pronunciation or expressive quality by itself.
- Music: original 104 BPM C-major pluck, bass and light percussion generated from `scripts/music-v6.py`; no external recordings. Sidechain compression lowers music under speech. Separate narration and music WAVs are included for comparison.
- Visual review: inspected the five representative frames, 15 boundary frames and contact sheet. Title, captions and full-screen composition remain in the intended zones without apparent occlusion. Anatomy is simplified and must not be read as a four-chamber diagram.
- Browser playback: the local v6 page loaded all five images; the complete MP4 played from 0.177313 through ended=true at 28.066667 seconds with no media error. See `v6-playback-check.json`. This verifies playback, not the audible result.
- Delivery: the 23 files in `v6-manifest.json` were transferred to local and checked against SHA256; 220 retains the matching delivery. The immutable packaged `qa.json` records browser playback as pending because it was created earlier; this file records the later check.
- Actual listening and user preference remain pending. Source voice reference rights have not been independently established. This is an internal review preview, not publication approval.
