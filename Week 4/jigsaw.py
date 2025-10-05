import numpy as np, random, math, scipy.io, matplotlib.pyplot as plt

# ----------- Load image from .mat -----------
mat = scipy.io.loadmat('scrambled_lena.mat')
# assume the image array is called 'img' in .mat
img = mat['img']
if img.ndim == 3 and img.shape[2]==1: img = img[:,:,0]
img = (img - img.min()) / (img.max()-img.min()) * 255
img = img.astype(np.uint8)

tile_h, tile_w = 32, 32        # adjust to match the tiles
R, C = img.shape[0]//tile_h, img.shape[1]//tile_w

# ----------- Cut into tiles -----------
tiles = [img[r*tile_h:(r+1)*tile_h, c*tile_w:(c+1)*tile_w] 
         for r in range(R) for c in range(C)]

# ----------- Energy function -----------
def energy(perm):
    e = 0
    for r in range(R):
        for c in range(C):
            idx = perm[r*C + c]
            if c < C-1: e += np.sum((tiles[idx][:, -1]-tiles[perm[r*C + c +1]][:,0])**2)
            if r < R-1: e += np.sum((tiles[idx][-1,:]-tiles[perm[(r+1)*C+c]][0,:])**2)
    return e

# ----------- Simulated annealing -----------
N = R*C
perm = list(range(N))
random.shuffle(perm)
E = energy(perm)
T = 1000; alpha=0.99
best_perm, best_E = perm[:], E

for _ in range(10000):
    i,j = random.sample(range(N),2)
    perm[i], perm[j] = perm[j], perm[i]
    E2 = energy(perm)
    dE = E2 - E
    if dE <0 or random.random() < math.exp(-dE/T): E,E2 = E2,E2
    else: perm[i], perm[j] = perm[j], perm[i]
    if E < best_E: best_E,best_perm = E,perm[:]
    T *= alpha

# ----------- Reconstruct image -----------
recon = np.zeros_like(img)
for r in range(R):
    for c in range(C):
        recon[r*tile_h:(r+1)*tile_h, c*tile_w:(c+1)*tile_w] = tiles[best_perm[r*C+c]]

plt.imshow(recon, cmap='gray'); plt.axis('off'); plt.show()
