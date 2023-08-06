import torch
import torch.nn.functional as F
import svox
from tqdm import tqdm

device='cuda:3'

g = svox.N3Tree(N=4, data_dim=3).to(device=device)

N = 12582912
#  N = 50331648
K = g.data_dim

torch.cuda.set_device(device)
start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)
torch.cuda.synchronize(device)

start.record()

print('prep')
print('begin refine')
g.refine(repeats=2)
for j in tqdm(range(5000)):
    for i in range(10):
        g._refine_at(j, torch.randint(0, g.N, (3,)))
    for i in range(20):
        q = torch.rand((1, 3), device=device)
        vals = 100 * torch.randn((1, K), device=device)
        g.set(q, vals)
print(g)
print(g.n_leaves)

end.record()
torch.cuda.synchronize(device)
print('refine time', start.elapsed_time(end) / 10000, 'ms')

if False:
    torch.cuda.synchronize(device)
    print('begin fuzz')
    worst = 0.0
    for i in range(5000):
        q = torch.rand((1, 3), device=device)
        vals = 100 * torch.randn((1, K), device=device)
        g.set(q, vals)
        if i % 1000 == 999:
            for j in tqdm(range(1000, 1500)):
                for k in range(10):
                    g.refine_at(j, torch.randint(0, g.N, (3,)))
            print('terr', worst.item())
        r = g(q + 0.00000001 * (torch.rand_like(q) - 0.5))
        worst = max(torch.abs(r - vals).max(), worst)
    print('err', worst.item())
    print('internal count', g.n_internal, 'max depth', g.max_depth)
    print('shape', g.data.shape)

if True:
    print('begin timing')
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    q = torch.rand((N, 3), device=device)
    torch.cuda.synchronize(device)
    start.record()

    for i in range(20):
        r = g(q)
        r.sum().backward()

    end.record()
    torch.cuda.synchronize(device)
    print('time', start.elapsed_time(end) / 20, 'ms')

    X = torch.randn(1, 3, 128, 128, 128, device=device)
    G = torch.rand((1, 1, 1, N, 3), device=device) * 2 - 1

    # ----

    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    torch.cuda.synchronize(device)

    X.requires_grad_(True)

    start.record()
    for i in range(20):
        r = F.grid_sample(X, G, mode='bilinear', align_corners=True)
        r.sum().backward()

    end.record()
    torch.cuda.synchronize(device)
    print('time', start.elapsed_time(end) / 20, 'ms')
