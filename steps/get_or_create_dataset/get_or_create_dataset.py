from pathlib import Path

from zenml.integrations.label_studio import steps as label_studio_steps


PROJECT_NAME = "all_in_one"
CONFIG_PATH = Path(__file__).parent / "config.xml"

label_studio_registration_params = label_studio_steps.LabelStudioDatasetRegistrationParameters(
    label_config=CONFIG_PATH.open("rt").read(),
    dataset_name=PROJECT_NAME,
)

get_or_create_dataset = label_studio_steps.get_or_create_dataset(
    label_studio_registration_params
)
