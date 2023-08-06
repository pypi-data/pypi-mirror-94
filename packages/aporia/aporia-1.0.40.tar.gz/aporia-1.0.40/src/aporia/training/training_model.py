from functools import lru_cache
import logging
from typing import Dict, List, Optional, Tuple

from numpy import ndarray
from pandas import DataFrame
from pandas.io.json import build_table_schema

from aporia.core.base_model import BaseModel, validate_model_ready
from aporia.core.errors import AporiaError
from aporia.core.logging_utils import LOGGER_NAME
from aporia.core.types.field import FieldCategory, FieldType
from .api.get_model_version import get_model_version
from .api.log_training import (
    calculate_training_data,
    FieldTrainingData,
    log_test_data,
    log_training_data,
)

TRAINING_DATASET_NAME = "training"
TEST_DATASET_NAME = "test"
FIELD_TYPE_TO_TABLE_SCHEMA_TYPES = {
    FieldType.NUMERIC: ["integer", "number"],
    FieldType.CATEGORICAL: ["integer", "number", "any"],
    FieldType.BOOLEAN: ["boolean"],
    FieldType.STRING: ["string"],
    FieldType.DATETIME: ["datetime"],
}


logger = logging.getLogger(LOGGER_NAME)


class TrainingModel(BaseModel):
    """Model object for logging training events."""

    def __init__(self, model_id: str, model_version: str):
        """Initializes a TrainingModel object.

        Args:
            model_id (str): Model identifier, as received from the Aporia dashboard.
            model_version (str): Model version - this can be any string that represents the model
                version, such as "v1" or a git commit hash.
        """
        super().__init__(model_id=model_id, model_version=model_version, set_ready_when_done=True)

    @validate_model_ready
    def log_training_set(
        self, features: DataFrame, labels: DataFrame, raw_inputs: Optional[DataFrame] = None
    ):
        """See aporia.model.Model."""
        logger.debug("Logging training set.")
        with self._handle_error("Logging training set failed, error: {}"):
            version_schema = self._get_version_schema()
            self._validate_training_dataframes(
                dataset_name="training",
                dataframes={
                    ("features", FieldCategory.FEATURES): features,
                    ("labels", FieldCategory.PREDICTIONS): labels,
                    ("raw inputs", FieldCategory.RAW_INPUTS): raw_inputs,
                },
                schema=version_schema,
            )

            raw_inputs_training_data = None
            if raw_inputs is not None:
                raw_inputs_training_data = self._calculate_dataframe_training_data(
                    raw_inputs, version_schema[FieldCategory.RAW_INPUTS]
                )

            self._event_loop.run_coroutine(
                log_training_data(
                    graphql_client=self._graphql_client,
                    model_id=self.model_id,
                    model_version=self.model_version,
                    features=self._calculate_dataframe_training_data(
                        features, version_schema[FieldCategory.FEATURES]
                    ),
                    labels=self._calculate_dataframe_training_data(
                        labels, version_schema[FieldCategory.PREDICTIONS]
                    ),
                    raw_inputs=raw_inputs_training_data,
                )
            )

    @validate_model_ready
    def log_test_set(
        self,
        features: DataFrame,
        predictions: DataFrame,
        labels: DataFrame,
        raw_inputs: Optional[DataFrame] = None,
        confidences: Optional[ndarray] = None,
    ):
        """See aporia.model.Model."""
        logger.debug("Logging test set.")
        with self._handle_error("Logging test set failed, error: {}"):
            version_schema = self._get_version_schema()
            self._validate_training_dataframes(
                dataset_name="test",
                dataframes={
                    ("features", FieldCategory.FEATURES): features,
                    ("predictions", FieldCategory.PREDICTIONS): predictions,
                    ("labels", FieldCategory.PREDICTIONS): labels,
                    ("raw inputs", FieldCategory.RAW_INPUTS): raw_inputs,
                },
                schema=version_schema,
            )

            raw_inputs_training_data = None
            if raw_inputs is not None:
                raw_inputs_training_data = self._calculate_dataframe_training_data(
                    raw_inputs, version_schema[FieldCategory.RAW_INPUTS]
                )

            self._event_loop.run_coroutine(
                log_test_data(
                    graphql_client=self._graphql_client,
                    model_id=self.model_id,
                    model_version=self.model_version,
                    features=self._calculate_dataframe_training_data(
                        features, version_schema[FieldCategory.FEATURES]
                    ),
                    predictions=self._calculate_dataframe_training_data(
                        predictions, version_schema[FieldCategory.PREDICTIONS]
                    ),
                    labels=self._calculate_dataframe_training_data(
                        labels, version_schema[FieldCategory.PREDICTIONS]
                    ),
                    raw_inputs=raw_inputs_training_data,
                )
            )

    @lru_cache(maxsize=1)
    def _get_version_schema(self) -> Dict[FieldCategory, Dict[str, FieldType]]:
        return self._event_loop.run_coroutine(
            get_model_version(
                graphql_client=self._graphql_client,
                model_id=self.model_id,
                model_version=self.model_version,
            )
        )

    @staticmethod
    def _validate_training_dataframes(
        dataset_name: str,
        dataframes: Dict[Tuple[str, FieldCategory], Optional[DataFrame]],
        schema: Dict[FieldCategory, Dict[str, FieldType]],
    ):
        for (training_data_type, field_category), data in dataframes.items():
            if data is None:
                continue

            # Check that a schema is defined for this category
            if field_category not in schema:
                raise AporiaError(
                    "Cannot report {} set {}, because it was not defined during model "
                    "version creation.".format(dataset_name, training_data_type)
                )

            # Check for missing fields
            column_names = set(data.columns)
            missing_fields = schema[field_category].keys() - column_names
            if len(missing_fields) > 0:
                logger.warning(
                    "Detected missing {training_type} in the {dataset} data - the following "
                    "{training_type} were defined during model version creation but are "
                    "not present in the {dataset} data: {missing_fields}".format(
                        training_type=training_data_type,
                        dataset=dataset_name,
                        missing_fields=missing_fields,
                    )
                )

            # Check for undefined fields
            undefined_fields = column_names - schema[field_category].keys()
            if len(undefined_fields) > 0:
                logger.warning(
                    "Detected undefined {training_type} in the {dataset} data - the following "
                    "{training_type} were found in the {dataset} data, but were not defined "
                    "during model version creation: {undefined_fields}".format(
                        training_type=training_data_type,
                        dataset=dataset_name,
                        undefined_fields=undefined_fields,
                    )
                )

            # Check that the data types match the schema
            dataframe_schema = {
                field["name"]: field["type"]
                for field in build_table_schema(data=data, index=False)["fields"]
            }
            for field_name, field_type in schema[field_category].items():
                if field_name in missing_fields:
                    continue

                if dataframe_schema[field_name] not in FIELD_TYPE_TO_TABLE_SCHEMA_TYPES[field_type]:
                    logger.warning(
                        "Detected type mismatch on field {field_name}: expected {expected_type} "
                        "type, got {actual_type}".format(
                            field_name=field_name,
                            expected_type=field_type.value,
                            actual_type=data[field_name].dtype,
                        )
                    )

    @staticmethod
    def _calculate_dataframe_training_data(
        data: DataFrame, fields_schema: Dict[str, FieldType]
    ) -> List[FieldTrainingData]:
        training_data = []
        for field_name, field_data in data.items():
            # Ignore fields that are not defined in the model version schema
            if field_name not in fields_schema:
                continue

            training_data.append(
                calculate_training_data(
                    field_name=field_name,
                    field_data=field_data,
                    field_type=fields_schema[field_name],
                )
            )

        return training_data
