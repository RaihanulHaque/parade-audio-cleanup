# Parade Audio Cleanup

Cleaned, single-voice and ringtone versions of a 2:40 military parade recording, with the boots and drums reduced and the singing brought forward.

The source file's embedded title is "رژه حماسی گروهان نمونه دانشگاه امیرالمؤمنین(ع) اصفهان" (Epic parade of the model company of Amir al-Momenin University, Isfahan).

## Rights and content

- **This is not an original recording.** The source audio belongs to its original creators. This repo claims no rights to it and has no license for the audio. If you own the recording and want it removed, please open an issue.
- **The lyrics are unverified.** They may include political chants. See [LYRICS_DRAFT.md](LYRICS_DRAFT.md), a low-accuracy machine transcription of part of the song.
- **The results have not been judged by ear during processing.** They were checked with measurements and spectrograms.

## Files

| Folder | Version | What it is |
|---|---|---|
| `ringtone/` | `parade_ringtone`, `parade_alarm` | 48-second main theme for phones, in MP3 and M4A. The alarm is louder and more compressed. |
| `solo/` | `parade_solo_natural_*` | Singing only, filtered to reduce the group sound. Sounds more natural, but still somewhat like a group. |
| `solo/` | `parade_solo_rebuilt_*` | Singing only, re-synthesized from one pitch line. Closer to one voice, but may sound synthetic. |
| `cleaned/` | `parade_clear_lyrics` | Clearest words, with a quieter band behind them. |
| `cleaned/` | `parade_clear_lyrics_vocals` | The same clear singing with almost no band. |
| `cleaned/` | `parade_strong` | Drums almost removed and boot sounds reduced. |
| `cleaned/` | `parade_gentle` | Fuller band, with some of the march beat kept. |
| `cleaned/` | `parade_vocals_only` | Singing with no band, and silence between sung phrases. |

Files in `solo/` ending in `_theme` are the 48-second clip, and files ending in `_full` are the 2:30 song. Files in `cleaned/` come in MP3 and FLAC.

No version sounds like one singer recording alone, because the source is a group singing together. Some boot sound remains in the mixes.

## How it was made

1. **Polarity fix:** The source's left channel was inverted and about 6.5 dB quieter than the right, so `fix.py` aligns and averages them to mono.
2. **Separation:** [Demucs](https://github.com/facebookresearch/demucs) `htdemucs_ft` splits the audio into vocals, drums, bass and other.
3. **Boot reduction:** `clean.py` and `clear.py` suppress leaked impacts with a harmonic/percussive mask, reduce the drums, and gate the gaps between phrases.
4. **Single-voice versions:** `solo.py` uses [pyworld](https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder) pitch tracking to build the natural and rebuilt versions.
5. **Mastering:** ffmpeg applies EQ, compression, a fixed gain and a limiter. The full-length versions reach -16 LUFS.
6. **Transcription:** `asr2.py` runs [faster-whisper](https://github.com/SYSTRAN/faster-whisper) `large-v3` on each sung phrase.

The scripts in `scripts/` are the working scripts from this cleanup rather than a packaged tool, and the ffmpeg mastering commands are not included. The original source file is not included either.
