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
        self._realized_alpha = None

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

    def calc_coeff_alpha(self):
        if not isinstance(self._data, pd.DataFrame):
            print("Cannot take coeff alpha of empty data set")
            return
        vars_of_items = self._data.var(axis=0, ddof=0)
        sums_of_respondents = self._data.sum(axis=1)
        self._realized_alpha = self.num_items / (self.num_items - 1) * \
            (1 - (np.sum(vars_of_items) / np.var(sums_of_respondents)))
        return self._realized_alpha

