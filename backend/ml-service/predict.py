import joblib

# Load the trained model
model = joblib.load("complaint_model.pkl")

# Load the TF-IDF vectorizer
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Load the label encoder
label_encoder = joblib.load("label_encoder.pkl")


print("ML model loaded successfully!")


# Function to predict complaint category
def predict_complaint(complaint):
    # Convert complaint text into TF-IDF features
    complaint_tfidf = vectorizer.transform([complaint])

    # Predict encoded category
    prediction = model.predict(complaint_tfidf)

    # Convert encoded category back to category name
    category = label_encoder.inverse_transform(prediction)[0]

    return category


# Test complaint
complaint = input("\nEnter your complaint: ")

category = predict_complaint(complaint)

print("\nComplaint:", complaint)
print("Predicted Category:", category)