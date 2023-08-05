import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from typing import List

from random_forest_model.config.core import config


class CreateHeartRateVariability(BaseEstimator, TransformerMixin):
    """Estime time between training sessions."""

    def __init__(self, mean_frequency=None, max_frequency=None) -> None:
        if not isinstance(mean_frequency, list):
            self.mean_frequency = mean_frequency
            self.max_frequency = max_frequency
        else:
            self.mean_frequency = mean_frequency[0]
            self.max_frequency = max_frequency[0]

    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> "CreateHeartRateVariability":
        """Fit statement to accomodate the sklearn pipeline."""

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply the transforms to the dataframe."""

        X = X.copy()
        X['HRV'] = X[self.max_frequency] - X[self.mean_frequency]
        X.drop(['herzfrequency','maximale_herzfrequenz'], axis=1, inplace=True)

        return X