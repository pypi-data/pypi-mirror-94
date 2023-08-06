import logging
from typing import List, Optional, Union

import numpy as np
from pandas import Series

from aporia.core.errors import AporiaError
from aporia.core.graphql_client import GraphQLClient
from aporia.core.logging_utils import LOGGER_NAME
from aporia.core.types.field import FieldType

logger = logging.getLogger(LOGGER_NAME)

MAX_BINS = 1000


class FieldTrainingData:
    """Field training data."""

    def __init__(
        self,
        field_name: str,
        bins: Optional[List[Union[float, int, str, bool]]] = None,
        counts: Optional[List[int]] = None,
        min: Optional[float] = None,
        max: Optional[float] = None,
        sum: Optional[float] = None,
        median: Optional[float] = None,
        average: Optional[float] = None,
        std: Optional[float] = None,
        variance: Optional[float] = None,
        num_samples: Optional[int] = None,
        num_missing_values: Optional[int] = None,
        num_posinf_values: Optional[int] = None,
        num_neginf_values: Optional[int] = None,
        num_unique_values: Optional[int] = None,
        num_zero_values: Optional[int] = None,
    ):
        """Initializes a FieldTrainingData object.

        Args:
            field_name: Field name
            bins: Histogram bin edges. Defaults to None.
            counts: Hitsogram. Defaults to None.
            min: Minimum value. Defaults to None.
            max: Maximum Value. Defaults to None.
            sum: Sum of all values. Defaults to None.
            median: Median values. Defaults to None.
            average: Average value. Defaults to None.
            std: Standard deviation value. Defaults to None.
            variance: Variance value. Defaults to None.
            num_samples: Number of data samples. Defaults to None.
            num_missing_values: Number of missing values. Defaults to None.
            num_posinf_values: Number of positive infinite values. Defaults to None.
            num_neginf_values: Number of negative infinite values. Defaults to None.
            num_unique_values: Number of unique values. Defaults to None.
            num_zero_values: Number of zero values. Defaults to None.
        """
        self.field_name = field_name
        self.bins = bins
        self.counts = counts
        self.min = min
        self.max = max
        self.sum = sum
        self.median = median
        self.average = average
        self.std = std
        self.variance = variance
        self.num_samples = num_samples
        self.num_missing_values = num_missing_values
        self.num_posinf_values = num_posinf_values
        self.num_neginf_values = num_neginf_values
        self.num_unique_values = num_unique_values
        self.num_zero_values = num_zero_values

    def serialize(self) -> dict:
        """Serializes the field training data to a dict.

        Returns:
            Serialized training data.
        """
        return {
            "fieldName": self.field_name,
            "bins": self.bins,
            "counts": self.counts,
            "min": self.min,
            "max": self.max,
            "sum": self.sum,
            "median": self.median,
            "average": self.average,
            "std": self.std,
            "variance": self.variance,
            "numSamples": self.num_samples,
            "numMissingValues": self.num_missing_values,
            "numPosinfValues": self.num_posinf_values,
            "numNeginfValues": self.num_neginf_values,
            "numUniqueValues": self.num_unique_values,
            "numZeroValues": self.num_zero_values,
        }


async def log_training_data(
    graphql_client: GraphQLClient,
    model_id: str,
    model_version: str,
    features: List[FieldTrainingData],
    labels: List[FieldTrainingData],
    raw_inputs: Optional[List[FieldTrainingData]] = None,
):
    """Reports training data.

    Args:
        graphql_client: GraphQL client
        model_id: Model ID
        model_version: Mode version
        features: Training set features.
        labels: Training set labels.
        raw_inputs: Training set raw inputs. Defaults to None.
    """
    query = """
        mutation LogTrainingSet(
            $modelId: String!,
            $modelVersion: String!,
            $features: [FieldTrainingData]!
            $labels: [FieldTrainingData]!
            $rawInputs: [FieldTrainingData]
        ) {
            logTrainingSet(
                modelId: $modelId,
                modelVersion: $modelVersion,
                features: $features
                labels: $labels
                rawInputs: $rawInputs
            ) {
                warnings
            }
        }
    """

    serialized_raw_inputs = None
    if raw_inputs is not None:
        serialized_raw_inputs = [field_data.serialize() for field_data in raw_inputs]

    variables = {
        "modelId": model_id,
        "modelVersion": model_version,
        "features": [field_data.serialize() for field_data in features],
        "labels": [field_data.serialize() for field_data in labels],
        "rawInputs": serialized_raw_inputs,
    }

    result = await graphql_client.query_with_retries(query, variables)
    for warning in result["logTrainingSet"]["warnings"]:
        logger.warning(warning)


async def log_test_data(
    graphql_client: GraphQLClient,
    model_id: str,
    model_version: str,
    features: List[FieldTrainingData],
    predictions: List[FieldTrainingData],
    labels: List[FieldTrainingData],
    raw_inputs: Optional[List[FieldTrainingData]] = None,
):
    """Reports test data.

    Args:
        graphql_client: GraphQL client
        model_id: Model ID
        model_version: Mode version
        features: Test set features.
        predictions: Test set features.
        labels: Test set labels.
        raw_inputs: Test set raw inputs. Defaults to None.
    """
    query = """
        mutation LogTestSet(
            $modelId: String!,
            $modelVersion: String!,
            $features: [FieldTrainingData]!
            $predictions: [FieldTrainingData]!
            $labels: [FieldTrainingData]!
            $rawInputs: [FieldTrainingData]
        ) {
            logTestSet(
                modelId: $modelId,
                modelVersion: $modelVersion,
                features: $features
                predictions: $predictions
                labels: $labels
                rawInputs: $rawInputs
            ) {
                warnings
            }
        }
    """

    serialized_raw_inputs = None
    if raw_inputs is not None:
        serialized_raw_inputs = [field_data.serialize() for field_data in raw_inputs]

    variables = {
        "modelId": model_id,
        "modelVersion": model_version,
        "features": [field_data.serialize() for field_data in features],
        "predictions": [field_data.serialize() for field_data in predictions],
        "labels": [field_data.serialize() for field_data in labels],
        "rawInputs": serialized_raw_inputs,
    }

    result = await graphql_client.query_with_retries(query, variables)
    for warning in result["logTestSet"]["warnings"]:
        logger.warning(warning)


def calculate_training_data(
    field_name: str, field_data: Series, field_type: FieldType
) -> FieldTrainingData:
    """Calculates training data for a single field.

    Args:
        field_name (str): Field name
        field_data (Series): Field data
        field_type (FieldType): Field type

    Returns:
        FieldTrainingData: Field training data.
    """
    # We currently don't support datetime training data
    if field_type == FieldType.DATETIME:
        return FieldTrainingData(field_name=field_name)
    elif field_type == FieldType.NUMERIC:
        return _calculate_numeric_training_data(field_name, field_data)
    elif field_type in [FieldType.BOOLEAN, FieldType.STRING, FieldType.CATEGORICAL]:
        return _calculate_categorical_training_data(field_name, field_data)

    raise AporiaError("Unsupported field type {} of field {}".format(field_type.value, field_name))


def _calculate_categorical_training_data(field_name: str, field_data: Series) -> FieldTrainingData:
    valid_values = field_data[field_data.notnull()]
    bins, counts = np.unique(valid_values, return_counts=True)

    # Note: There is a possible edge case here in which a user passes an infinite value
    # as one of the categories. We chose not to count those values at the moment, since
    # most numpy functions don't handle str and bool well, which would force us to split
    # this function up for each field type.
    return FieldTrainingData(
        field_name=field_name,
        bins=bins.tolist(),
        counts=counts.tolist(),
        num_samples=len(valid_values),
        num_missing_values=len(field_data) - len(valid_values),
        num_unique_values=len(bins),
    )


def _calculate_numeric_training_data(field_name: str, field_data: Series) -> FieldTrainingData:
    # Cast everything to float - this converts None to np.nan
    field_data = field_data.astype(float)

    # Filter out infinite and NaN values (isfinite is False for NaN)
    finite_values = field_data[np.isfinite(field_data)]

    bin_edges = np.histogram_bin_edges(finite_values, bins="auto")
    if len(bin_edges) > MAX_BINS:
        counts, bins = np.histogram(finite_values, bins=MAX_BINS)
    else:
        counts, bins = np.histogram(finite_values, bins=bin_edges)

    return FieldTrainingData(
        field_name=field_name,
        bins=bins.tolist(),
        counts=counts.tolist(),
        min=np.min(finite_values),
        max=np.max(finite_values),
        sum=np.sum(finite_values),
        median=np.median(finite_values),
        average=np.average(finite_values),
        std=np.std(finite_values),
        variance=np.var(finite_values),
        num_samples=len(finite_values),
        num_missing_values=np.count_nonzero(np.isnan(field_data)),
        num_posinf_values=np.count_nonzero(np.isposinf(field_data)),
        num_neginf_values=np.count_nonzero(np.isneginf(field_data)),
        num_zero_values=np.count_nonzero(finite_values == 0),
    )
