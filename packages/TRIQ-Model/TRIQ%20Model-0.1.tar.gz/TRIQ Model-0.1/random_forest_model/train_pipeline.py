from random_forest_model.pipeline import pipeline
from random_forest_model.processing.data_management import save_pipeline
from random_forest_model import __version__ as _version

import logging

_logger = logging.getLogger(__name__)


def fit_pipeline() -> None:
    _logger.warning(f"saving pipeline version:{_version}")
    save_pipeline(pipeline_to_persist=pipeline)


if __name__ == '__main__':
    fit_pipeline()
