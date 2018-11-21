import numpy as np
import pandas as pd

class Generator(object):
    def __init__(self, params):
        self.num_respondents = params['num_respondents']
        self.data_size = (self.num_respondents, 0)
        self._data = None
        self.output_file = params['output_file']

    def generate_random_data(self):
        self._data = pd.DataFrame(
            np.random.randint(self.scale_min, self.scale_max+1, size=self.data_size),
            index=["r{}".format(r) for r in range(self.num_respondents)],
            columns=["i{}".format(i) for i in range(self.num_items)]
        )

        return self._data

    def generate_data(self):
        while not isinstance(self._data, pd.DataFrame) or not self._is_valid():
            self._generate_data()

    def write(self):
        if not isinstance(self._data, pd.DataFrame):
            print("No data to print")
            return

        self._data.to_csv(self.output_file)

