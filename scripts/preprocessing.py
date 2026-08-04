import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/factory_flow_data.csv")

# Shape
print("Shape:")
print(df.shape)

# Columns
print("\nColumns:")
print(df.columns)

# First five rows
print("\nFirst Five Rows:")
print(df.head())

# Information
print("\nDataset Info:")
print(df.info())

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Remove duplicates
df = df.drop_duplicates()

# Summary statistics
print("\nSummary Statistics:")
print(df.describe())

# Save cleaned dataset
df.to_csv(
    "data/processed/cleaned_factory_flow_data.csv",
    index=False
)

print("\nDataset cleaned successfully!")