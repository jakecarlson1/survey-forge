from forge import Generator
import numpy as np
import pandas as pd

class RegressionGenerator(Generator):
    def __init__(self, params):
        super().__init__(params)
        self.scales = params['scales']
        self.num_feats = len(self.scales)
        self.data_size = (self.num_respondents, self.num_feats)
        self.pred_scale = params['pred_scale']
        self.betas = params['norm_betas']

    def __str__(self):
        return "n: {}\t f: {}\t s: {}\t b: {}\t".format(
            self.num_respondents, self.num_feats, self.scales, self.betas
        )

