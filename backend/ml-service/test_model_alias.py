
from mlflow import MlflowClient

# Connect to the existing MLflow database
client = MlflowClient(
    tracking_uri="sqlite:///mlflow.db"
)

# Retrieve Version 1 using its alias
model_version = client.get_model_version_by_alias(
    name="smart_complaint_classifier",
    alias="candidate"
)

# Display model information
print("Model Name:", model_version.name)
print("Model Version:", model_version.version)
print("Model Alias:", model_version.aliases)
print("Source Run ID:", model_version.run_id)
