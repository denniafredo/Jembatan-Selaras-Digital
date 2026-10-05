"""Phase 1/2 measurement: unmix the JPG into blue / gray coverage and measure each semantic part.

Coverage model: pixel = w*White + b*Blue + g*Gray (least squares, clipped to [0,1]).
"""
import json
import numpy as np
from PIL import Image
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parents[1] / 'source.jpg'
a = np.asarray(Image.open(SRC).convert('RGB')).astype(float)
H, W, _ = a.shape
WHITE = np.array([253, 253, 253.]); BLUE = np.array([6, 148, 214.]); GRAY = np.array([81, 98, 112.])
M = np.stack([BLUE - WHITE, GRAY - WHITE], axis=1)
d = (a - WHITE).reshape(-1, 3) @ np.linalg.pinv(M).T
blue = np.clip(d[:, 0], 0, 1).reshape(H, W)
gray = np.clip(d[:, 1], 0, 1).reshape(H, W)
np.save(HERE / 'blue_cov.npy', blue.astype(np.float32))
np.save(HERE / 'gray_cov.npy', gray.astype(np.float32))

print('size', W, H, 'mode RGB, no alpha')
print('background median', np.median(a[(blue < .05) & (gray < .05)], axis=0))
smudge = (a.mean(axis=2) < 248) & (blue < .1) & (gray < .1)
ys, xs = np.nonzero(smudge)
print('faint smudge px', smudge.sum(), 'bbox', xs.min(), xs.max(), ys.min(), ys.max(), 'median', np.median(a[smudge], axis=0))

B = blue > .5; G = gray > .5
for name, m in [('blue', B), ('gray', G)]:
    ys, xs = np.nonzero(m)
    print(name, 'bbox x', xs.min(), xs.max(), 'y', ys.min(), ys.max(), 'px', m.sum())
