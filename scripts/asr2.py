import sys, json, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
out_dir = sys.argv[1]
ref, sr = sf.read(out_dir + '/asr_clear.wav', dtype='float32')
w = int(.05*sr); env = 20*np.log10(np.sqrt(np.convolve(ref**2, np.ones(w)/w, 'same'))+1e-9)
act = env > np.percentile(env, 92) - 25
# phrases: merge gaps under 0.6 s, drop blips under 0.8 s, cap length at 24 s
idx = np.flatnonzero(np.diff(np.r_[0, act.astype(int), 0])); regs = list(zip(idx[::2], idx[1::2]))
merged = []
for a, b in regs:
    if merged and (a - merged[-1][1]) / sr < .6: merged[-1][1] = b
    else: merged.append([a, b])
chunks = []
for a, b in merged:
    if (b - a) / sr < .8: continue
    while (b - a) / sr > 24: chunks.append((a, a + 24*sr)); a += 24*sr
    chunks.append((a, b))
print('chunks', [(round(a/sr,1), round(b/sr,1)) for a, b in chunks], flush=True)
m = WhisperModel('large-v3', device='cpu', compute_type='int8', cpu_threads=10)
tok = m.hf_tokenizer
ban = sorted({i for t in ['موسیقی', ' موسیقی', 'موزیک', ' موزیک', 'Music', ' Music', 'Thank', ' you'] for i in tok.encode(t, add_special_tokens=False).ids})
res = {}
for name in sys.argv[2:]:
    x = sf.read(f'{out_dir}/asr_{name}.wav', dtype='float32')[0]
    rows = []
    for a, b in chunks:
        c = x[max(a - int(.2*sr), 0):b + int(.2*sr)]; c = c / max(np.abs(c).max(), 1e-6) * .9
        segs, _ = m.transcribe(c, language='fa', beam_size=5, vad_filter=False, condition_on_previous_text=False, no_speech_threshold=None, log_prob_threshold=None, compression_ratio_threshold=None, temperature=[0.0], suppress_tokens=[-1] + ban, without_timestamps=True)
        segs = list(segs)
        rows.append(dict(s=round(a/sr,1), e=round(b/sr,1), t=' '.join(s.text.strip() for s in segs), lp=round(float(np.mean([s.avg_logprob for s in segs])) if segs else -9, 2)))
        print(name, rows[-1], flush=True)
    res[name] = rows
    json.dump(res, open(out_dir + '/asr2.json', 'w'), ensure_ascii=False, indent=0)
