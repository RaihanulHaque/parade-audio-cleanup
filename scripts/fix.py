import sys, numpy as np, soundfile as sf
x, sr = sf.read(sys.argv[1], always_2d=True); L, R = x[:,0], x[:,1]
k = (L @ R) / (L @ L)             # least-squares gain mapping L onto R (negative = inverted)
m = (R + k*L) / 2                 # align polarity and level, then average to reduce independent codec noise
print('k', round(k,3), 'residual dB', round(10*np.log10(((R-k*L)**2).mean()/(R**2).mean()),1), 'mono level vs R dB', round(10*np.log10((m**2).mean()/(R**2).mean()),2))
p = np.abs(m).max(); print('peak', round(p,3))
m = m/p*.95 if p > .95 else m
sf.write(sys.argv[2], np.stack([m,m],1), sr, subtype='FLOAT')
