from pathlib import Path
import typing as t

from pydantic import BaseModel, validator
from strictyaml import load, YAML

import random_forest_model

# Project Directories:
PACKAGE_ROOT = Path(random_forest_model.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
TRAINED_PIPELINES_DIR = PACKAGE_ROOT / "trained_pipelines"
DATASET_DIR = PACKAGE_ROOT / "datasets"


class AppConfig(BaseModel):
    """
    Application-level config.
    """

    package_name: str
    pipeline_name: str
    pipeline_save_file: str
    model_name: str
    model_save_file: str
    data_file: str
    training_data_file: str


class ModelConfig(BaseModel):
    """
    All configuration relevant to model
    training and feature engineering
    """
    # Modelling features:
    features_before_processing: t.Sequence[str]
    features_after_processing: t.Sequence[str]
    numerical_na_not_allowed: t.Sequence[str]
    target: str

    # Split data configuration
    random_state: int

    # Probability threshold
    proba_threshold: float

    # model configuration
    max_depth: int
    min_samples_leaf: int
    min_samples_split: int

    # the order is necessary for validation
    class_weight: str
    allowed_criterion: t.Tuple[str, ...]
    criterion: str


class Config(BaseModel):
    """Master config object"""

    app_config: AppConfig
    model_config: ModelConfig


def find_config_file() -> Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH}")


def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
    """Parse YAML containing the package configuration."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        model_config=ModelConfig(**parsed_config.data)
    )

    return _config


config = create_and_validate_config()
