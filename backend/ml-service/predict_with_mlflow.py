
import mlflow
import mlflow.sklearn
import joblib

# Connect to MLflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# Load registered classifier
model_uri = "models:/smart_complaint_classifier@candidate"
model = mlflow.sklearn.load_model(model_uri)

# Load existing TF-IDF vectorizer and label encoder
vectorizer = joblib.load("tfidf_vectorizer.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Example complaint
complaint = "My internet connection is not working"

# Convert complaint text into numerical features
complaint_vector = vectorizer.transform([complaint])

# Predict category
prediction = model.predict(complaint_vector)

# Convert numerical prediction into category name
category = label_encoder.inverse_transform(prediction)[0]

print("Complaint:", complaint)
print("Predicted Category:", category)
