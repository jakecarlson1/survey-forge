from forge import Generator
import numpy as np
import pandas as pd

class RegressionGenerator(Generator):
    def __init__(self, params):
        super().__init__(params)
        self.scales = params['scales']
        self.num_feats = len(self.scales)
        self.data_size = (self.num_respondents, self.num_feats)
        self.target_scale = params['target_scale']
        self.betas = params['norm_betas']

    def __str__(self):
        return "n: {}\t f: {}\t s: {}\t b: {}\t t: {}".format(
            self.num_respondents, self.num_feats, self.scales, self.betas, self.target_scale
        )

    def generate_data(self):
        # generate values for the independent variable, mean half of scale
        norm_features, norm_means = self._gen_normalized_features_for_betas()

        # generate values for dependent variable so the covariance matches beta * var(x)
        vals_to_match = [self.betas[i] * np.var(norm_features[i]) for i in range(self.num_feats)]

        norm_target = self._gen_normalized_target_for_features(norm_features, norm_means, vals_to_match)

    def _gen_normalized_features_for_betas(self):
        features = []
        means = [0.5 for s in self.scales]
        stds = [0.2 for s in self.scales]
        
        for i in range(self.num_feats):
            features.append(np.random.normal(means[i], stds[i], self.num_respondents))
            print(features[i])

        return features, means

    def _gen_normalized_target_for_features(self, norm_features, norm_means, vals_to_match):
        target = []

        return target

