"""Reduce unison-group spread: harmonic comb + de-reverb (natural), WORLD single-f0 resynthesis (rebuilt)."""
import sys, numpy as np, soundfile as sf, pyworld as pw
from scipy.signal import stft, istft, medfilt
from scipy.ndimage import uniform_filter1d
inp, out = sys.argv[1:3]
x, sr = sf.read(inp, always_2d=True); x = x.mean(1).astype(np.float64)
peak = np.abs(x).max(); x = x / peak * .9
FP = 5.0
f0, t = pw.harvest(x, sr, f0_floor=110, f0_ceil=600, frame_period=FP)
f0 = pw.stonemask(x, f0, t, sr)
f0 = medfilt(f0, 9)
v = f0 > 0
# zero voiced frames where the vocal is effectively silent, so noise is not pitched
frame = np.sqrt(np.convolve(x**2, np.ones(int(.02*sr))/int(.02*sr), 'same'))[(t*sr).astype(int).clip(0, len(x)-1)]
f0[frame < 10**(-48/20)] = 0; v = f0 > 0
print('voiced %', round(100*v.mean(),1), 'median f0', round(float(np.median(f0[v])),1), 'p5/p95', np.round(np.percentile(f0[v],[5,95]),1), flush=True)

# --- natural
N, H = 4096, 512
f, st, Z = stft(x, sr, nperseg=N, noverlap=N-H)
M = np.abs(Z)
fi = np.interp(st, t, f0, left=0, right=0)
vi = np.interp(st, t, v.astype(float)) > .5
G = np.ones_like(M)
sig = np.maximum(14, .014*f)
top = np.clip((f - 4000) / 2000, 0, 1)
for i in np.flatnonzero(vi):
    r = f / max(fi[i], 1); d = np.abs(r - np.round(r)) * fi[i]
    comb = .14 + .86*np.exp(-.5*(d/sig)**2)
    comb[f < fi[i]*.7] = .05
    G[:, i] = comb*(1-top) + .8*top
G = uniform_filter1d(G, 3, axis=1)
D = 5                                   # late reverb estimate from about 60 ms earlier
late = np.zeros_like(M); late[:, D:] = .45*uniform_filter1d(M, 5, axis=1)[:, :-D]
Rv = np.clip(1 - late/(M + 1e-9), .3, 1)
_, nat = istft(Z*G*Rv, sr, nperseg=N, noverlap=N-H); nat = np.pad(nat, (0, max(0, len(x)-len(nat))))[:len(x)]

# --- rebuilt: voiced frames from a single f0, consonants from the natural signal
sp = pw.cheaptrick(x, f0, t, sr); ap = pw.d4c(x, f0, t, sr)
ap = ap**1.6
y = pw.synthesize(f0, sp, ap, sr, FP)[:len(x)]; y = np.pad(y, (0, max(0, len(x)-len(y))))
vs = np.interp(np.arange(len(x))/sr, t, v.astype(float))
vs = np.convolve(vs, np.hanning(int(.02*sr))/np.hanning(int(.02*sr)).sum(), 'same')
reb = y*vs + nat*(1-vs)

def hfrac(sig_):
    f_, st_, Z_ = stft(sig_, sr, nperseg=N, noverlap=N-H); P = np.abs(Z_)**2
    fi_ = np.interp(st_, t, f0, left=0, right=0); idx = np.flatnonzero(fi_ > 0)[::4]; lo = f_ < 4000; e = h = 0
    for i in idx:
        d = np.abs(f_/fi_[i] - np.round(f_/fi_[i]))*fi_[i]
        k = lo & (f_ > fi_[i]*.7) & (d < np.maximum(10, .01*f_))
        h += P[k, i].sum(); e += P[lo & (f_ > fi_[i]*.7), i].sum()
    return 100*h/e
for n, s in [('input', x), ('natural', nat), ('rebuilt', reb)]:
    print(f'{n:8} energy on the main pitch lines {hfrac(s):5.1f}%', flush=True)
sf.write(out+'/solo_natural_raw.wav', nat/np.abs(nat).max()*.89, sr, subtype='FLOAT')
sf.write(out+'/solo_rebuilt_raw.wav', reb/np.abs(reb).max()*.89, sr, subtype='FLOAT')
