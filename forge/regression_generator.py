from forge import Generator
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

class RegressionGenerator(Generator):
    def __init__(self, params):
        super().__init__(params)
        self.scales = params['scales']
        self.num_feats = len(self.scales)
        self.data_size = (self.num_respondents, self.num_feats)
        self.target_scale = params['target_scale']
        self.betas = params['norm_betas']
        self.betas_tol = params['betas_tol']
        self.norm_features = None
        self.norm_target = None

    def __str__(self):
        return "n: {}\t f: {}\t s: {}\t b: {}\t t: {}".format(
            self.num_respondents, self.num_feats, self.scales, self.betas, self.target_scale
        )

    def _generate_data(self):
        # generate values for the independent variable, mean half of scale
        self.norm_features, norm_means = self._gen_normalized_features_for_betas()

        # generate values for dependent variable so the covariance matches beta * var(x)
        vals_to_match = [self.betas[i] * np.var(self.norm_features[i]) for i in range(self.num_feats)]

        self.norm_target = self._gen_normalized_target_for_features(self.norm_features, norm_means, vals_to_match)

        self._data = self._gen_data_from_normalized_features(self.norm_features, self.norm_target)

    def _gen_normalized_features_for_betas(self):
        features = []
        means = [0.5 for s in self.scales]
        stds = [0.2 for s in self.scales]
        
        for i in range(self.num_feats):
            features.append(np.random.normal(means[i], stds[i], self.num_respondents))

        return features, means

    def _gen_normalized_target_for_features(self, norm_features, norm_means, vals_to_match):
        target = []
        target_mean = 0.5
        target_std = 0.2

        residual_mean = 0.0
        residual_std = 0.15

        # assume just one feature
        val_to_match = vals_to_match[0] * (self.num_respondents - 1)
        for i in range(self.num_respondents):
            feat_diff = norm_features[0][i] - norm_means[0]
            target_sample = np.random.normal(target_mean, target_std, 1)[0]
            target_diff = target_sample - target_mean
            prod = feat_diff * target_diff

            while prod > val_to_match:
                target_sample = np.random.normal(target_mean, target_std, 1)[0]
                target_diff = target_sample - target_mean
                prod = feat_diff * target_diff

            residual = np.random.normal(residual_mean, residual_std, 1)[0]
            target_sample += residual
            target.append(target_sample)
            val_to_match -= prod

        return target

    def _is_valid(self):
        reg = LinearRegression().fit(self.norm_features[0].reshape(-1, 1), self.norm_target)
        if np.absolute(reg.coef_[0] - self.betas[0]) < self.betas_tol[0]:
            return True
        return False

    def _gen_data_from_normalized_features(self, norm_features, norm_targets):
        data = pd.DataFrame(
            index=["r{}".format(r) for r in range(self.num_respondents)],
            columns=["f{}".format(i) for i in range(self.num_feats)] + ["t0"]
        )

        for i in range(self.num_feats):
            feat = norm_features[i] * self.scales[i]
            data.iloc[:,i] = feat

        target = [t * self.target_scale for t in norm_targets]
        data.iloc[:,-1] = target

        return data

