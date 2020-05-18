import argparse
import random

import numpy as np
import torch

class Config:
    seed = 20
    classifier = 'LogisticRegression'
    PCA = False
    pca_out_dim = 1000
    lbp = True
    hog = False
    fft = False
    test = False

args = Config()

def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--seed', type=int, default=20, help='random seed')
        parser.add_argument('--classifier', type=str, default='LogisticRegression')
        parser.add_argument('--PCA', action='store_const', default=False, const=True)
        parser.add_argument('--pca_out_dim', type=int, default=1000, help='Number of dimensions to keep after PCA')
        parser.add_argument('--lbp', action='store_const', default=False, const=True)
        parser.add_argument('--hog', action='store_const', default=False, const=True)
        parser.add_argument('--fft', action='store_const', default=False, const=True)
        args = parser.parse_args()

        # Set seeds
        torch.manual_seed(args.seed)
        random.seed(args.seed)
        np.random.seed(args.seed)

        return args

if __name__ == '__main__':
    args = parse_args()