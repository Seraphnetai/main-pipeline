from zenml.pipelines import pipeline

@pipeline(enable_cache=False)
def labeling_pipeline(
    get_or_create_dataset,
    get_labeled_data,
):
    dataset = get_or_create_dataset()
    data = get_labeled_data(dataset)
