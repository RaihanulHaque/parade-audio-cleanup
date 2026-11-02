"""Remix Demucs stems: suppress boot transients leaking into vocals/music, reduce drums, gate vocal gaps."""
import sys, json, subprocess, os
import numpy as np, soundfile as sf
from scipy.signal import stft, istft, butter, sosfiltfilt
from scipy.ndimage import median_filter

stem_dir, out_dir = sys.argv[1:3]
N, HOP = 4096, 1024

def load(n):
    x, sr = sf.read(os.path.join(stem_dir, n + '.wav'), always_2d=True)
    return x.astype(np.float32), sr

def floor_curve(freqs, pts):
    return np.interp(np.log10(np.maximum(freqs, 1)), np.log10([p[0] for p in pts]), [p[1] for p in pts])

def desuppress(x, sr, pts):
    """Soft harmonic/percussive mask; pts = (Hz, min gain) keeps consonants and treble intact."""
    out = np.zeros_like(x)
    for c in range(x.shape[1]):
        f, _, Z = stft(x[:, c], sr, nperseg=N, noverlap=N - HOP)
        M = np.abs(Z)
        H = median_filter(M, size=(1, 17), mode='nearest')
        P = median_filter(M, size=(31, 1), mode='nearest')
        mask = H**2 / (H**2 + P**2 + 1e-12)
        fl = floor_curve(f, pts)[:, None]
        g = fl + (1 - fl) * mask
        _, y = istft(Z * g, sr, nperseg=N, noverlap=N - HOP)
        out[:, c] = y[:len(x)] if len(y) >= len(x) else np.pad(y, (0, len(x) - len(y)))
    return out

def gate(x, sr, floor_db, thr_db=-32):
    """Attenuate vocal stem between sung phrases using 300-3000 Hz envelope (residue there is not singing)."""
    sos = butter(4, [300, 3000], 'bandpass', fs=sr, output='sos')
    band = sosfiltfilt(sos, x.mean(1))
    win = int(.05 * sr)
    env = np.sqrt(np.convolve(band**2, np.ones(win) / win, 'same'))
    ref = np.percentile(env, 95)
    open_ = env > ref * 10**(thr_db / 20)
    # hold 350 ms so phrase tails and short gaps between words survive
    hold = int(.35 * sr)
    open_ = np.convolve(open_.astype(np.float32), np.ones(hold), 'same') > 0
    g = np.where(open_, 1.0, 10**(floor_db / 20)).astype(np.float32)
    k = int(.04 * sr)
    g = np.convolve(g, np.hanning(k) / np.hanning(k).sum(), 'same')
    return x * g[:, None], float(open_.mean())

v, sr = load('vocals'); d, _ = load('drums'); b, _ = load('bass'); o, _ = load('other')

V_PTS = [(20, .10), (250, .15), (800, .55), (2500, .85), (6000, 1.0), (22050, 1.0)]
O_PTS = [(20, .10), (400, .12), (1500, .40), (6000, .70), (22050, .70)]
O_PTS_MILD = [(20, .35), (400, .40), (1500, .65), (6000, .90), (22050, .90)]
vc = desuppress(v, sr, V_PTS)
oc = desuppress(o, sr, O_PTS)
om = desuppress(o, sr, O_PTS_MILD)
bc = desuppress(b, sr, O_PTS)

vg_soft, _ = gate(vc, sr, -8)
vg_hard, open_frac = gate(vc, sr, -24)
print('vocal gate open fraction', round(open_frac, 3))

db = lambda x: 10**(x / 20)
mixes = {
    'gentle': vg_soft + om + b + d * db(-9),
    'strong': vg_hard + oc * db(-1) + bc + d * db(-30),
    'vocals_only': vg_hard,
}
for name, m in mixes.items():
    p = max(np.abs(m).max(), 1e-6)
    sf.write(os.path.join(out_dir, f'{name}_raw.wav'), m / p * .89, sr, subtype='FLOAT')
