import torch
import torch.nn.functional as F
import numpy as np

import torchxrayvision as xrv
from param import args

import feature_engineering


class FeatureExtractor:
    def __init__(self, lbp=True, hog=True, fft=True, nn=False, args_num=10000):
        assert lbp or hog or fft or nn, "no transformations specified"
        self.hog = hog
        self.lbp = lbp
        self.fft = fft
        self.nn = nn
        if nn:
            self.nn_extractor = NeuralNetFeatureExtractor()
        self.args_num=args_num

    def extract(self, dataset):
        results = []
        if self.fft or self.hog:
            comp_share=self.args_num/(self.fft+self.hog)
        #print(f'Features to be extracted: hog={self.hog}, lbp={self.lbp}, fft={self.fft}, nn={self.nn}')
        for example in dataset:
            result = []
            if self.hog:
                result = \
                    np.concatenate([result,
                                    feature_engineering.get_hog(example['img'],comp_share)
                                                       .reshape(-1)])
            if self.fft:
                result = \
                    np.concatenate([result,
                                    feature_engineering.get_fft(example['img'],comp_share)
                                                       .reshape(-1)])
            if self.lbp:
                result = \
                    np.concatenate([result,
                                    feature_engineering.get_lbp(example['img'])
                                                       .reshape(-1)])
            results.append(result)
        results = np.array(results)
        if self.nn:
            nn_features = self.nn_extractor.extract(dataset)
            results = np.concatenate([results, nn_features], axis=1)
        #print(f'Shape of the features after extraction: {np.shape(np.array(results))}')
        return results


class NeuralNetFeatureExtractor(FeatureExtractor):

    def __init__(self):
        self.model = xrv.models.DenseNet(weights='all')
        self.model.eval()
        self.model.cuda()

    def get_features(self, batch):
        # return batch['lab']
        d = batch['img'].cuda()
        features = self.model.features(d)
        out = F.relu(features, inplace=True)
        out = F.adaptive_avg_pool2d(out, (1, 1)).view(features.size(0), -1)
        out = out.cpu()
        # out = out[:, 500:501]
        # out = torch.rand(batch['img'].shape[0], 3)
        # out = torch.cat([out, batch['lab']], axis=1)
        return out

    def extract(self, dataset):
        """Returns numpy array with 1024 features for each example"""
        loader = torch.utils.data.DataLoader(dataset, batch_size=16)
        results = []
        # I'm not sure why no grad is necessary here.
        # Calling model.eval() doesn't seem to work, model runs out
        # of memory after a few batches without torch.no_grad().
        with torch.no_grad():
            for i, batch in enumerate(loader):
                features = self.get_features(batch)
                results.append(features)
        results = torch.cat(results, axis=0).numpy()
        return results
