import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# 1. Load dataset
# ==========================================

df = pd.read_csv("dataset/complaints.csv")

print("Dataset loaded successfully!")
print("Total complaints:", len(df))


# ==========================================
# 2. Input and Output
# ==========================================

X = df["complaint"]
y = df["category"]


# ==========================================
# 3. Convert categories into numbers
# ==========================================

label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)

print("\nCategory names:")
print(label_encoder.classes_)

print("\nEncoded categories:")
print(y_encoded)


# ==========================================
# 4. Split data
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

print("\nTraining data size:", len(X_train))
print("Testing data size:", len(X_test))


# ==========================================
# 5. Convert text into numbers using TF-IDF
# ==========================================

vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)

X_test_tfidf = vectorizer.transform(X_test)

print("\nTF-IDF training shape:")
print(X_train_tfidf.shape)

print("TF-IDF testing shape:")
print(X_test_tfidf.shape)


# ==========================================
# 6. Create ML model
# ==========================================

model = MultinomialNB()


# ==========================================
# 7. Train model
# ==========================================

model.fit(X_train_tfidf, y_train)

print("\nModel training completed successfully!")


# ==========================================
# 8. Test model
# ==========================================

y_pred = model.predict(X_test_tfidf)


# ==========================================
# 9. Accuracy
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")
print(accuracy)


# ==========================================
# 10. Classification report
# ==========================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_,
        zero_division=0
    )
)


# ==========================================
# 11. Test new complaint
# ==========================================

new_complaint = [
    "My WiFi is not working in the computer lab"
]

new_complaint_tfidf = vectorizer.transform(new_complaint)

prediction = model.predict(new_complaint_tfidf)

predicted_category = label_encoder.inverse_transform(prediction)

print("\nNew Complaint:")
print(new_complaint[0])

print("\nPredicted Category:")
print(predicted_category[0])


# ==========================================
# 12. Save ML components
# ==========================================

joblib.dump(model, "complaint_model.pkl")

joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

joblib.dump(label_encoder, "label_encoder.pkl")


print("\nML model saved successfully!")
print("complaint_model.pkl")
print("tfidf_vectorizer.pkl")
print("label_encoder.pkl")


print("\n================================")
print("Training and saving completed!")
print("================================")