import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

import torchvision
from collections import OrderedDict
import torchvision.transforms as transforms

# =========== configuration ==============
M = 5.0; alpha = 0.01
transform = transforms.Compose(
                [transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

def getLoader(phase, download=False):
    if phase=='train':
        trainset = torchvision.datasets.CIFAR10(root='.', train=True, transform=transform, download=download)
        loader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True, num_workers=4)
    else:
        testset = torchvision.datasets.CIFAR10(root='.', train=False, transform=transform, download=download)
        loader = torch.utils.data.DataLoader(testset, batch_size=1)
    return loader

class BaseNet(nn.Module):
    def __init__(self):
        super(BaseNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return x

def create_net():
    net = nn.Sequential(BaseNet(), nn.Linear(84,10))
    snet = nn.Sequential(BaseNet(), nn.Linear(84, 1), nn.Sigmoid())
    return net, snet

if __name__=='__main__':
    pass