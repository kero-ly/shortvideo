# v7 mix review

User requested slightly quieter narration and louder background music. The v7 mix lowers the pre-normalization voice gain from 1.4 to 1.25 and raises music from 0.48 to 0.60, retaining the v6 sidechain ducking, original source WAVs, 104 BPM composition, script, subtitles and picture. Overall loudness normalization still targets -16 LUFS; these numbers describe the relative balance, not a guaranteed perceived loudness change on every speaker.

- Produced on 220 in unique `runs/20261013-heart-v7` and `deliveries/20261013-heart-v7`; no TTS, animation or caption regeneration.
- The copied video packet stream hashes match v6 exactly. Output is 1080×1920, 30 fps, 842 frames, 28.0667 seconds. Full decode passed, with no black segment >= 0.15 seconds.
- Integrated loudness is -16.22 LUFS; true peak is -8.30 dBTP. Original narration ends with 0.906 seconds to spare. AAC is 48 kHz stereo.
- v6 narration WAV, original music WAV, alignment and subtitles are byte-for-byte copied. The five shot images are the v6 review frames; no new visual content was introduced.
- Both 220 and local v7 deliveries have 23 files verified against `v7-manifest.json`.
- Browser playback and actual listening are tracked separately in `v7-playback-check.json`. User evaluation of voice/music balance remains pending. Internal preview only; voice reference rights have not been independently established.
