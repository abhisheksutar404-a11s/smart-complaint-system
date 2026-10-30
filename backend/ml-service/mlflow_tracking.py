
import os
import pandas as pd
import mlflow
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


# ==========================================
# 1. Connect to MLflow
# ==========================================

mlflow.set_tracking_uri("sqlite:///mlflow.db")

mlflow.set_experiment("Smart Complaint Classification")


# ==========================================
# 2. Load dataset
# ==========================================

df = pd.read_csv("dataset/complaints.csv")

X = df["complaint"]
y = df["category"]

print("Dataset loaded:", len(df))


# ==========================================
# 3. Encode categories
# ==========================================

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)


# ==========================================
# 4. Split dataset
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)


# ==========================================
# 5. TF-IDF vectorization
# ==========================================

vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


# ==========================================
# 6. Train model
# ==========================================

model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)


# ==========================================
# 7. Calculate metrics
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

report = classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_,
    output_dict=True,
    zero_division=0
)

precision = report["weighted avg"]["precision"]
recall = report["weighted avg"]["recall"]
f1 = report["weighted avg"]["f1-score"]


# ==========================================
# 8. Generate artifact files
# ==========================================

os.makedirs("artifacts", exist_ok=True)

# Classification report text
report_text = classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_,
    zero_division=0
)

report_path = "artifacts/classification_report.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write(report_text)


# Confusion matrix
cm = confusion_matrix(y_test, y_pred)

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=label_encoder.classes_
)

display.plot(xticks_rotation=45)

plt.title("Complaint Classification Confusion Matrix")
plt.tight_layout()

matrix_path = "artifacts/confusion_matrix.png"

plt.savefig(matrix_path, dpi=150)
plt.close()


# ==========================================
# 9. Log experiment in MLflow
# ==========================================

with mlflow.start_run():

    # Log parameters
    mlflow.log_param("algorithm", "MultinomialNB")
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("random_state", 42)
    mlflow.log_param("vectorizer", "TfidfVectorizer")

    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)

    # Log artifacts
    mlflow.log_artifact(report_path)
    mlflow.log_artifact(matrix_path)

    # Log trained ML model
    mlflow.sklearn.log_model(
        sk_model=model,
        name="complaint_model"
    )


# ==========================================
# 10. Display results
# ==========================================

print("\nModel Evaluation Results")

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)

print("\nArtifacts created:")
print(report_path)
print(matrix_path)

print("\nMLflow metrics and artifacts logged successfully!")
