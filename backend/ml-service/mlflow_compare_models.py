
import os
import pandas as pd
import mlflow
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    ConfusionMatrixDisplay
)


# 1. Load dataset
df = pd.read_csv("dataset/complaints.csv")

X = df["complaint"]
y = df["category"]

print("Dataset loaded:", len(df))


# 2. Encode categories
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)


# 3. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)


# 4. Convert text into TF-IDF
vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


# 5. Create Logistic Regression model
model = LogisticRegression(max_iter=1000)


# 6. Train model
model.fit(X_train_tfidf, y_train)


# 7. Make predictions
y_pred = model.predict(X_test_tfidf)


# 8. Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test, y_pred, average="weighted", zero_division=0
)

recall = recall_score(
    y_test, y_pred, average="weighted", zero_division=0
)

f1 = f1_score(
    y_test, y_pred, average="weighted", zero_division=0
)


print("\nLogistic Regression Results")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)


# 9. Create artifact folder
os.makedirs("artifacts_logistic_regression", exist_ok=True)

report_path = "artifacts_logistic_regression/classification_report.txt"
matrix_path = "artifacts_logistic_regression/confusion_matrix.png"


# 10. Save classification report
report = classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_,
    zero_division=0
)

with open(report_path, "w") as file:
    file.write(report)


# 11. Save confusion matrix
ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred,
    display_labels=label_encoder.classes_,
    xticks_rotation="vertical"
)

plt.tight_layout()
plt.savefig(matrix_path)
plt.close()


# 12. Log experiment in MLflow
mlflow.set_experiment("Smart Complaint Classification")

with mlflow.start_run(run_name="Logistic Regression"):

    mlflow.log_param("algorithm", "LogisticRegression")
    mlflow.log_param("max_iter", 1000)
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("random_state", 42)
    mlflow.log_param("vectorizer", "TfidfVectorizer")

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)

    mlflow.log_artifact(report_path)
    mlflow.log_artifact(matrix_path)

print("\nLogistic Regression experiment logged successfully!")
