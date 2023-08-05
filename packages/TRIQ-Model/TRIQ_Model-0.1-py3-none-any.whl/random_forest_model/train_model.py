from random_forest_model.processing.data_management import (
    load_dataset,
    load_pipeline,
    save_model
)
from random_forest_model.config.core import config
from random_forest_model import __version__ as _version
from sklearn.ensemble import RandomForestClassifier

import logging

_logger = logging.getLogger(__name__)

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_data_pipeline = load_pipeline(file_name=pipeline_file_name)


def run_training() -> None:
    """Train the model"""

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)

    # Transform input data
    data_transformed = _data_pipeline.fit_transform(data)

    X = data_transformed[config.model_config.features_after_processing]
    y = data_transformed[config.model_config.target]

    model = RandomForestClassifier(class_weight=config.model_config.class_weight,
                                   criterion=config.model_config.criterion,
                                   random_state=config.model_config.random_state,
                                   max_depth=config.model_config.max_depth,
                                   min_samples_leaf=config.model_config.min_samples_leaf,
                                   min_samples_split=config.model_config.min_samples_split) \
        .fit(X, y)

    _logger.warning(f"saving model version:{_version}")
    save_model(model_to_persist=model)


if __name__ == '__main__':
    run_training()
