import logging
import typing as t

import numpy as np
import pandas as pd

from random_forest_model import __version__ as _version
from random_forest_model.config.core import config
from random_forest_model.processing.data_management import load_model, load_pipeline
from random_forest_model.processing.validation import validate_inputs

_logger = logging.getLogger(__name__)

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
model_file_name = f"{config.app_config.model_save_file}{_version}.pkl"

_data_pipeline = load_pipeline(file_name=pipeline_file_name)
_predict_model = load_model(file_name=model_file_name)


def make_prediction(*, input_data: t.Union[pd.DataFrame, dict], ) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)

    validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions_proba": None,
               "predictions": None,
               "version": _version,
               "errors": errors}

    if not errors:
        validated_data_transformed = _data_pipeline \
            .fit_transform(validated_data[config.model_config.features_before_processing])

        predictions_proba = _predict_model \
            .predict_proba(X=validated_data_transformed)[:, 1]

        predictions = np.where(
            predictions_proba >= config.model_config.proba_threshold,
            1, 0)

        _logger.info(
            f"Making predictions with model version: {_version} "
            f"Predictions: {predictions}"
        )

        results = {"predictions_proba": predictions_proba,
                   "predictions": predictions,
                   "version": _version,
                   "errors": errors}

    return results