import numpy as np
import pandas as pd

class Generator(object):
    def __init__(self, params):
        self.num_respondents = params['num_respondents']
        self.num_items = params['num_items']
        self.scale_max = params['scale']
        self.scale_min = 1
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
            np.random.randint(self.scale_min, self.scale_max+1, size=self.data_size),
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

    def _gen_means_for_items(self):
        # assume each scale value occurs an equal number of times as the mean for an item
        results = []
        for s in range(self.scale_min, self.scale_max+1):
            results.extend([s for _ in range(int(self.num_items / self.scale_max))])

        return results

    def _gen_scores(self, sum_of_scores):
        # assume scores are normally distributed
        # mean for scores is sum of scores / num respondents
        # normalized std is 1
        min_score = self.scale_min * self.num_items
        max_score = self.scale_max * self.num_items
        mean_score = sum_of_scores / self.num_respondents
        norm_std = 0.2
        if min_score > mean_score or max_score < mean_score:
            print("Mean score falls out of score range")

        # take the smaller distance from mean, mult by normalized std
        left_range = mean_score - min_score
        right_range = max_score - mean_score
        actual_std = left_range if left_range > right_range else right_range
        actual_std *= norm_std

        # sample normally with given characteristics
        scores = np.random.normal(mean_score, actual_std, self.num_respondents)

        # make these integers
        scores = np.round(scores).astype(np.int)
        diff = sum_of_scores - np.sum(scores)

        # distribute diff back into scores
        while np.absolute(diff) > 0:
            adjustment = np.random.randint(0, (diff/self.num_respondents)+2) if diff > 0 else np.random.randint((diff/self.num_respondents)-1, 0)
            idx = np.random.randint(0, len(scores))
            if scores[idx] + adjustment >= min_score and scores[idx] + adjustment <= max_score:
                scores[idx] += adjustment
                diff -= adjustment
        
        return scores

    def _gen_variances_for_items(self, value_to_match, variance_of_scores):
        # sum of variances for items needs to equal this
        value_to_match *= variance_of_scores
        rem_to_match = value_to_match

        variances = []
        for i in range(self.num_items):
            var = rem_to_match/(self.num_items - i) * np.random.random_sample()
            variances.append(var)
            rem_to_match -= var

        # distribute diff back into variances
        while np.absolute(rem_to_match) > 0.0001:
            adjustment = 2 * rem_to_match / self.num_items * np.random.random_sample()
            idx = np.random.randint(0, len(variances))
            if variances[idx] + adjustment > 0:
                variances[idx] += adjustment
                rem_to_match -= adjustment

        return variances

    def _gen_data_with_distributions(self, scores, variance_of_scores, mean_per_item, variance_per_item):
        data = pd.DataFrame(
            index=["r{}".format(r) for r in range(self.num_respondents)],
            columns=["i{}".format(i) for i in range(self.num_items)]
        )
        rem_scores = scores

        for i, m in enumerate(mean_per_item):
            #data.iloc[:,i] = np.random.normal(m, variance_per_item[i], self.num_respondents) 
            n = self.scale_max
            p = (-1 + np.sqrt(1 + 4 * variance_per_item[i])) / 2
            vals_for_item = np.random.binomial(n, p if p < 1 else 1, self.num_respondents) 
            
            # prevent item values from exceeding scores for respondents
            vals_to_use = np.minimum(rem_scores, vals_for_item)
            rem_scores -= vals_to_use
            data.iloc[:,i] = vals_to_use

        # need to make item responses match score distribution
        sums_of_respondents = data.sum(axis=1)
        realized_var_of_scores = np.var(sums_of_respondents)
        print(realized_var_of_scores, variance_of_scores)

        return data

    def generate_data_to_match_alpha(self):
        # goal is to make sum of variance in item responses / variance in 
        # respondent scores equal this value
        value_to_match = 1 - ((self.num_items - 1) / self.num_items) * self.alpha        

        # the mean and covariance need to be determined for each item
        # we can set the mean for each time, the sum of which will equal the
        # sum of the scores for each respondent
        mean_per_item = self._gen_means_for_items()
        sum_of_scores = np.sum(mean_per_item) * self.num_respondents

        # distribution of scores
        scores = self._gen_scores(sum_of_scores)
        variance_of_scores = np.var(scores)

        # generate variance for each item
        variance_per_item = self._gen_variances_for_items(value_to_match, variance_of_scores)

        # sample values for items such that the score is met for each respondent
        self._data = self._gen_data_with_distributions(scores, variance_of_scores, mean_per_item, variance_per_item)

