from forge import Generator
import numpy as np
import pandas as pd
from scipy import stats

class AnovaGenerator(Generator):
    def __init__(self, params):
        super().__init__(params)
        self.num_groups = params['num_groups']
        self.data_size = (self.num_respondents, self.num_groups)
        self.size = self.data_size[0] * self.data_size[1]
        self.f = params['f_stat']
        self.scale = params['scale']
        self.f_tol = params['f_stat_tol']

    def __str__(self):
        return "n: {}\t g: {}\t s: {}\t f:{}\t tol:{}".format(
            self.num_respondents, self.num_groups, self.scale, self.f, self.tol
        )

    def generate_data(self):
        self._data = None
        while self._data == None or not self.is_valid():
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
        group_match = sse / self.num_groups

        results = []
        for i in range(self.num_groups):
            group_data = self._gen_data_with_mean_and_squared_deviation(means[i], group_match)
            results.append(group_data)

        return results

    def _gen_data_with_mean_and_squared_deviation(self, mean, sdev):
        std = 0.8
        approx_value = np.sqrt(sdev/self.num_respondents) + mean
        return np.random.normal(1, std, self.num_respondents) * approx_value

    def is_valid(self):
        F, p = stats.f_oneway(*self._data)
        if np.absolute(F - self.f) < self.f_tol:
            return True
        return False

