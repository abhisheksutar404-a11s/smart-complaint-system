import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder


# ==========================================
# 1. Load dataset
# ==========================================

df = pd.read_csv("dataset/complaints.csv")

print("Dataset loaded successfully!")
print("Total complaints:", len(df))


# ==========================================
# 2. Input and Output
# ==========================================

# X = Input
# Complaint text is the input
X = df["complaint"]


# y = Output
# Category is the output
y = df["category"]


print("\nInput complaints:")
print(X.head())

print("\nTarget categories:")
print(y.head())


# ==========================================
# 3. Split data into training and testing
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining data size:", len(X_train))
print("Testing data size:", len(X_test))


# ==========================================
# 4. Convert complaint text into numbers
#    using TF-IDF
# ==========================================

vectorizer = TfidfVectorizer()

# Learn vocabulary from training data
# and convert training complaints into numbers
X_train_tfidf = vectorizer.fit_transform(X_train)

# Convert testing complaints using
# the same vocabulary
X_test_tfidf = vectorizer.transform(X_test)


print("\nTF-IDF shape:")
print(X_train_tfidf.shape)


# ==========================================
# 5. Show first training complaint
# ==========================================

print("\nFirst training complaint:")
print(X_train.iloc[0])


# ==========================================
# 6. Show TF-IDF values
# ==========================================

print("\nTF-IDF values for first complaint:")
print(X_train_tfidf[0])


# ==========================================
# 7. Convert categories into numbers
#    using LabelEncoder
# ==========================================

label_encoder = LabelEncoder()

# Learn category names and convert them to numbers
y_train_encoded = label_encoder.fit_transform(y_train)

# Convert testing categories using
# the same encoding
y_test_encoded = label_encoder.transform(y_test)


print("\nCategory names:")
print(label_encoder.classes_)


print("\nEncoded training categories:")
print(y_train_encoded[:10])


print("\nEncoded testing categories:")
print(y_test_encoded[:10])


# ==========================================
# 8. Final shapes
# ==========================================

print("\nFinal data shapes:")

print("X_train TF-IDF:", X_train_tfidf.shape)
print("X_test TF-IDF:", X_test_tfidf.shape)

print("y_train:", y_train_encoded.shape)
print("y_test:", y_test_encoded.shape)


# ==========================================
# END
# ==========================================

print("\nPreprocessing completed successfully!")