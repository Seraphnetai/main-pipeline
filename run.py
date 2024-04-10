from steps.get_labeled_data import get_labeled_data
from steps.get_historical_features import historical_features
from steps.get_or_create_dataset import get_or_create_dataset
from pipelines import labeling_pipeline, feast_pipeline

if __name__ == "__main__":
    pipeline = feast_pipeline(historical_features)
    # pipeline = labeling_pipeline(
    #     get_or_create_dataset,
    #     get_labeled_data,
    # )
    pipeline.run()
