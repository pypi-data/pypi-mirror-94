import torch
import torch.nn as nn
import torch.nn.functional as F
import svox
from math import floor
from tqdm import tqdm
import numpy as np

device = 'cuda:0'

g = svox.N3Tree().to(device=device)
#  g._refine_at(0, (0,0,0))
#  #  g.refine()
#  g.refine()
