from forge import Generator
import numpy as np
import pandas as pd

class AnovaGenerator(Generator):
    def __init__(self, params):
        super().__init__(params)
        self.num_groups = params['num_groups']
        self.data_size = (self.num_respondents, self.num_groups)
        self.size = self.data_size[0] * self.data_size[1]
        self.f = params['f_stat']
        self.scale = params['scale']

    def __str__(self):
        return "n: {}\t g: {}\t s: {}".format(
            self.num_respondents, self.num_groups, self.scale
        )

    def generate_data(self):
        means_for_groups = self._gen_means_for_groups()

        overall_mean = np.mean(means_for_groups)

        sst = self._calc_sum_squares_of_treatment(means_for_groups, overall_mean)

        value_to_match = sst / (self.num_groups - 1) / self.f * (self.size - self.num_groups)

        self._data = self._gen_data_to_match_sum_square_error(value_to_match, means_for_groups)

    def _gen_means_for_groups(self):
        return np.random.randint(1, self.scale, self.num_groups)

    def _calc_sum_squares_of_treatment(self, means, overall):
        return (self.num_groups - 1) * np.sum([(m - overall)**2 for m in means])

    def _gen_data_to_match_sum_square_error(self, sse, means):
        return []

    def is_valid(self):
        return True

