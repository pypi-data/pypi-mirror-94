import typing as t

from random_forest_model.config.core import config

import numpy as np
import pandas as pd
from marshmallow import fields, Schema, ValidationError


class UserInputSchema(Schema):
    distanz = fields.Float()
    herzfrequency = fields.Float()
    maximale_herzfrequenz = fields.Float()
    aerober_te = fields.Float()
    last_aerober_te = fields.Float()


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter"""
    validated_data = input_data.copy()
    if input_data[config.model_config.features_before_processing].isnull().any().any():
        validated_data = validated_data.dropna(
            axis=0, subset=config.model_config.numerical_na_not_allowed
        )

    return validated_data


def validate_inputs(
        *, input_data: pd.DataFrame
) -> t.Tuple[pd.DataFrame, t.Optional[dict]]:
    """Check model inputs for unprocessable values"""

    # convert syntax error field names (beginning with numbers):
    validated_data = drop_na_inputs(input_data=input_data)

    # set many=True to allow passing in a list
    schema = UserInputSchema(many=True)
    errors = None

    try:
        # replace numpy nans so that Marshmallow can validate
        schema.load(validated_data.replace({np.nan: None}).to_dict(orient="records"))
    except ValidationError as exc:
        errors = exc.messages

    return validated_data, errors
