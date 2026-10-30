
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Load dataset
df = pd.read_csv("dataset/complaints.csv")

X = df["complaint"]
y = df["category"]

# Encode category labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

# Convert text into numerical features
vectorizer = TfidfVectorizer()
X_train_vector = vectorizer.fit_transform(X_train)
X_test_vector = vectorizer.transform(X_test)

# Train model
model = MultinomialNB()
model.fit(X_train_vector, y_train)

# Make predictions
y_pred = model.predict(X_test_vector)

# Generate confusion matrix
cm = confusion_matrix(
    y_test,
    y_pred,
    labels=range(len(label_encoder.classes_))
)

print("Categories:", label_encoder.classes_)
print("\nConfusion Matrix:\n", cm)

# Display confusion matrix
display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=label_encoder.classes_
)

display.plot(cmap="Blues", xticks_rotation=45)
plt.title("Smart Complaint System - Confusion Matrix")
plt.tight_layout()
plt.show()
