from datetime import datetime
from typing import Any, Dict, List, Union
import pandas as pd

from zenml.steps import BaseParameters, step, StepContext
from zenml.exceptions import DoesNotExistException

entity_dict = {
    "task_id": [1],
}
features = [
    "annotations:x",
    "annotations:y",
    "annotations:width",
    "annotations:height",
    "annotations:rectanglelabels",
    "tasks:image",
]

class FeastHistoricalFeaturesParameters(BaseParameters):
    """Feast Feature Store historical data step configuration."""

    entity_dict: Union[Dict[str, Any], str]
    features: List[str]
    full_feature_names: bool = False

    class Config:
        arbitrary_types_allowed = True


@step
def get_historical_features(
        params: FeastHistoricalFeaturesParameters,
        context: StepContext,
) -> pd.DataFrame:
    """Feast Feature Store historical data step

    Args:
        config: The step configuration.
        context: The step context.

    Returns:
        The historical features as a DataFrame.
    """
    if not context.stack:
        raise DoesNotExistException(
            "No active stack is available. Please make sure that you have registered and set a stack."
        )
    elif not context.stack.feature_store:
        raise DoesNotExistException(
            "The Feast feature store component is not available. "
            "Please make sure that the Feast stack component is registered as part of your current active stack."
        )

    feature_store_component = context.stack.feature_store
    entity_df = pd.DataFrame.from_dict(params.entity_dict)
    entity_df = entity_df.assign(event_timestamp=datetime.now())

    return feature_store_component.get_historical_features(
        entity_df=entity_df,
        features=params.features,
        full_feature_names=params.full_feature_names,
    )


historical_features = get_historical_features(
    params=FeastHistoricalFeaturesParameters(
        entity_dict=entity_dict,
        features=features,
    ),
)
