import numpy as np
import pandas as pd

class Generator(object):
    def __init__(self, params):
        self.num_respondents = params['num_respondents']
        self.num_items = params['num_items']
        self.scale_max = params['scale']
        self.alpha = params['coeff_alpha']
        self.data_size = (self.num_respondents, self.num_items)
        self._data = None

    def __str__(self):
        return "n: {}\t i: {}\t s: {}\t a: {}".format(
            self.num_respondents, self.num_items, self.scale_max, self.alpha
        )

    def generate_random_data(self):
        self._data = pd.DataFrame(
            np.random.randint(1, self.scale_max+1, size=self.data_size),
            index=["r{}".format(r) for r in range(self.num_respondents)],
            columns=["i{}".format(i) for i in range(self.num_items)]
        )
        return self._data

