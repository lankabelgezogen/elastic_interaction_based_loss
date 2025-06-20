import os

from argparse import ArgumentParser

from unet.model import Model
from unet.dataset import Image2D
from unet.elastic_loss import EnergyLoss
import torch.optim as optim
import torch

parser = ArgumentParser()
parser.add_argument('--dataset', required=True, type=str)
parser.add_argument('--results_path', required=True, type=str)
parser.add_argument('--model_path', required=True, type=str)
parser.add_argument('--device', default='cpu', type=str)
args = parser.parse_args()

predict_dataset = Image2D(args.dataset)
unet = torch.load(args.model_path, weights_only=False)

if not os.path.exists(args.results_path):
    os.makedirs(args.results_path)

loss = EnergyLoss(alpha=0.35)
optimizer = optim.Adam(unet.parameters(), lr=1e-3)

model = Model(unet, loss, optimizer, checkpoint_folder=args.results_path, device=args.device)

model.predict_dataset(predict_dataset, args.results_path)
