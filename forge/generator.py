import numpy as np
import pandas as pd

class Generator(object):
    def __init__(self, params):
        self.num_respondents = params['num_respondents']
        self.data_size = (self.num_respondents, self.num_items)
        self._data = None
        self.output_file = params['output_file']

    def __str__(self):
        return "n: {}\t i: {}\t s: {}\t a: {}".format(
            self.num_respondents, self.num_items, self.scale_max, self.alpha
        )

    def generate_random_data(self):
        self._data = pd.DataFrame(
            np.random.randint(self.scale_min, self.scale_max+1, size=self.data_size),
            index=["r{}".format(r) for r in range(self.num_respondents)],
            columns=["i{}".format(i) for i in range(self.num_items)]
        )

        return self._data

    def generate_data(self):
        pass

    def write(self):
        if not isinstance(self._data, pd.DataFrame):
            print("No data to print")
            return

        self._data.to_csv(self.output_file)

