from typing import Any, Optional

from aporia.core.errors import AporiaError
from aporia.inference.inference_model import InferenceModel

try:
    import numpy
    import pandas

    import aporia.training

    ndarray = numpy.ndarray
    DataFrame = pandas.DataFrame
    TRAINING_ENABLED = True

except ImportError:
    ndarray = Any
    DataFrame = Any
    TRAINING_ENABLED = False


class Model(InferenceModel):
    """Model object for logging model events."""

    def __init__(self, model_id: str, model_version: str):
        """Initializes an model object.

        Args:
            model_id: Model identifier, as received from the Aporia dashboard.
            model_version: Model version - this can be any string that represents the model
                version, such as "v1" or a git commit hash.
        """
        super().__init__(model_id=model_id, model_version=model_version)

        self._training = None
        if TRAINING_ENABLED:
            self._training = aporia.training.TrainingModel(
                model_id=model_id, model_version=model_version
            )

    def log_training_set(
        self, features: DataFrame, labels: DataFrame, raw_inputs: Optional[DataFrame] = None  # type: ignore
    ):
        """Logs training data.

        Args:
            features: Training set features
            labels: Training set labels
            raw_inputs: Training set raw inputs. Defaults to None.

        Notes:
            * Each dataframe corresponds to a field category defined in create_model_version:
                * features -> features
                * labels -> predictions
                * raw_inputs -> raw_inputs
            * Each column in the dataframe should match a field defined in create_model_version
                * Missing fields will be handled as missing values
                * Columns that do not match a defined field will be ignored
                * The column name must match the field name
            * This function is blocking and may take a while to finish running.
        """
        with self._handle_error("{}"):
            if self._training is None:
                raise AporiaError(
                    short_message="Logging training data failed, Aporia training extension not found",
                    verbose_message=(
                        "The Aporia training extension is required to log training data. "
                        "Install it with `pip install aporia[training] and try again."
                    ),
                )

            self._training.log_training_set(features=features, labels=labels, raw_inputs=raw_inputs)

    def log_test_set(
        self,
        features: DataFrame,  # type: ignore
        predictions: DataFrame,  # type: ignore
        labels: DataFrame,  # type: ignore
        raw_inputs: Optional[DataFrame] = None,  # type: ignore
        confidences: Optional[ndarray] = None,  # type: ignore
    ):
        """Logs test data.

        Args:
            features: Test set features
            predictions: Test set predictions
            labels: Test set labels
            raw_inputs: Test set raw inputs. Defaults to None.
            confidences: Confidence values for the test predictions. Defaults to None.

        Notes:
            * Each dataframe corresponds to a field category defined in create_model_version:
                * features -> features
                * predictions -> predictions
                * labels -> predictions
                * raw_inputs -> raw_inputs
            * Each column in the dataframe should match a field defined in create_model_version
                * Missing fields will be handled as missing values
                * Columns that do not match a defined field will be ignored
                * The column name must match the field name
            * This function is blocking and may take a while to finish running.
        """
        with self._handle_error("{}"):
            if self._training is None:
                raise AporiaError(
                    short_message="Logging test data failed, Aporia training extension not found",
                    verbose_message=(
                        "The Aporia training extension is required to log test data. "
                        "Install it with `pip install aporia[training] and try again."
                    ),
                )

            self._training.log_test_set(
                features=features,
                predictions=predictions,
                labels=labels,
                raw_inputs=raw_inputs,
                confidences=confidences,
            )
