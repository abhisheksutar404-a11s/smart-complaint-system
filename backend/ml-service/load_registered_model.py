
import mlflow
import mlflow.sklearn

# Connect to the existing MLflow database
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# Model URI using the candidate alias
model_uri = "models:/smart_complaint_classifier@candidate"

# Load the registered model
model = mlflow.sklearn.load_model(model_uri)

# Display information
print("Registered model loaded successfully!")
print("Model type:", type(model).__name__)
