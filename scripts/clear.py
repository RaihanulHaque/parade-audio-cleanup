"""Stage 1: de-boot vocals and band, soft-gate vocals, save for the clarity chain."""
import sys, os, re
import numpy as np, soundfile as sf
src = open(sys.argv[3]).read().split("v, sr = load('vocals')")[0]
sys.argv = ['x', sys.argv[1], sys.argv[2]]
exec(src)
v, sr = load('vocals'); d, _ = load('drums'); b, _ = load('bass'); o, _ = load('other')
V_PTS = [(20, .10), (250, .15), (800, .65), (2000, .90), (4000, 1.0), (22050, 1.0)]
O_PTS = [(20, .10), (400, .12), (1500, .40), (6000, .70), (22050, .70)]
vc = desuppress(v, sr, V_PTS)
vg, frac = gate(vc, sr, -12, thr_db=-45)
print('gate open', round(frac, 3))
band = desuppress(o, sr, O_PTS) + desuppress(b, sr, O_PTS) + d * 10**(-30/20)
sf.write(out_dir + '/v_in.wav', vg, sr, subtype='FLOAT'); sf.write(out_dir + '/band_in.wav', band, sr, subtype='FLOAT')
