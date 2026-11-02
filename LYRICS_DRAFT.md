# Lyrics draft: machine transcription, not verified

Whisper large-v3 was run on three versions of the audio. No published lyrics were found to check against.
Whisper did not understand this singing well, so have a Persian speaker correct this before relying on it.

Times are from the `cleaned/` versions. Ringtone time is about 1:26 earlier.

## Not recovered

0:00-1:24 and 2:14-end: no usable words. Whisper returned only "PYM JBZ", which is not lyrics.

## Section 1: 1:26-1:49 (ringtone 0:00-0:22)

Raw output:

- Clear vocals: هر قربه چه ما منفرد دولت امریا برک برک امریا ما باده قدری ما برانگره این ما برک برک اسرابین ترراه فرد فلسطین در جنگ دشمنه بینین چون بر رهونه این در باده رفته این
- Vocal track: هر قربه چه ما منفرد دولت آمرین ها منفرد آمرین ها ما قادر قدری و برانگره هین ها منفرد اسرائيل تر راه فرد فلسطین در جنگ دشمنه بینین چون برد و نهین در باد و تهین
- Full mix: هر قررش ما منفرد دولت امریا برک برک امریا آباده خودتین و برانگره این ما برک برک اسرابین در راه فرد فلسطین در جنگ دشمنه بینین چون بد رومونه این سرواد رومونه این

Possible words, all to be checked:

| Heard | Possible meaning | Confidence |
|---|---|---|
| فلسطین | Palestine | Fairly high: in all three |
| در جنگ دشمن | in the war/battle with the enemy | Medium |
| اسرائیل (اسرابین) | Israel | Medium: spelled correctly in one, similar in two |
| دولت آمریکا (دولت امریا) | the American government | Medium |
| مرگ مرگ (برک برک) | "death, death", possibly "death to America/Israel" | Low: a guess from similar sounds |

## Section 2: 1:54-2:13 (ringtone 0:28-0:47)

Raw output:

- Clear vocals: رسمنده این ادنس یاران شریدین فرامان خونه این ادنس را با عرصه شنینین بس این بار این شان نخدین با صبح دولت نخدین با نخد زهورین با شور و شورین
- Vocal track: رسمنده این ادنه اصد یاران شریدین فرماه خومین این را ما اصد شنینین بسین با این شان عهدین با صبح دولت ماهدین ما نصد زبونین با شور و شورین
- Full mix: رسمنده یاد نست یاران شریدین فرماه خوبه این این را ما هست و شنینین بستین با این شان عهدین با صبح دولت و عهدین ما نست به ظهورین و شور و شورین

Possible words, all to be checked:

| Heard | Possible meaning | Confidence |
|---|---|---|
| رزمنده‌ایم (رسمنده این) | we are fighters | Medium |
| یاران شهیدیم (یاران شریدین) | we are companions of the martyrs | Medium |
| با صبح دولت | with the dawn of the (blessed) state | Medium: in all three |
| با شور و شعوریم (با شور و شورین) | we have passion and awareness | Medium |
| ظهور (زهورین / ظهورین) | the Advent / appearance | Low |
| فرمان خمینی (فرماه خومین) | Khomeini's command | Low: a guess from one version |
