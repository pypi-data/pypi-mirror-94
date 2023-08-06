#  import torch
#  import torch.nn.functional as F
import numpy as np
import svox

#  device='cuda:3'
K = 4

g = svox.N3Tree(N=2) #.to(device=device)

for i in range(10):
    #  q = torch.rand((1, 3), device=device)
    #  vals = torch.randn((1, K), device=device)
    q = np.random.rand(1, 3).astype(np.float32)
    vals = np.random.rand(1, K).astype(np.float32)
    g.set(q, vals, cuda=True)

g._refine_at(0, (0, 0, 0))
print(g)
g.shrink_to_fit()
print(g)
#  q = torch.tensor([[0.9,0.9,0.9], [0.49, 0.49, 0.49]], device=device)
#  vals = torch.tensor([[0.0, 1.0, 1.0, 10.0], [1.0, 0.49, 0.49, 0.49]], device=device)
q = np.array([[0.9,0.9,0.9], [0.49, 0.49, 0.49]], dtype=np.float32)
vals = np.array([[0.0, 1.0, 1.0, 10.0], [1.0, 0.49, 0.49, 0.49]], dtype=np.float32)
g.set(q, vals, cuda=True)
r=g.get(q, cuda=True)
print(r)
print(vals)

