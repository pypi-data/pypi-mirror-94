from sklearn.pipeline import Pipeline

from random_forest_model.processing import preprocessors as pp
from random_forest_model.config.core import config

import logging

_logger = logging.getLogger(__name__)

pipeline = Pipeline(
    [
        ('CreateHeartRateVariability',
         pp.CreateHeartRateVariability(
             mean_frequency=['herzfrequency'],
             max_frequency=['maximale_herzfrequenz'])
         )
    ]
)
