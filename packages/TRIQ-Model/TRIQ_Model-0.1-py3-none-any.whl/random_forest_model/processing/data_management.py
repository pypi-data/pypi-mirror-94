from pathlib import Path

import pandas as pd
import joblib
from sklearn.pipeline import Pipeline

from random_forest_model.config.core import config, \
    DATASET_DIR, \
    TRAINED_MODEL_DIR, \
    TRAINED_PIPELINES_DIR
from random_forest_model import __version__ as _version

import logging
import typing as t

_logger = logging.getLogger(__name__)


def load_dataset(*, path: Path = DATASET_DIR, file_name: str, ) -> pd.DataFrame:
    """
        Loads the data into a pandas dataframe and retains
        the columns necessary for modelling
    """
    dataframe = pd.read_csv(f"{path}/{file_name}")

    return dataframe


def save_model(*, model_to_persist) -> None:
    """Persist the model.

    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.model_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_artifacts(files_to_keep=[save_file_name])
    joblib.dump(model_to_persist, save_path)
    _logger.info(f"saved model: {save_file_name}")


def load_model(*, file_name: str):
    """Load a persisted model."""

    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


def save_pipeline(*, pipeline_to_persist) -> None:
    """Persist the pipeline.
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_PIPELINES_DIR / save_file_name

    remove_old_artifacts(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)
    _logger.info(f"saved pipeline: {save_file_name}")


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_PIPELINES_DIR / file_name
    pipeline = joblib.load(filename=file_path)
    return pipeline


def remove_old_artifacts(*, files_to_keep: t.List[str]) -> None:
    """
       Remove old models and pipelines.
       This is to ensure there is a simple one-to-one
       mapping between the package version and the model
       version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]

    if files_to_keep.__contains__("pipeline"):
        DIR = TRAINED_PIPELINES_DIR
    else:
        DIR = TRAINED_MODEL_DIR

    for model_file in DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()


if __name__ == '__main__':
    for model_file in TRAINED_MODEL_DIR.iterdir():
        print(model_file)