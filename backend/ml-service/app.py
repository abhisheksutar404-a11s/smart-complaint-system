from fastapi import FastAPI
from pydantic import BaseModel
import joblib


# ==========================================
# CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Smart Complaint ML Service",
    description="ML API for complaint category prediction",
    version="1.0"
)


# ==========================================
# LOAD TRAINED ML FILES
# ==========================================

model = joblib.load("complaint_model.pkl")

vectorizer = joblib.load("tfidf_vectorizer.pkl")

label_encoder = joblib.load("label_encoder.pkl")


print("ML model loaded successfully!")


# ==========================================
# REQUEST DATA FORMAT
# ==========================================

class ComplaintRequest(BaseModel):

    complaint: str


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Smart Complaint ML Service is running"
    }


# ==========================================
# PREDICTION ENDPOINT
# ==========================================

@app.post("/predict")
def predict(request: ComplaintRequest):

    # Get complaint text
    complaint_text = request.complaint


    # Convert complaint into TF-IDF features
    complaint_vector = vectorizer.transform(
        [complaint_text]
    )


    # Predict category
    prediction = model.predict(
        complaint_vector
    )


    # Convert encoded label back to category name
    category = label_encoder.inverse_transform(
        prediction
    )[0]


    # Calculate confidence
    probabilities = model.predict_proba(
        complaint_vector
    )[0]

    confidence = float(max(probabilities))


    # Return JSON response
    return {

        "category": category,

        "confidence": confidence

    }