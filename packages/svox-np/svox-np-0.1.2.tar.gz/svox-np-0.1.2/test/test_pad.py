import torch
import svox

#  device = 'cuda:0'
device = 'cpu'
t1 = svox.N3Tree(padding_mode="zeros").to(device=device)
t2 = svox.N3Tree(padding_mode="border").to(device=device)

t1[:] = 3.0
t2[:] = 3.0

pts = torch.tensor([[0.5, 0.5, 0.5], [-1, -1, -1], [1.0, 1, 1], [0.5, 0.5, 2]],
        device=device)
with torch.no_grad():
    r1 = t1(pts, cuda=False)
    r2 = t2(pts, cuda=False)

print(r1)
print(r2)

print((r1[0] == 3).all().item(), 'expect r1[0]==3, pass?')
print((r1[1:] == 0).all().item(), 'expect r1[1:]==0, pass?')
print((r2 == 3).all().item(), 'expect r2==3, pass?')
