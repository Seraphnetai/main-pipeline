from zenml.pipelines import pipeline

@pipeline(enable_cache=False)
def feast_pipeline(
    get_historical_features,
):
    features = get_historical_features()
