import pandas as pd

df = pd.read_csv("dataset/complaints.csv")

print("First 5 complaints:")
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nCategory counts:")
print(df["category"].value_counts())

print("\nColumn names:")
print(df.columns)

print("\nDataset size:")
print(df.shape)