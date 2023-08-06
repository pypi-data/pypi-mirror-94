#  import torch
#  import torch.nn.functional as F
import numpy as np
import svox
from math import floor
from tqdm import tqdm
import numpy as np

device = 'cuda:0'
K = 4
NN = 4
N = 64

g = svox.N3Tree(N=NN, depth_limit=1000)
gt = np.zeros((N, N, N, K), dtype=np.float32)

g.refine(repeats=2)
g.shrink_to_fit()


print('begin fuzz')
worst = 0.0

def xyz_to_int(q):
    x = int(floor(q[0, 0] * N))
    y = int(floor(q[0, 1] * N))
    z = int(floor(q[0, 2] * N))
    return x, y, z

for i in tqdm(range(5000)):
    if np.random.rand() < 0.5:
        q = np.random.rand(1, 3).astype(np.float32)
        vals = 100 * np.random.randn(1, K).astype(np.float32)

        x, y, z = xyz_to_int(q)
        gt[x, y, z] = vals[0]
        g.set(q, vals, cuda=True)

    # ---

    q = np.random.rand(1, 3).astype(np.float32)
    x, y, z = xyz_to_int(q)
    rt = gt[x, y, z]

    r = g(q, cuda=True)[0]
    err = np.abs(r - rt).max()
    worst = max(err, worst)
    if err > 5e-5:
        print(i, err.item(), 'q', q[0].detach().cpu().numpy(),
                'g', r.detach().cpu().numpy(), 'gt', rt.detach().cpu().numpy(),
                 x, y, z)
        break
print('worst', worst)

